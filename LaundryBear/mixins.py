from LaundryBear import settings

from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class LoginRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    login_view_name = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super(LoginRequiredMixin, self).dispatch(request, *args,
                **kwargs)
        else:
            redirect_url = reverse(self.login_view_name)
            redirect_url = '{0}?next={1}'.format(redirect_url, request.path)
            return redirect(redirect_url)
