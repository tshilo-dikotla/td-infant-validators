from django.test import TestCase
from dateutil.relativedelta import relativedelta
from edc_constants.constants import YES, NO, NOT_APPLICABLE, POS
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import InfantVisit, Appointment


class TestInfantFuFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=timezone.now(),
            visit_code='2000',
            visit_instance='0')

        infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

        self.registered_subject = self.maternal_eligibility.registered_subject

        self.options = {'registered_subject': self.registered_subject,
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
            infant_fu = TestInfantFuFormValidator(cleaned_data=self.options)
            self.assertRaises(ValidationError, infant_fu.validate)
#             self.assertIn(
#                 'If infant was hospitalized, please provide # of days hospitalized',
#                 infant_fu.errors.get('__all__'))

    def test_validate_hospitalization_duration(self):
        self.options['infant_birth'] = self.infant_visit.id
        self.options['was_hospitalized'] = YES
        self.options['days_hospitalized'] = 100
        infant_fu = TestInfantFuFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, infant_fu.validate)
#         self.assertIn(
#             'days hospitalized cannot be greater than 90days',
#             infant_fu.errors.get('__all__'))
