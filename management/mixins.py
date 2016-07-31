from LaundryBear.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator


class AdminLoginRequiredMixin(LoginRequiredMixin):

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			userprofile = request.user.userprofile
			if userprofile.account_type == 3:
				return super(AdminLoginRequiredMixin, self).dispatch(request,
																	 *args, **kwargs)
			elif userprofile.account_type == 1:
				return redirect('client:menu')

			elif userprofile.account_type == 2:
				return redirect('shopadmin:menu')
		else:
			return super(AdminLoginRequiredMixin, self).dispatch(request,
																 *args, **kwargs)
