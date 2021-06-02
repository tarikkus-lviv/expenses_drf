from __future__ import unicode_literals

import gzip
import os
import re
from difflib import SequenceMatcher

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _, ungettext
from six import string_types


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator['NAME'])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your CUSTOM_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator['NAME'])
        validators.append(klass(**validator.get('OPTIONS', {})))

    return validators


# @lru_cache.lru_cache(maxsize=None)
def get_custom_password_validators():
    return get_password_validators(settings.CUSTOM_PASSWORD_VALIDATORS)


def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_custom_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)


class MinimumLengthValidator(object):
    """
    Validate whether the password is of a minimum length.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ungettext(
                    "This password is too short. It must contain at least %(min_length)d character.",
                    "This password is too short. It must contain at least %(min_length)d characters.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ungettext(
            "Your password must contain at least %(min_length)d character.",
            "Your password must contain at least %(min_length)d characters.",
            self.min_length
        ) % {'min_length': self.min_length}


class UserAttributeSimilarityValidator(object):
    """
    Validate whether the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, string_types):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = force_text(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("The password is too similar to the %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("Your password can't be too similar to your other personal information.")


class CommonPasswordValidator(object):
    """
    Validate whether the password is a common password.

    The password is rejected if it occurs in a provided list, which may be gzipped.
    The list Django ships with contains 1000 common passwords, created by Mark Burnett:
    https://xato.net/passwords/more-top-worst-passwords/
    """
    DEFAULT_PASSWORD_LIST_PATH = os.path.join(
        os.path.dirname(os.path.realpath(os.path.abspath(__file__))), 'common-passwords.txt'
    )

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path) as f:
                common_passwords_lines = f.read().decode('utf-8').splitlines()
        except IOError:
            with open(password_list_path) as f:
                common_passwords_lines = f.readlines()

        self.passwords = {p.strip() for p in common_passwords_lines}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("This password is too common."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Your password can't be a commonly used password.")


class NumericPasswordValidator(object):
    """
    Validate whether the password is alphanumeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Your password can't be entirely numeric.")


class OneNumberAtLeastPasswordValidator(object):
    """
    Validate whether the password has at least one number.
    """

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("This password have no numbers."),
                code='password_have_no_numbers',
            )

    def get_help_text(self):
        return _("Your password must have at least one number.")


class SymbolPasswordValidator(object):
    """
    Validate whether the password has at least one number.
    """

    def validate(self, password, user=None):
        symbols = ['$', '#', '@', '!', '*']
        if not any(char in symbols for char in password):
            raise ValidationError(
                _("This password have no symbols."),
                code='password_have_no_symbols',
            )

    def get_help_text(self):
        return _("Your password must have at least one symbol.")


class OneBigLetterAtLeastPasswordValidator(object):
    """
    Validate whether the password has at least one big letter.
    """

    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("This password have no uppercase letters."),
                code='password_have_no_uppercase_letters',
            )

    def get_help_text(self):
        return _("Your password must have at least one uppercase letter.")
