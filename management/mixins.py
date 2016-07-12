from LaundryBear.mixins import LoginRequiredMixin

from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class AdminLoginRequiredMixin(LoginRequiredMixin):
	login_view_name = 'management:login-admin'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			user = request.user
			if user.is_staff and user.userprofile.account_type == 3:
				return super(AdminLoginRequiredMixin, self).dispatch(request,
																	 *args, **kwargs)
			else:
				return redirect('client:menu')
		else:
			return super(AdminLoginRequiredMixin, self).dispatch(request,
																 *args, **kwargs)
