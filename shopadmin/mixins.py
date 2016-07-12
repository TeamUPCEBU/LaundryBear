from LaundryBear.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.utils.decorators import method_decorator

class ShopAdminLoginRequiredMixin(LoginRequiredMixin):
    login_view_name = 'client:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user = request.user
            if user.userprofile.account_type == 2:
                return super(ShopAdminLoginRequiredMixin, self).dispatch(request,
                                                                     *args, **kwargs)
            elif user.userprofile.account_type == 1:
                return redirect('client:menu')
            else:
                return redirect('management:menu')
        else:
            return super(ShopAdminLoginRequiredMixin, self).dispatch(request,
                                                                 *args, **kwargs)
