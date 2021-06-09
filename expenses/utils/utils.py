from expenses import settings
from expenses.utils.tokens import default_token_generator
from django.template import loader
from django.core.mail import (
    EmailMultiAlternatives,
    EmailMessage
)
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode
)
from django.utils.encoding import (
    force_bytes,
    force_text
)


def encode_uid(pk):
    return urlsafe_base64_encode(force_bytes(pk))


def decode_uid(pk):
    return force_text(urlsafe_base64_decode(pk))


class UserEmailFactoryBase(object):
    token_generator = default_token_generator
    subject_template_name = None
    plain_body_template_name = None
    html_body_template_name = None

    def __init__(self, from_email, user, site_name, **context):
        self.from_email = from_email
        self.user = user
        self.site_name = site_name
        self.context_data = context

    @classmethod
    def from_request(cls, request, user=None, from_email=None, **context):
        from_email = from_email or getattr(
            settings, 'DEFAULT_FROM_EMAIL', ''
        )

        return cls(
            from_email=from_email,
            user=user or request.user,
            site_name=settings.APPLICATION_NAME,
            **context
        )

    def create(self):
        assert self.plain_body_template_name or self.html_body_template_name
        context = self.get_context()
        subject = loader.render_to_string(self.subject_template_name, context)
        subject = ''.join(subject.splitlines())

        if self.plain_body_template_name:
            plain_body = loader.render_to_string(
                self.plain_body_template_name, context
            )
            email_message = EmailMultiAlternatives(
                subject, plain_body, self.from_email,
                [self.user.email if hasattr(self.user, 'email') else '']
            )
            email_message.attach_alternative(plain_body, "text/html")
            if self.html_body_template_name:
                html_body = loader.render_to_string(
                    self.html_body_template_name, context
                )
                email_message.attach_alternative(html_body, "text/html")
        else:
            html_body = loader.render_to_string(
                self.html_body_template_name, context
            )
            email_message = EmailMessage(
                subject, html_body, self.from_email,
                [self.user.email if hasattr(self.user, 'email') else '']
            )
            email_message.content_subtype = 'html'
        return email_message

    def get_context(self):
        if type(self.user) != str and self.user.id:
            self.user_uid = encode_uid(self.user.pk)
            self.user_token = self.token_generator.make_token(self.user)
        else:
            self.user_uid = None
            self.user_token = None
        context = {
            'user': self.user,
            'email': self.user.email if hasattr(self.user, 'email') else '',
            'site_name': self.site_name,
            'uid': self.user_uid,
            'token': self.user_token,
        }
        context.update(self.context_data)
        return context


class UserConfirmationEmailFactory(UserEmailFactoryBase):
    subject_template_name = 'confirmation_email_subject.html'
    plain_body_template_name = 'confirmation_email_body.html'


class UserPasswordResetEmailFactory(UserEmailFactoryBase):
    subject_template_name = 'password_reset_email_subject.html'
    plain_body_template_name = 'password_reset_email_body.html'


class UserPasswordChangedEmailFactory(UserEmailFactoryBase):
    subject_template_name = 'password_changed_email_subject.html'
    plain_body_template_name = 'password_changed_email_body.html'


class ExpensesReminderEmailFactory(UserEmailFactoryBase):
    subject_template_name = 'reminder_email_subject.html'
    plain_body_template_name = 'reminder_email_body.html'


class ActionViewMixin(object):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer)
