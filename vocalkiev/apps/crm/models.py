from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.utils.translation import gettext_lazy as _


class User(AuthUser):
    class Meta:
        proxy = True
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()


class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', _('ACTIVE')
    INACTIVE = 'INACTIVE', _('INACTIVE')


class PaymentType(models.TextChoices):
    CASH = 'CASH', _('CASH')
    CARD = 'CARD', _('CARD')


class Model(models.Model):
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    creator = models.ForeignKey(
        User,
        models.CASCADE,
        related_name="%(app_label)s_%(class)s_related"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(Model):
    first_name = models.CharField(blank=True, max_length=64)
    last_name = models.CharField(blank=True, max_length=64, default='')
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True, max_length=20)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()


class ClientComment(Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200, blank=True, default='')

    class Meta:
        verbose_name = _('Client Comment')
        verbose_name_plural = _('Client Comments')

    def __str__(self):
        dt = self.created_at.strftime('%d.%m.%Y %H:%M')
        return f"{dt} {self.creator}: {self.comment}"


class Place(Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')

    def __str__(self):
        return self.name


class Classroom(Model):
    place = models.ForeignKey(Place, models.CASCADE)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')

    def __str__(self):
        return f"{self.place} {self.name}"


class Subject(Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return self.name


class Subscription(Model):
    subject = models.ForeignKey(Subject, models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    lessons_qty = models.IntegerField(default=0)
    percentage_if_absent = models.FloatField(default=0)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')

    def __str__(self):
        return f"{self.subject} {self.name} ({self.price}{_('uah')})"


class ClientSubscription(Model):
    subscription = models.ForeignKey(Subscription, models.CASCADE)
    client = models.ForeignKey(Client, models.CASCADE)
    teacher = models.ForeignKey(User, models.CASCADE, related_name='subscription_teacher')
    comment = models.TextField(max_length=500, blank=True)
    payment_type = models.CharField(max_length=10, choices=PaymentType.choices)

    class Meta:
        verbose_name = _('Client Subscription')
        verbose_name_plural = _('Client Subscriptions')

    def __str__(self):
        return f"{self.client}, {self.subscription}"


class Lesson(Model):
    client_subscription = models.ForeignKey(ClientSubscription, models.CASCADE)
    teacher = models.ForeignKey(User, models.CASCADE, related_name='lesson_teacher')
    classroom = models.ForeignKey(Classroom, models.CASCADE)
    datetime = models.DateTimeField(_('Time of the event'))
    is_passed = models.BooleanField(_('Is passed'), default=False)

    class Meta:
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __str__(self):
        client = self.client_subscription.client
        dt = self.datetime.strftime('%d.%m.%Y %H:%M')
        return f"{client} / {self.teacher}, {self.classroom}, {dt}"


class LessonComment(Model):
    lesson = models.ForeignKey(Lesson, models.CASCADE)
    comment = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = _('Lesson comment')
        verbose_name_plural = _('Lesson comments')

    def __str__(self):
        dt = self.created_at.strftime('%d.%m.%Y %H:%M:%S')
        return f"{dt} {self.creator}: {self.comment}"


class Payment(Model):
    client_subscription = models.ForeignKey(ClientSubscription, models.CASCADE)
    payment_type = models.CharField(max_length=10, choices=PaymentType.choices)
    amount = models.FloatField(blank=True, default=000)
    comment = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
