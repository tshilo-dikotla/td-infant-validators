from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.utils import timezone
from edc_constants.constants import YES, OTHER

from ..form_validators import InfantFuNewMedItemsFormValidator


class Medication:

    new_medications = YES


@tag('infantfuitems')
class TestInfantFuNewMedItemsFormValidator(TestCase):

    def setUp(self):
        med = Medication()
        self.data = {
            'infant_fu_med': med,
            'medication': None,
            'other_medication': None,
            'stop_date': timezone.now() - timezone.timedelta(days=2),
            'date_first_medication': timezone.now()
        }

    def test_medication_not_specified(self):
        infant_fu_new_items = InfantFuNewMedItemsFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, infant_fu_new_items.validate)

    def test_other_medication_not_specified(self):
        self.data['medication'] = OTHER
        self.data['other_medication'] = None
        infant_fu_new_items = InfantFuNewMedItemsFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, infant_fu_new_items.validate)
