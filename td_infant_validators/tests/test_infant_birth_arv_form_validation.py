from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from django.utils import timezone
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NOT_APPLICABLE

from ..form_validators import InfantBirthArvFormValidator
from .models import InfantVisit, Appointment


class TestInfantBirthArvFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=timezone.now(),
            visit_code='2000',
            visit_instance='0')

        self.infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

    @tag('arv')
    def test_azt_after_birth_yes_azt_dose_date_required(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': YES,
            'azt_dose_date': None
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('azt_dose_date', form_validator._errors)

    def test_azt_after_birth_yes_azt_dose_date_provided(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': YES,
            'azt_dose_date': get_utcnow().date()
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unepectedly. Got{e}')

    def test_azt_after_birth_no_azt_dose_date_invalid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': NO,
            'azt_dose_date': get_utcnow().date()
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('azt_dose_date', form_validator._errors)

    def test_azt_after_birth_no_azt_dose_date_none_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': NO,
            'azt_dose_date': None
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unepectedly. Got{e}')

    def test_azt_after_birth_yes_azt_additional_dose_na_invalid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': YES,
            'azt_dose_date': get_utcnow().date(),
            'azt_additional_dose': NOT_APPLICABLE
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('azt_additional_dose', form_validator._errors)

    def test_azt_after_birth_yes_azt_additional_dose_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': YES,
            'azt_dose_date': get_utcnow().date(),
            'azt_additional_dose': 'Unknown'
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unepectedly. Got{e}')

    def test_azt_after_birth_no_azt_additional_dose_invalid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': NO,
            'azt_dose_date': None,
            'azt_additional_dose': 'Unknown'
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('azt_additional_dose', form_validator._errors)

    def test_azt_after_birth_no_azt_additional_dose_na_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'azt_after_birth': NO,
            'azt_dose_date': None,
            'azt_additional_dose': NOT_APPLICABLE
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unepectedly. Got{e}')

    def test_sdnvp_after_birth_yes_nvp_dose_date_required(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'sdnvp_after_birth': YES,
            'nvp_dose_date': None
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('nvp_dose_date', form_validator._errors)

    def test_sdnvp_after_birth_yes_nvp_dose_date_provided(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'sdnvp_after_birth': YES,
            'nvp_dose_date': get_utcnow().date()
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unepectedly. Got{e}')

    def test_sdnvp_after_birth_no_nvp_dose_date_invalid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'sdnvp_after_birth': NO,
            'nvp_dose_date': get_utcnow().date()
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('nvp_dose_date', form_validator._errors)

    def test_sdnvp_after_birth_no_nvp_dose_date_none_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'sdnvp_after_birth': NO,
            'nvp_dose_date': None
        }
        form_validator = InfantBirthArvFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unepectedly. Got{e}')
