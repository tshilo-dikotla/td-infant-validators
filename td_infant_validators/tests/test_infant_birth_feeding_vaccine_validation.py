from django.test import TestCase
from django.utils import timezone
from edc_constants.constants import YES

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
