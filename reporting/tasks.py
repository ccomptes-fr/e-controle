import logging
import time
from datetime import timedelta, datetime

from actstream import action
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from control.models import Control, ResponseFile
from utils.email import send_email
from utils.file import get_last_file_metadata_in_control_folder

logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


ACTION_LOG_VERB_SENT = "files report email sent"
ACTION_LOG_VERB_NOT_SENT = "files report email not sent"

ACTION_LOG_VERB_SENT_CLEAN = "clean files report email sent"
ACTION_LOG_VERB_NOT_SENT_CLEAN = "clean files report email not sent"

ACTION_LOG_VERB_SENT_ORPHANS = "orphans controls report email sent"
ACTION_LOG_VERB_NOT_SENT_ORPHANS = "orphans controls report email not sent"

EMAIL_SPACING_TIME_SECONDS = settings.EMAIL_SPACING_TIME_MILLIS / 1000


def get_date_cutoff(control):
    """
    The reporting tool looks for files uploaded after a certain date cutoff, which could be :
    - The last thime a reporting email was sent
    - 24h from now
    """
    latest_email_sent = control.actor_actions.filter(verb=ACTION_LOG_VERB_SENT).first()
    if latest_email_sent:
        date_cutoff = latest_email_sent.timestamp
    else:
        date_cutoff = timezone.now() - timedelta(hours=24)
    return date_cutoff


def get_files(control):
    date_cutoff = get_date_cutoff(control)
    logger.info(
        f'Looking for files uploaded after this timestamp: {date_cutoff.strftime("%Y-%m-%d %H:%M:%S")}'
    )
    files = ResponseFile.objects.filter(
        question__theme__questionnaire__control=control,
        created__gt=date_cutoff,
    )
    logger.info(f"Number of files: {len(files)}")
    return files


def add_log_entry(control, verb, to, subject):
    log_message = f'Sending email "{subject}" to: {to}.'
    action_details = {
        "sender": control,
        "verb": verb,
        "description": log_message,
    }
    action.send(**action_details)


def get_admin_emails():
    # admin user has not a email
    return list(User.objects.filter(is_staff=True, is_active=True).exclude(email="").values_list("email", flat=True))

@shared_task(queue=settings.CELERY_QUEUE)
def sent_emails(recipient_list, subject, html_template, text_template, context, control, action_sent, action_not_sent):
    number_of_sent_email = send_email(
      to=recipient_list,
      subject=subject,
      html_template=html_template,
      text_template=text_template,
      extra_context=context,
    )
    logger.info(f"Sent {number_of_sent_email} emails")
    number_of_recipients = len(recipient_list)
    if number_of_sent_email != number_of_recipients:
        logger.warning(
          f"There was {number_of_recipients} recipient(s), "
          f"but {number_of_sent_email} email(s) sent."
        )
    if number_of_sent_email > 0:
        logger.info(f"Email sent for control {control.id}")
        verb = action_sent
    else:
        logger.info(f"No email was sent for control {control.id}")
        verb = action_not_sent

    add_log_entry(control, verb, recipient_list, subject)

    logger.info(
      f"Waiting {EMAIL_SPACING_TIME_SECONDS}s after emailing for control {control.id}"
    )

@shared_task(queue=settings.CELERY_QUEUE)
def send_files_report():
    html_template = "reporting/email/files_report.html"
    text_template = "reporting/email/files_report.txt"
    for control in Control.objects.all():
        logger.info(f"Contrôle : {control.id}")
        if control.depositing_organization:
            subject = control.depositing_organization
        else:
            subject = control.title
        subject += " - de nouveaux documents déposés !"
        files = get_files(control)
        if not files:
            logger.info(f"Pas de nouveau document, arrêt.")
            continue
        recipient_list = [
            access.userprofile.user.email
            for access in control.access.all()
            if access.userprofile.send_files_report == True
        ]
        if not recipient_list:
            logger.info(f"Pas de destinataire, arrêt.")
            continue
        logger.debug(f"Destinataires : {len(recipient_list)}")
        date_cutoff = get_date_cutoff(control)
        context = {
            "control": control,
            "date_cutoff": date_cutoff.strftime("%A %d %B %Y"),
            "files": files,
        }
        sent_emails(recipient_list, subject, html_template, text_template, context, control, ACTION_LOG_VERB_SENT,
                    ACTION_LOG_VERB_NOT_SENT)
        time.sleep(EMAIL_SPACING_TIME_SECONDS)


@shared_task(queue=settings.CELERY_QUEUE)
def send_clean_controls_report():
    html_template = "reporting/email/clean_controls_report.html"
    text_template = "reporting/email/clean_controls_report.txt"

    admin_list = get_admin_emails()

    # files uploaded 2 years from now
    date_cutoff = datetime.now() - timedelta(weeks=2 * 52, days=3, seconds=34)

    for control in Control.objects.active():
        logger.info(f"Processing active control: {control.id}")

        last_file = get_last_file_metadata_in_control_folder(control.reference_code)
        logger.debug(f"Last file: {last_file}")
        if last_file and last_file[1] < date_cutoff:
            recipients = control.user_profiles.filter(send_files_report=True)
            recipient_list = list(
                set(list(recipients.values_list("user__email", flat=True)) + admin_list)
            )
            logger.info(f"Recipients: {recipient_list}")

            if control.depositing_organization:
                subject = control.depositing_organization
            else:
                subject = control.title
            subject += " - proposition d'espace de dépôt à supprimer"

            context = {
                "control": control,
                "email": settings.DEFAULT_FROM_EMAIL,
                "date_cutoff": date_cutoff.strftime("%A %d %B %Y"),
                "has_file": last_file[0] > 0,
            }

            sent_emails(recipient_list, subject, html_template, text_template, context, control,
                        ACTION_LOG_VERB_SENT_CLEAN, ACTION_LOG_VERB_NOT_SENT_CLEAN)

            time.sleep(EMAIL_SPACING_TIME_SECONDS)
        else:
            logger.info(f"Active control not too old: {control.id}")


@shared_task(queue=settings.CELERY_QUEUE)
def send_orphans_controls_report():
    html_template = "reporting/email/orphans_controls_report.html"
    text_template = "reporting/email/orphans_controls_report.txt"

    logger.info("Processing orphans controls")

    recipient_list = get_admin_emails()

    # get "orphans" controls (equipe de controle and organisme interroge empty)
    orphan_controls = []
    for control in Control.objects.active():
        if not control.user_profiles.exists():
            orphan_controls.append(control)

    if orphan_controls:
        subject = "Liste des contrôles orphelins"

        context = {"controls": orphan_controls}
        sent_emails(recipient_list, subject, html_template, text_template, context, orphan_controls[0],
                    ACTION_LOG_VERB_SENT_ORPHANS, ACTION_LOG_VERB_NOT_SENT_ORPHANS)

        time.sleep(EMAIL_SPACING_TIME_SECONDS)
    else:
        logger.info("No orphans controls")

