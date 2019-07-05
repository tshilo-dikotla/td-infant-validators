from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import VaccinesMissedFormValidator
from .models import Appointment, InfantVisit, InfantFuImmunizations


@tag('missed')
class TestVaccinesMissedFormValidator(TestCase):

    def setUp(self):
        subject_identifier = '22334'
        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')
        self.infant_visit = InfantVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)
        self.infant_fu_immunizations = InfantFuImmunizations.objects.create(
            infant_visit=self.infant_visit,
            vaccines_received=NO,
            vaccines_missed=YES)

    def test_infant_fu_immunization_vaccine_missed_yes_name_required(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': None,
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('missed_vaccine_name', form_validator._errors)

    def test_infant_fu_immunization_vaccine_missed_yes_name_given(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': 'Polio',
            'reason_missed': 'missed scheduled vaccination',
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unexpectedly. Got{e}')

    def test_infant_fu_immunization_vaccine_missed_no_name_invalid(self):
        self.infant_fu_immunizations.vaccines_missed = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': 'Polio',
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('missed_vaccine_name', form_validator._errors)

    def test_infant_fu_immunization_vaccine_missed_no_name_none(self):
        self.infant_fu_immunizations.vaccines_missed = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': None,
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unexpectedly. Got{e}')

    def test_missed_vaccine_name_given_reason_required(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': 'Polio',
            'reason_missed': None
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_missed', form_validator._errors)

    def test_missed_vaccine_name_given_reason_provided(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': 'Polio',
            'reason_missed': 'missed scheduled vaccination',
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unexpectedly. Got{e}')

    def test_missed_vaccine_name_none_reason_invalid(self):
        self.infant_fu_immunizations.vaccines_missed = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': None,
            'reason_missed': 'missed scheduled vaccination'
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_missed', form_validator._errors)

    def test_missed_vaccine_name_none_reason_none_valid(self):
        self.infant_fu_immunizations.vaccines_missed = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'missed_vaccine_name': None,
            'reason_missed': None,
        }
        form_validator = VaccinesMissedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unexpectedly. Got{e}')
