from registration.backends.default.views import RegistrationView
from .forms import UserProfileRegistrationForm
from .models import UserProfile

class MyRegistrationView(RegistrationView):
    form_class = UserProfileRegistrationForm

    def get_success_url(self, user):
        return '/'

    def register(self, form_class):
        new_user = super(MyRegistrationView, self).register(form_class)
        user_profile = UserProfile()
        new_user.is_active = True
        new_user.save()
        user_profile.user = new_user
        
        user_profile.firstname_field = form_class.cleaned_data['firstname_field']
        user_profile.lastname_field = form_class.cleaned_data['lastname_field']
        user_profile.intro = form_class.cleaned_data['intro']
        user_profile.photo_url = form_class.cleaned_data['photo_url']
        user_profile.location = form_class.cleaned_data['location']
        user_profile.save()
        return new_user