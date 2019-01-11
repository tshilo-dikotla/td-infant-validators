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
            infant_visit=self.infantvisit,
            formula_intro_date=timezone.now()
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
            'comments': '',
            'report_datetime': timezone.now()}

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

    def test_infant_formula_feeding_YES(self):
        """"Test if the child took formula, the field for whether this is the first reporting in not N/A"""
        self.options['is_first_formula'] = None
        self.options['took_formula'] = YES
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_infant_formula_feeding_not_yes(self):
        """Test if the child did not take formula, the field for whether this is the first reporting is N/A not YES"""
        self.options['took_formula'] = NO
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_infant_formula_feeding_not_yes_date_provided(self):
        """Test if the child did not take formula, the field for whether this is the first reporting is N/A not None"""
        self.options['took_formula'] = NO
        self.options['is_first_formula'] = None
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_infant_formula_feeding_not_yes_est_date_provided(self):
        """Test if the child did not take formula, the date of estimated first formula use is not provided"""
        self.options['took_formula'] = NO
        self.options['is_first_formula'] = None
        self.options['date_first_formula'] = None
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_is_first_formula_yes_no_date(self):
        """Test that if this is the first reporting of infant formula,'
        ' the date should be provided"""
        self.options['date_first_formula'] = None
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_is_first_formula_yes_date_estimated_field_none(self):
        """Test that if this is the first reporting of infant formula, whether the date is estimated should be indicated"""
        self.options['date_first_formula'] = NO
        self.options['est_date_first_formula'] = None
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_is_first_formula_no_date_provided(self):
        """Test that if this is not the first reporting of infant formula, the date should not be provided"""
        self.options['is_first_formula'] = NO
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_is_first_formula_no_date_estimated_given(self):
        """Test that if this is not the first reporting of infant formula, whether the date is estimated should not
           be indicated"""
        self.options['is_first_formula'] = NO
        self.options['date_first_formula'] = None
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_took_cow_milk_yes(self):
        """test that if the infant received cow milk, the field question13 should not be N/A"""
        self.options['cow_milk_yes'] = NOT_APPLICABLE
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_took_cow_milk__not_yes(self):
        """test that if the infant did not receive cow milk, the field question13 should be N/A"""
        self.options['cow_milk'] = NO
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_took_milk_other_yes_animal_not_specified(self):
        """Test that if the infant took milk from another animal, that animal is specified"""
        self.options['other_milk'] = YES
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_took_milk__yes_milk_boiled_not_applicable(self):
        """Test that if the infant took milk from another animal, the answer to Question16 is not N/A"""
        self.options['other_milk'] = YES
        self.options['other_milk_animal'] = 'Goat'
        self.options['milk_boiled'] = NOT_APPLICABLE
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_took_milk_other_not_yes_animal_specified(self):
        """Test that if the infant did not take milk from another animal, that animal is not specified"""
        self.options['other_milk_animal'] = 'Goat'
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_took_milk_other_not_yes_boiled_not_not_applicable(self):
        """Test that if the infant did not take milk from another animal, the answer to question 16 is N/A"""
        self.options['milk_boiled'] = YES
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_child_breastfed_complete_weaning_not_not_applicable(self):
        """Test that if the infant has been breast fed since the last visit, the answer to question24 is N/A"""
        self.options['complete_weaning'] = NO
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    def test_child_not_breastfed_complete_weaning_not_applicable(self):
        """Test that if the child has not been breast fed since the last visit, the answer to question24 should not be
        NA"""
        self.options['ever_breastfeed'] = NO
        self.options['complete_weaning'] = NOT_APPLICABLE
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)

    @tag('2')
    def test_formula_intro_occur_yes_no_foods_indicated(self):
        self.options['juice'] = NO
        self.options['cow_milk'] = NO
        self.options['cow_milk_yes'] = NOT_APPLICABLE
        self.options['other_milk'] = NO
        self.options['fruits_veg'] = NO
        self.options['cereal_porridge'] = NO
        self.options['solid_liquid'] = NO
        forms = InfantFeedingFormValidator(cleaned_data=self.options)
        forms.infantfeeding = 'td_infant_validators.infantfeeding'
        forms.infant_visit = 'td_infant_validators.infantfeeding'
        self.assertRaises(ValidationError, forms.validate)
#         self.assertIn("You should answer YES on either one of the questions about the juice, cow_milk, other milk, "
#                       "fruits_veg, cereal_porridge or solid_liquid", forms.errors.get('__all__'))
