from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from edc_constants.constants import YES, NO, UNKNOWN

from ..constants import MODIFIED, START
from ..form_validators import InfantBirthDataFormValidator
from .models import InfantVisit, Appointment, InfantBirthArv


class TestInfantBirthFeedingVaccineForm(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=timezone.now(),
            visit_code='2000',
            visit_instance='0')

        infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

        InfantBirthArv.objects.create(
            azt_discharge_supply=YES,
            infant_visit=infant_visit)

        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': infant_visit,
            'prophylatic_nvp': YES,
            'arv_status': MODIFIED,
        }