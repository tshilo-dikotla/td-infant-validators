from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_constants.constants import ALIVE
from edc_base.utils import get_utcnow
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)


class InfantVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)


class InfantArvProph(models.Model):
    pass


class InfantFuPhysical(models.Model):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=PROTECT)

    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,)

    head_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=2,)


class RegisteredSubject(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50,
        unique=True)

    relative_identifier = models.CharField(
        max_length=36,
        null=True,
        blank=True)


class MaternalConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    consent_datetime = models.DateTimeField()

    dob = models.DateField()


class InfantFuImmunizations(models.Model):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=PROTECT)

    vaccines_received = models.CharField(max_length=25)

    vaccines_missed = models.CharField(max_length=25)


class InfantBirth(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50,
        unique=True)

    dob = models.DateField()
