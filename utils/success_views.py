# util/success_views.py
# success message mixins

from django.views.generic.edit import FormView, CreateView, DeleteView, \
    UpdateView


class SuccessMessageMixin(object):
    """
    Adds a success message on successful form submission
    """
    success_message = ""

    def success(self, data):
        """
        Some action was successful, send a message
        """
        success_message = self.get_success_message(data)
        if success_message:
            messages.success(self.request, success_message)

    def get_success_message(self, cleaned_data):
        return self.success_message.format(**cleaned_data)


class SuccessCreateView(SuccessMessageMixin, CreateView):
    """
    Create view with success message
    """

    def form_valid(self, form):
        """
        Add success message when object is successfully created
        """
        self.success(form.cleaned_data)
        return super(SuccessCreateView, self).form_valid(form)


class SuccessUpdateView(SuccessMessageMixin, UpdateView):
    """
    Update view with success message
    """

    def form_valid(self, form):
        """
        Add success message when object is successfully updated
        """
        self.success(form.cleaned_data)
        return super(SuccessUpdateView, self).form_valid(form)


class SuccessDeleteView(SuccessMessageMixin, DeleteView):
    """
    Delete view with success message
    """

    def delete(self, request, *args, **kwargs):
        """
        Add success message when object is successfully celeted
        """
        self.success(self.get_object().__dict__)
        return super(DeleteView, self).delete(request, *args, **kwargs)


class CustomAuthorizationMixin(AccessMixin):
    """
    allows the view to define a custom authorization function

    extends the functionality of django-braces's AccessMixin
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