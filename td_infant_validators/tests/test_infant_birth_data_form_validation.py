from django.test import TestCase, tag
from django.utils import timezone
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO, UNKNOWN

from ..form_validators import InfantBirthDataFormValidator
from .models import InfantVisit, Appointment
from django import forms


@tag('apgar_1')
class TestInfantBirthDataFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=timezone.now(),
            visit_code='2000',
            visit_instance='0')

        infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

        self.options = {
            'report_datetime': timezone.now(),
            'infant_visit': infant_visit,
            'weight_kg': 3.61,
            'infant_length': 89.97,
            'head_circumference': 39.30,
            'apgar_score': NO,
            'apgar_score_min_1': '',
            'apgar_score_min_5': '',
            'apgar_score_min_10': '',
            'congenital_anomalities': NO
        }

    def test_validate_apgar_1(self):
        self.options['apgar_score'] = YES
        form = InfantBirthDataFormValidator(cleaned_data=self.options)
        self.assertRaises(forms.ValidationError, form.validate)
        errors = form._errors.keys()
        self.assertIn(
            'apgar_score_min_1', errors)

    def test_validate_apgar_2(self):
        self.options['apgar_score'] = YES
        self.options['apgar_score_min_1'] = 2
        form = InfantBirthDataFormValidator(cleaned_data=self.options)
        self.assertRaises(forms.ValidationError, form.validate)
        errors = form._errors.keys()
        self.assertIn(
            'apgar_score_min_5', errors)

    def test_validate_apgar_3(self):
        self.options['apgar_score'] = YES
        self.options['apgar_score_min_1'] = 3
        form = InfantBirthDataFormValidator(cleaned_data=self.options)
        self.assertRaises(forms.ValidationError, form.validate)
        errors = form._errors.keys()
        self.assertIn(
            'apgar_score_min_5', errors)

    def test_validate_apgar_4(self):
        self.options['apgar_score'] = NO
        self.options['apgar_score_min_1'] = 3
        form = InfantBirthDataFormValidator(cleaned_data=self.options)
        self.assertRaises(forms.ValidationError, form.validate)
        errors = form._errors.keys()
        self.assertIn(
            'apgar_score_min_1', errors)

    def test_validate_apgar_5(self):
        self.options['apgar_score'] = NO
        self.options['apgar_score_min_5'] = 3
        form = InfantBirthDataFormValidator(cleaned_data=self.options)
        self.assertRaises(forms.ValidationError, form.validate)
        errors = form._errors.keys()
        self.assertIn(
            'apgar_score_min_5', errors)
