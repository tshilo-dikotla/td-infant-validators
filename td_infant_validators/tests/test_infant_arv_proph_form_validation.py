from django.test import TestCase
from django.utils import timezone
from edc_constants.constants import YES, NO, UNKNOWN
from ..form_validators import InfantArvProphFormValidator


from tshilo_dikotla.constants import MODIFIED, START
from .models import InfantVisit, Appointment, InfantBirthArv
from django.core.exceptions import ValidationError
import td_infant_validators


class TestInfantArvProphForm(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=timezone.now(),
            visit_code='2000',
            visit_instance='0')

        infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

        infantbirtharv = InfantBirthArv.objects.create(
            azt_discharge_supply=YES,
            infant_visit=infant_visit)

        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': infant_visit,
            'prophylatic_nvp': YES,
            'arv_status': MODIFIED,
        }

    def test_validate_taking_arv_proph_unknown(self):
        self.data['prophylatic_nvp'] = UNKNOWN
        self.data['arv_status'] = START
        infant_arv_proph = InfantArvProphFormValidator(
            cleaned_data=self.data)
        infant_arv_proph.infantvisit = 'td_infant_validators.infantvisit'
        infant_arv_proph.infantbirtharv = 'td_infant_validators.infantbirtharv'
        self.assertRaises(ValidationError, infant_arv_proph.validate)
        self.assertIn('prophylatic_nvp',
                      infant_arv_proph._errors.keys())

    def test_validate_taking_arv_proph_no(self):
        """Test if the infant was not taking prophylactic arv
            and arv status is not Not Applicable"""
        self.data['prophylatic_nvp'] = NO
        self.data['arv_status'] = MODIFIED
        infant_arv_proph = InfantArvProphFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, infant_arv_proph.validate)
        self.assertIn('prophylatic_nvp',
                      infant_arv_proph._errors.keys())

#     def test_validate_taking_arv_proph_yes(self):
#         """Test if the infant was not taking prophylactic arv and arv status is Never Started"""
#         self.data['prophylatic_nvp'] = YES
#         self.data['arv_status'] = START
#         infant_arv_proph = InfantArvFormValidator(cleaned_data=self.data)
#         self.assertRaises(ValidationError, infant_arv_proph.validate)
#         self.assertIn('arv_status',
#                       infant_arv_proph._errors.keys())
