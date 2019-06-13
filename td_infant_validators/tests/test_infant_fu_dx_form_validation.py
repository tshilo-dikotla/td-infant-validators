from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO

from ..form_validators import InfantFuDxItemsFormValidator
from .models import InfantVisit, Appointment


class TestInfantFuDxItemsFormValidator(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=get_utcnow(),
            visit_code='2000',
            visit_instance='0')

        self.infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment)

    def test_health_facility_no_was_hospitalized_yes_invalid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'health_facility': NO,
            'was_hospitalized': YES}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('health_facility', form_validator._errors)

    def test_health_facility_yes_was_hospitalized_yes_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'health_facility': YES,
            'was_hospitalized': YES}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_health_facility_no_was_hospitalized_no_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'health_facility': NO,
            'was_hospitalized': NO}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_fu_dx_other_serious_fu_dx_specify_required(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'fu_dx': 'Other serious (grade 3 or 4)infection(not listed above),'
            'specify',
            'fu_dx_specify': None}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('fu_dx_specify', form_validator._errors)

    def test_fu_dx_other_abnlabtest_fu_dx_specify_required(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'fu_dx': ('Other abnormallaboratory tests(other than tests '
                      'listed above  or tests done as part of this study),'
                      ' specify test and result'),
            'fu_dx_specify': None}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('fu_dx_specify', form_validator._errors)

    def test_fu_dx_other_fu_dx_specified_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'fu_dx': ('Other serious (grade 3 or 4) non-infectious'
                      '(not listed above),specify'),
            'fu_dx_specify': 'description'}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_fu_dx_specified_other_fu_dx_invalid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'fu_dx': 'Acute Renal Failure',
            'fu_dx_specify': 'description'}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('fu_dx_specify', form_validator._errors)

    def test_fu_dx_specified_other_fu_dx_none_valid(self):
        cleaned_data = {
            'infant_visit': self.infant_visit,
            'fu_dx': 'Acute Renal Failure',
            'fu_dx_specify': None}
        form_validator = InfantFuDxItemsFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
