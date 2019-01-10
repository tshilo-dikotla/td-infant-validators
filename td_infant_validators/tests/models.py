from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_constants.choices import YES_NO_UNKNOWN_NA
from edc_base.utils import get_utcnow
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)

    visit_instance = models.CharField(max_length=25)


class InfantVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)


class InfantBirthArv(models.Model):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=PROTECT)

    azt_discharge_supply = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN_NA,
        verbose_name="Was the infant discharged with a supply of AZT? ",
        help_text="if infant not yet discharged, please enter 'Not applicable'")


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

    screening_identifier = models.CharField(max_length=50)

    consent_datetime = models.DateTimeField()

    dob = models.DateField()

    version = models.CharField(
        max_length=10,
        editable=False)


class MaternalLabourDel(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    delivery_datetime = models.DateTimeField()


class InfantFuImmunizations(models.Model):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=PROTECT)

    vaccines_received = models.CharField(max_length=25)

    vaccines_missed = models.CharField(max_length=25)


class InfantBirth(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50,
        unique=True)

    dob = models.DateField()


class SubjectScreening(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)

    has_omang = models.CharField(max_length=3)

    age_in_years = age_in_years = models.IntegerField()


class TdConsentVersion(BaseUuidModel):

    subjectscreening = models.ForeignKey(
        SubjectScreening, null=True, on_delete=PROTECT)

    version = models.CharField(max_length=3)

    report_datetime = models.DateField(
        null=True,
        blank=True)


class Foods (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_infant_validators'
        verbose_name = "Foods"
