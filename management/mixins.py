from LaundryBear.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class AdminLoginRequiredMixin(LoginRequiredMixin):
	login_view_name = 'management:login-admin'

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			if request.user.is_staff:
				return super(AdminLoginRequiredMixin, self).dispatch(request,
																	 *args, **kwargs)
			else:
				# redirect to client menu if not staff
				return redirect('client:menu')
		else:
			return super(AdminLoginRequiredMixin, self).dispatch(request,
																 *args, **kwargs)