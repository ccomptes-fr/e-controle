from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin

from sendfile import sendfile

from .models import Questionnaire, Theme, QuestionFile, ResponseFile


class QuestionnaireList(LoginRequiredMixin, ListView):
    template_name = "ecc/questionnaire_list.html"
    context_object_name = 'questionnaires'

    def get_queryset(self):
        return Questionnaire.objects.filter(control=self.request.user.profile.control)


class QuestionnaireDetail(LoginRequiredMixin, DetailView):
    template_name = "ecc/questionnaire_detail.html"
    context_object_name = 'questionnaire'
    model = Questionnaire

    def get_queryset(self):
        return self.model.objects.filter(control=self.request.user.profile.control)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_list = Theme.objects.filter(questionnaire=self.object)
        questionnaire_list = Questionnaire.objects.filter(control=self.request.user.profile.control)
        context['themes'] = theme_list
        context['questionnaires'] = questionnaire_list
        return context


class UploadResponseFile(LoginRequiredMixin, CreateView):
    model = ResponseFile
    fields = ('file',)

    def form_valid(self, form):
        try:
            question_id = form.data['question_id']
        except KeyError:
            raise forms.ValidationError("Question ID was missing on file upload")
        self.object = form.save(commit=False)
        self.object.question_id = question_id
        self.object.author = self.request.user
        self.object.save()
        data = {'status': 'success'}
        response = JsonResponse(data)
        return response


class SendFileMixin(SingleObjectMixin):
    model = None

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return sendfile(request, obj.file.path)


class SendQuestionnaireFile(SendFileMixin, LoginRequiredMixin, View):
    model = Questionnaire

    def get_queryset(self):
        return self.model.objects.filter(control=self.request.user.profile.control)


class SendQuestionFile(SendFileMixin, LoginRequiredMixin, View):
    model = QuestionFile

    def get_queryset(self):
        # The user should only have access to files that belong to the control
        # he was associated with. That's why we filter-out based on the user's
        # control.
        return self.model.objects.filter(
            question__theme__questionnaire__control=self.request.user.profile.control)


class SendResponseFile(SendQuestionFile):
    model = ResponseFile


upload_response_file = UploadResponseFile.as_view()
questionnaire_list = QuestionnaireList.as_view()
questionnaire_detail = QuestionnaireDetail.as_view()
send_questionnaire_file = SendQuestionnaireFile.as_view()
send_question_file = SendQuestionFile.as_view()
send_response_file = SendResponseFile.as_view()