from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_constants.constants import ALIVE
from edc_base.utils import get_utcnow
from django.utils import timezone


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)


class InfantVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)


class InfantArvProph(models.Model):
    pass
