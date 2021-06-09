from django.contrib import admin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as UA
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from users.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active')


class UserAdmin(UA):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['id', 'role', 'full_name', 'email', 'phone_number', 'image', 'is_active', 'is_draft',
                    'is_receiving_notifications']

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info',
         {'fields': ('full_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': (('role', 'is_active', 'is_draft', 'is_receiving_notifications'),)}),
        ('Important dates', {'fields': (('last_login', 'created'),)}),
    )
    ordering = ['-created']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )
    search_fields = ['email', 'full_name']
    list_filter = ('is_active', 'is_draft')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
