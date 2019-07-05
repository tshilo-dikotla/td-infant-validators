from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from ..form_validators import InfantRequisitionFormValidator
from .models import Panel, InfantVisit, Appointment


@tag('req')
class TestInfantRequisitionFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=get_utcnow(),
            visit_code='2000',
            visit_instance='0')

        self.infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

    def test_dna_pcr_item_type_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
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
            'infant_visit': self.infant_visit,
            'panel': Panel.objects.create(name='infant_insulin'),
            'item_type': 'dbs'}
        form_validator = InfantRequisitionFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('item_type',
                      form_validator._errors.keys())
