from magicauth.views import LoginView as MagicAuthLoginView
from alerte.models import Alert
from django.db.models import Q
from django.utils import timezone

class LoginView(MagicAuthLoginView):

  template_name = 'login/login.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    now = timezone.now()
    alerte = Alert.objects.filter(
        Q(start_date__lt=now) | Q(start_date=None)
    ).filter(
        Q(end_date__gt=now) | Q(end_date=None)
    ).first()
    context['alerte'] = alerte
    return context
