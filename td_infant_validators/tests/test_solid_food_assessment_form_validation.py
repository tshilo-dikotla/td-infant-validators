from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, OTHER

from ..form_validators import SolidFoodAssessementFormValidator
from .models import Foods, InfantVisit, Appointment


@tag('solidfood')
class TestSolidFoodAssessementFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=get_utcnow(),
            visit_code='2000',
            visit_instance='0')

        self.infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

        self.solid_foods = Foods.objects.create(
            name=OTHER, short_name=OTHER)
        self.solid_foods = Foods.objects.create(
            name="Tsabana", short_name="Tsabana")

        self.options = {'infant_visit': self.infant_visit,
                        'age_solid_food': 7,
                        'solid_foods': Foods.objects.all(),
                        'solid_foods_other': None,
                        'porridge': YES,
                        'porridge_freq': 5,
                        'tsabana': YES,
                        'tsabana_week': 5,
                        'mother_tsabana': YES,
                        'meat': YES,
                        'meat_freq': 5,
                        'potatoes': YES,
                        'potatoes_freq': 5,
                        'carrot_swt_potato': YES,
                        'carrot_swt_potato_freq': 5,
                        'green_veg': YES,
                        'green_veg_freq': 5,
                        'fresh_fruits': YES,
                        'fresh_fruits_freq': 5,
                        'fullcream_milk': YES,
                        'fullcream_milk_freq': 5,
                        'skim_milk': YES,
                        'skim_milk_freq': 5,
                        'raw_milk': YES,
                        'raw_milk_freq': 5,
                        'juice': YES,
                        'juice_freq': 5,
                        'eggs': YES,
                        'eggs_freq': 5,
                        'yogurt': YES,
                        'yogurt_freq': 5,
                        'cheese': YES,
                        'cheese_freq': 5,
                        'rations': YES,
                        'rations_receviced ': '',
                        }

    def test_validate_other_solid_food_assessment_other_specified(self):
        """Test if other is specified if selected other"""
        self.options['solid_foods_other'] = None
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)

    def test_validate_had_any_poridge(self):
        """Test if the child had any porridge"""
        self.options['porridge'] = YES
        self.options['porridge_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('porridge_freq',
                      solid_foods_form._errors.keys())

    def test_validate_had_any_tsabana(self):
        """Test if the child had any tsabana"""
        self.options['tsabana'] = YES
        self.options['tsabana_week'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('tsabana_week',
                      solid_foods_form._errors.keys())

    def test_validate_has_the_child_had_meat_chicken_or_fish(self):
        """Test Since this time yesterday, has this child had any meat, chicken or fish"""
        self.options['meat'] = YES
        self.options['meat_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('meat_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_the_child_had_any_potatoes(self):
        """Test since this time yesterday, has this child had any potatoes"""
        self.options['potatoes'] = YES
        self.options['potatoes_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('potatoes_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_carrot_swt_potato(self):
        """Test if child has had pumpkin, carrot or sweet potato"""
        self.options['carrot_swt_potato'] = YES
        self.options['carrot_swt_potato_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('carrot_swt_potato_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_green_veg(self):
        """Test if child has had green vegetables"""
        self.options['green_veg'] = YES
        self.options['green_veg_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('green_veg_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_fresh_fruits(self):
        """Test child has had fresh fruits"""
        self.options['fresh_fruits'] = YES
        self.options['fresh_fruits_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('fresh_fruits_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_full_cream_milk(self):
        """Test if child has had fullcream milk"""
        self.options['fullcream_milk'] = YES
        self.options['fullcream_milk_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('fullcream_milk_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_skim_milk(self):
        """Test if child has had skim milk"""
        self.options['skim_milk'] = YES
        self.options['skim_milk_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('skim_milk_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_raw_milk(self):
        """Test if child has had raw milk"""
        self.options['raw_milk'] = YES
        self.options['raw_milk_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('raw_milk_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_juice(self):
        """Test if child has had juice"""
        self.options['juice'] = YES
        self.options['juice_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('juice_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_eggs(self):
        """ Test if child has had eggs"""
        self.options['eggs'] = YES
        self.options['eggs_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('eggs_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_yogurt(self):
        """Test if child has had yogurt"""
        self.options['yogurt'] = YES
        self.options['yogurt_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('yogurt_freq',
                      solid_foods_form._errors.keys())

    def test_validate_has_had_cheese(self):
        """Test if child has had cheese"""
        self.options['cheese'] = YES
        self.options['cheese_freq'] = 0
        solid_foods_form = SolidFoodAssessementFormValidator(
            cleaned_data=self.options)
        self.assertRaises(ValidationError, solid_foods_form.validate)
        self.assertIn('cheese_freq',
                      solid_foods_form._errors.keys())
