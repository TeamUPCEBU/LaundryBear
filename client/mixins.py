from django.shortcuts import redirect
from LaundryBear.mixins import LoginRequiredMixin

class ClientLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            userprofile = request.user.userprofile
            if userprofile.account_type == 1:
                return super(ClientLoginRequiredMixin, self).dispatch(request,
                                                                     *args, **kwargs)
            elif userprofile.account_type == 2:
                return redirect('shopadmin:menu')

            elif userprofile.account_type == 3:
                return redirect('management:menu')
        else:
            return super(ClientLoginRequiredMixin, self).dispatch(request,
                                                                 *args, **kwargs)
