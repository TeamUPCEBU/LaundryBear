from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import FormView, RedirectView
from django.contrib.auth import authenticate, login, logout


class LoginView(FormView):
    success_view_name = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(LoginView, self).form_valid(form)
        user = form.cleaned_data['user']
        login(self.request, user)
        return response

    def get_success_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        else:
            return reverse(self.success_view_name)


class LogoutView(RedirectView):
    permanent = False
    login_view_name = None

    def get_redirect_url(self, *args, **kwargs):
        return reverse(self.login_view_name)

    def get(self, request, *args, **kwargs):
        response = super(LogoutView, self).get(request, *args, **kwargs)
        logout(request)
        return response
