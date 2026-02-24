from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Ensures the user is an Administrator (Superuser or Staff).
    Redirects to the appropriate dashboard if unauthorized.
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # If logged in but not admin, let the dispatch view handle redirection
            return redirect('login_dispatch')
        # If not logged in, redirect to login
        return super().handle_no_permission()

class SupplierRequiredMixin(UserPassesTestMixin):
    """
    Ensures the user is a Supplier.
    Redirects to the appropriate dashboard if unauthorized.
    """
    def test_func(self):
        return self.request.user.groups.filter(name='PROVEEDOR').exists() or hasattr(self.request.user, 'proveedor')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # If logged in but not supplier, let the dispatch view handle redirection
            return redirect('login_dispatch')
        return super().handle_no_permission()
