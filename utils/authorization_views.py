# utils/authorization_views.py
# custom authorization


class CustomAuthorizationMixin(AccessMixin):
    """
    allows the view to define a custom authorization function
    """

    def is_authorized(self):
        """
        authorization function
        obviously subclasses should override this
        """
        return True

    def dispatch(self, request, *args, **kwargs):
        if self.is_authorized():
            return super(CustomAuthorizationMixin, self).dispatch(request,
                *args, **kwargs)
        else:
            if self.raise_exception:
                raise PermissionDenied  # return a forbidden response
            else:
                return redirect_to_login(request.get_full_path(),
                    self.get_login_url(), self.get_redirect_field_name())