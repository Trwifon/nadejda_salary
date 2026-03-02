from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from nadejda_salary.mixins import ReadonlyViewMixin

UserModel = get_user_model()


class ProfileBaseForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        help_text='Въведете потребителско име',
        widget=forms.TextInput(attrs={'placeholder': 'Потребителско име'}))

    first_name = forms.CharField(
        max_length=30,
        help_text='Въведете име',
        widget=forms.TextInput(attrs={'placeholder': 'Име'}))

    last_name = forms.CharField(
        max_length=30,
        help_text='Въведете фамилия',
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileCreateForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        help_text= 'Потребителското име трябва да съдържа само букви и цифри',
        widget=forms.TextInput(attrs={'placeholder': 'Потребитеслко име'}))

    email = forms.EmailField(
        help_text='Въведете Вашия имейл',
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = UserModel
        fields = ('username', 'email')


class ProfileUpdateForm(ProfileBaseForm):
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}),
        help_text='Enter your current password to change it')

    new_password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
        help_text='Enter new password')

    new_password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat new password'}),
        help_text='Repeat new password')

    def clean(self):
        cleaned_data = super().clean()
        new1 = cleaned_data.get('new_password1')
        new2 = cleaned_data.get('new_password2')
        current = cleaned_data.get('current_password')

        # If any new-password field is filled, require current password
        if new1 or new2:
            if not current:
                raise ValidationError('Current password is required to change password.')

            # verify current password is correct
            if not self.instance.check_password(current):
                raise ValidationError('Current password is incorrect.')

            # ensure new passwords match
            if new1 != new2:
                raise ValidationError('The two new password fields didn\'t match.')

            # validate new password with Django validators
            try:
                password_validation.validate_password(new1, self.instance)
            except ValidationError as e:
                raise ValidationError(e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new1 = self.cleaned_data.get('new_password1')
        if new1:
            user.set_password(new1)
        if commit:
            user.save()
        return user


class DeleteUserForm(ReadonlyViewMixin, ProfileBaseForm):
    read_only_fields = ('username', 'first_name', 'last_name')

    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name')