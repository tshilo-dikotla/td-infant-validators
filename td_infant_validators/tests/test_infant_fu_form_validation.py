from django.test import TestCase
from dateutil.relativedelta import relativedelta
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import InfantVisit, Appointment
from ..form_validators import InfantFuFormValidator


class TestInfantFuFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=timezone.now(),
            visit_code='2000',
            visit_instance='0')

        self.infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

        self.options = {
            'current_hiv_status': POS,
            'evidence_hiv_status': YES,
            'will_get_arvs': YES,
            'is_diabetic': NO,
            'will_remain_onstudy': YES,
            'rapid_test_done': NOT_APPLICABLE,
            'last_period_date': (
                timezone.datetime.now() - relativedelta(weeks=25)).date()
        }

    def test_infant_hospitalization(self):
        self.options['infant_birth'] = self.infant_visit.id
        self.options['was_hospitalized'] = YES
        infant_fu = InfantFuFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, infant_fu.validate)

    def test_validate_hospitalization_duration(self):
        self.options['infant_birth'] = self.infant_visit.id
        self.options['was_hospitalized'] = YES
        self.options['days_hospitalized'] = 100
        infant_fu = InfantFuFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, infant_fu.validate)