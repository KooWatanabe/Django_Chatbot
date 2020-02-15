from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, CreateView
from . import forms

User = get_user_model()


class UserCreateView(CreateView):
    form_class = forms.UserCreateForm
    template_name = "register/user_create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        crrent_site = get_current_site(self.request)
        domain = crrent_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('register/mail_template/subject.txt', context)
        message = render_to_string('register/mail_template/message.txt', context)
        user.email_user(subject, message)

        return redirect('register:user_create_dane')


class UserCreateDaneView(TemplateView):
    template_name = "register/user_create_dane.html"


class UserCreateCompleteView(TemplateView):
    template_name = "register/user_create_complete.html"
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60)

    def get(self, request, **kwargs):
        token = kwargs.get('token', None)
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
        except SignatureExpired:
            return HttpResponseBadRequest()
        except BadSignature:
            return  HttpResponseBadRequest()
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, kwargs)

        return HttpResponseBadRequest()