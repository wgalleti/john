from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.managers import UsuarioManager

from django.contrib.auth.models import User


class Usuario1(AbstractUser):
    GATEC = 1
    SAPIENS = 2
    OUTROS = 3

    APP = (
        (GATEC, 'Gatec'),
        (SAPIENS, 'Sapiens'),
        (OUTROS, 'Outros'),
    )
    app = models.IntegerField(_('app'), default=3, choices=APP)
    password_app = models.CharField(_('password app'), max_length=100, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Usuario(AbstractBaseUser, PermissionsMixin):
    GATEC = 1
    SAPIENS = 2
    OUTROS = 3

    APP = (
        (GATEC, 'Gatec'),
        (SAPIENS, 'Sapiens'),
        (OUTROS, 'Outros'),
    )

    name = models.CharField(_('first name'), max_length=30, blank=True)
    app = models.IntegerField(_('app'), default=3, choices=APP)
    password_app = models.CharField(_('password app'), max_length=100, blank=True, null=True)

    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="groups_user",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="permissions_user",
        related_query_name="user",
    )

    objects = UsuarioManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['app']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % self.name
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
