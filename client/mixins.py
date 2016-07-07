from LaundryBear.mixins import LoginRequiredMixin


class ClientLoginRequiredMixin(LoginRequiredMixin):
    login_view_name = 'client:login'
