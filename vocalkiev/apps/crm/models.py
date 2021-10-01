from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class UserFullName(User):
    class Meta:
        proxy = True

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return f"{self.get_full_name()}"


class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', _('ACTIVE')
    INACTIVE = 'INACTIVE', _('INACTIVE')


class PaymentType(models.TextChoices):
    CASH = 'CASH', _('CASH')
    CARD = 'CARD', _('CARD')


class Client(models.Model):
    firstname = models.CharField(_('First name'), blank=True, max_length=64)
    lastname = models.CharField(_('Last name'), blank=True, max_length=64, default='')
    email = models.EmailField(_('Email'), blank=True, default='')
    phone = models.CharField(_('Phone number'), blank=True, max_length=20, default='')
    comment = models.TextField(_('Comment'), max_length=500, blank=True, default='')
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['lastname', 'firstname']

    def get_full_name(self):
        full_name = '%s %s' % (self.firstname, self.lastname)
        return full_name.strip()

    def __str__(self):
        return f"{self.get_full_name()}"


class ClientComment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Client'))
    user = models.ForeignKey(UserFullName, on_delete=models.CASCADE, verbose_name=_('User'))
    comment = models.TextField(_('Comment'), max_length=200, blank=True, default='')
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Client Comment')
        verbose_name_plural = _('Client Comments')

    def __str__(self):
        return f"{self.client}, {self.user}, {self.comment}"


class Place(models.Model):
    name = models.CharField(_('Name'), max_length=64)

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ['name']

    def __str__(self):
        return self.name


class Classroom(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name=_('Place'))
    name = models.CharField(_('Name'), max_length=64)

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')
        ordering = ['place', 'name']

    def __str__(self):
        return f"{self.name}, {self.place}"


class Subject(models.Model):
    name = models.CharField(_('Name'), max_length=64)

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')
        ordering = ['name']

    def __str__(self):
        return self.name


class Subscription(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, primary_key=False, verbose_name=_('Subject'), default=9, related_name='subjects')
    name = models.CharField(_('First name'), max_length=64)
    status = CharField(_('Status'), max_length=10, choices=Status.choices, default=Status.ACTIVE)
    price = models.FloatField(_('Price'), blank=True, default=000)
    percentage = models.FloatField(_('Percentage'), blank=True, default=000)
    lessons_qty = models.IntegerField(_('lessons_qty'), default=0)  # number of lessons per subscription
    percentage_if_absent = models.FloatField(_('Percentage if absent'), blank=True, default=000)  # percentage when the student does not appear
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ['name']

    def __str__(self):
        return str(self.price) + '-' + str(self.name)


class ClientSubscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name=_('Subscription'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_('Client'))
    teacher = models.ForeignKey(UserFullName, on_delete=models.CASCADE, verbose_name=_('Teacher'))
    status = CharField(_('Status'), max_length=10, choices=Status.choices, default=Status.ACTIVE)
    comment = models.TextField(_('Comment'), max_length=500, blank=True)
    payment_type = CharField(_('Payment type'), max_length=10, choices=PaymentType.choices)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('User subscription')
        verbose_name_plural = _('Users subscriptions')

    def __str__(self):
        return str(self.client) + ' - ' + str(self.subscription)


class Lesson(models.Model):
    client_subscription = models.ForeignKey(ClientSubscription, on_delete=models.CASCADE, verbose_name=_('User subscription'))
    teacher = models.ForeignKey(UserFullName, on_delete=models.CASCADE, verbose_name=_('Teacher'))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_('Classroom'))
    datetime = models.DateTimeField(_('Time of the event'))
    status = CharField(_('Status'), max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')
        ordering = ['datetime']

    def __str__(self):
        return f"{self.client_subscription.client.get_full_name()}, {self.teacher}, {self.classroom}, {self.datetime.strftime('%Y-%m-%d %H:%M')}"


class LessonComment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name=_('Lesson'))
    user = models.ForeignKey(UserFullName, on_delete=models.CASCADE, verbose_name=_('User'))
    comment = models.TextField(_('Comment'), max_length=500, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Lesson comment')
        verbose_name_plural = _('Lesson comments')
        ordering = ['lesson', 'user']

    def __str__(self):
        return str(self.lesson)


class Payment(models.Model):
    client_subscription = models.ForeignKey(ClientSubscription, on_delete=models.CASCADE, verbose_name=_('User subscription'))
    admin = models.ForeignKey(UserFullName, on_delete=models.CASCADE, verbose_name=_('Admin'))
    payment_type = CharField(_('Payment type'), max_length=10, choices=PaymentType.choices)
    amount = models.FloatField(_('Amount'), blank=True, default=000)
    comment = models.TextField(_('Comment'), max_length=200, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
