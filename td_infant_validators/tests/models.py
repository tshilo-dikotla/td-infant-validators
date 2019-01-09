from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_constants.choices import YES_NO_UNKNOWN_NA
from edc_base.utils import get_utcnow


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
