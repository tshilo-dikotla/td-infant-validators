from django.test import TestCase
from django.utils import timezone
from edc_constants.constants import YES, NO
from ..form_validators import InfantArvFormValidator


from tshilo_dikotla.constants import MODIFIED, NEVER_STARTED
from .models import InfantVisit, Appointment


class TestInfantArvProphForm(TestCase):

    def setUp(self):
        self.appointment = Appointment(
            subject_identifier='23344',
            appt_datetime=timezone.now(),
            visit_code='2000')
        self.infant_visit = InfantVisit(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'prophylatic_nvp': YES,
            'arv_status': MODIFIED,
        }

    def test_validate_taking_arv_proph_unknown(self):
        pass

    def test_validate_taking_arv_proph_no(self):
        """Test if the infant was not taking prophylactic arv
            and arv status is not Not Applicable"""
        self.data['prophylatic_nvp'] = NO
        self.data['arv_status'] = MODIFIED
        infant_arv_proph = InfantArvFormValidator(cleaned_data=self.data)
        self.assertIn('Infant was not taking prophylactic arv, prophylaxis should be Never Started or Discontinued.',
                      infant_arv_proph.errors.get('__all__'))

    def test_validate_taking_arv_proph_yes(self):
        """Test if the infant was not taking prophylactic arv and arv status is Never Started"""
        self.data['prophylatic_nvp'] = YES
        self.data['arv_status'] = NEVER_STARTED
        infant_arv_proph = InfantArvFormValidator(cleaned_data=self.data)
        self.assertIn(u'Infant has been on prophylactic arv, cannot choose Never Started or Permanently discontinued.',
                      infant_arv_proph.errors.get('__all__'))
