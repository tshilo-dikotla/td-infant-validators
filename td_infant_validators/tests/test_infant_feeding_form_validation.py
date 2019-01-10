from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.utils import timezone
from datetime import datetime, date
from edc_constants.constants import YES, NO, NOT_APPLICABLE


from ..form_validators import InfantFeedingFormValidator
from .models import InfantVisit, Appointment, InfantFeeding


@tag('1')
class TestInfantFeedingFormValidator(TestCase):

    def setUp(self):

        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=timezone.now(),
            visit_code='2000',
            visit_instance='0')

        self.infantvisit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment,
            report_datetime=timezone.now() - timezone.timedelta(days=5))

        self.infantfeeding = InfantFeeding.objects.create(
            infant_visit=self.infantvisit
        )

        self.options = {
            'infant_visit': self.infantvisit,
            'other_feeding': YES,
            'formula_intro_occur': YES,
            'formula_intro_date': date.today(),
            'took_formula': YES,
            'is_first_formula': YES,
            'date_first_formula': date.today(),
            'est_date_first_formula': YES,
            'water': YES,
            'juice': YES,
            'cow_milk': YES,
            'cow_milk_yes': 'boiled',
            'other_milk': NO,
            'other_milk_animal': None,
            'milk_boiled': NOT_APPLICABLE,
            'fruits_veg': NO,
            'cereal_porridge': NO,
            'solid_liquid': YES,
            'rehydration_salts': NO,
            'water_used': 'Water direct from source',
            'water_used_other': None,
            'ever_breastfeed': YES,
            'complete_weaning': NOT_APPLICABLE,
            'weaned_completely': NO,
            'most_recent_bm': None,
            'times_breastfed': '<1 per week',
            'comments': ''}

    def test_child_received_other_feeding_date_no_date(self):
        """Test that if the child received other feeding, the date the food '
        'was introduced is given"""
        self.options['formula_intro_date'] = None
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantvisit'
        self.assertRaises(ValidationError, forms.validate)

    def test_child_not_received_other_feeding_date_given(self):
        """Test that if the child did not receive other feeding, the date '
        'the food was introduced is not given"""
        self.options['formula_intro_occur'] = NO
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)
