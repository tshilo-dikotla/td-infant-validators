from django.core.exceptions import ValidationError
from django.test import TestCase, tag

from ..constants import TUBE
from ..form_validators import InfantRequisitionFormValidator
from .models import Panel


class TestInfantRequisitionFormValidator(TestCase):

    def test_dna_pcr_item_type_valid(self):
        cleaned_data = {
            'panel': Panel.objects.create(name='dna_pcr'),
            'item_type': 'dbs'}
        form_validator = InfantRequisitionFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_dna_pcr_item_type_invalid(self):
        cleaned_data = {
            'panel': Panel.objects.create(name='dna_pcr'),
            'item_type': TUBE}
        form_validator = InfantRequisitionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('item_type',
                      form_validator._errors.keys())
