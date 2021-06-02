from django.utils.translation import ugettext_lazy as _

USER_ALREADY_EXIST = _('Account with this email already exists.')
PASSWORD_MISMATCH_ERROR = _('Passwords do not match or empty.')
PASSWORD_REQUIREMENTS_ERROR = _("Use 8 or more characters with a mix of numbers, uppercase and lowercase letters.")

INVALID_TOKEN_ERROR = _('Invalid token for given user.')
INVALID_UID_ERROR = _('Invalid user id or user doesn\'t exist.')
INVALID_PASSWORD_ERROR = _('Invalid password')
EMAIL_NOT_FOUND = _('User with given email does not exist.')
STALE_TOKEN_ERROR = _('Stale token for given user.')
INVALID_CREDENTIALS_ERROR = _('The email or password is incorrect.')
MUST_INCLUDE_PASSWORD_ERROR = _('Must include "password" and "retype_password" fields.')


USER_ALREADY_ACTIVE = _('Account with this email is already active.')
USER_SOFT_DELETED = _("Account with this email is deactivated. Go to 'restore account' to activate")
NOT_ALLOW_TO_ADD_WORKBLOCKS_USER = _('Sorry, workblocks user can not be added to your referrals.')
NOT_ALLOW_TO_ADD_SUPPORT_USER = _('Sorry, support user can not be added to your referrals.')
NOT_ALLOW_TO_ADD_REFERRALS = _('Unable to add user at this time.')
NOT_ALLOW_TO_ADD_THIS_USER = _('Sorry, You are not able to add this user until there registration id will be '
                               'checked by our administrator.')
USER_REG_ID_ALREADY_EXIST = _('User with given registration ID already exist.')
MAX_PROMO_REG_ID_EXCEED = _('Max allowed promo ids exceed.')
CANT_RESTORE_USER_REG_ID_ALREADY_EXIST = _(
    'User with given registration ID already exist, so deleted user can not be restored.')
REPORT_TYPE_ERROR = _('Report type field is not correct. Should be 1, 2, 3 or 4.')
REPORT_NEWS_TYPE_ERROR = _('Report type field is not correct. Should be 1 or 2.')
SUPPORT_CHAT_MESSAGE_BUSINESS_ID_REQUIRED = "To continue as a %s, Workblocks requires an active Business ID Number. " \
                                            "Once verified, your full account will be active. Reply with valid " \
                                            "Business ID Number."
SUPPORT_CHAT_MESSAGE_FULLY_ACTIVE = _("Your account is now fully active.")
WORKBLOCKS_CHAT_MESSAGE_FULLY_ACTIVE = _(
    "Thanks for joining! Have a question or suggestion, drop us a line, we are here to help.")
WORKBLOCKS_USER_ALREADY_EXIST = _("Workblocks user already exist.")
SUPPORT_USER_ALREADY_EXIST = _("Support user already exist.")
