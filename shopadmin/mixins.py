from LaundryBear.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.utils.decorators import method_decorator

class ShopAdminLoginRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            userprofile = request.user.userprofile
            if userprofile.account_type == 2: # shop admin
                return super(ShopAdminLoginRequiredMixin, self).dispatch(request,
                                                                     *args, **kwargs)
            elif userprofile.account_type == 1 or userprofile.account_type == 4: #client
                return redirect('client:menu')

            elif userprofile.account_type == 3: # laundry bear admin (mgt)
                return redirect('management:menu')
        else:
            return super(ShopAdminLoginRequiredMixin, self).dispatch(request,
                                                                 *args, **kwargs)
