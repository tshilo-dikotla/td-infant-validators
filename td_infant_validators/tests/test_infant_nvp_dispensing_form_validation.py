from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO
from ..form_validators import InfantNvpDispensingFormValidator


class TestInfantNvpDispensingFormValidator(TestCase):

    def test_nvp_prophylaxis_yes_azt_required(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': None,
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('azt_prophylaxis', form_validator._errors)

    def test_nvp_prophylaxis_yes_azt_given(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_yes_reason_not_given_invalid(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': 'specified',
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_not_given', form_validator._errors)

    def test_nvp_prophylaxis_yes_reason_not_given_none_valid(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_no_reason_not_given_req(self):
        cleaned_data = {
            'nvp_prophylaxis': NO,
            'azt_prophylaxis': NO,
            'reason_not_given': None}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('reason_not_given', form_validator._errors)

    def test_nvp_prophylaxis_no_reason_not_given_specified(self):
        cleaned_data = {
            'nvp_prophylaxis': NO,
            'azt_prophylaxis': NO,
            'reason_not_given': 'specified'}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_yes_nvp_admin_date_req(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': None,
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('nvp_admin_date', form_validator._errors)

    def test_nvp_prophylaxis_yes_nvp_admin_date_given(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_no_nvp_admin_date_invalid(self):
        cleaned_data = {
            'nvp_prophylaxis': NO,
            'azt_prophylaxis': NO,
            'reason_not_given': 'specified',
            'nvp_admin_date': get_utcnow().date()}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('nvp_admin_date', form_validator._errors)

    def test_nvp_prophylaxis_no_nvp_admin_date_none_valid(self):
        cleaned_data = {
            'nvp_prophylaxis': NO,
            'azt_prophylaxis': NO,
            'reason_not_given': 'specified',
            'nvp_admin_date': None}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_yes_medication_instructions_req(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': None,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('medication_instructions', form_validator._errors)

    def test_nvp_prophylaxis_yes_medication_instructions_given(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_yes_dose_admin_infant_req(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': None,
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dose_admin_infant', form_validator._errors)

    def test_nvp_prophylaxis_yes_dose_admin_infant_given(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_no_dose_admin_infant_invalid(self):
        cleaned_data = {
            'nvp_prophylaxis': NO,
            'azt_prophylaxis': NO,
            'reason_not_given': 'specified',
            'nvp_admin_date': None,
            'medication_instructions': NO,
            'dose_admin_infant': '50'}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dose_admin_infant', form_validator._errors)

    def test_nvp_prophylaxis_no_dose_admin_infant_none(self):
        cleaned_data = {
            'nvp_prophylaxis': NO,
            'azt_prophylaxis': NO,
            'reason_not_given': 'specified',
            'nvp_admin_date': None,
            'medication_instructions': NO,
            'dose_admin_infant': None}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_nvp_prophylaxis_yes_correct_dose_req(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': None}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('correct_dose', form_validator._errors)

    def test_nvp_prophylaxis_yes_correct_dose_given(self):
        cleaned_data = {
            'nvp_prophylaxis': YES,
            'azt_prophylaxis': NO,
            'reason_not_given': None,
            'nvp_admin_date': get_utcnow().date(),
            'medication_instructions': YES,
            'dose_admin_infant': '50',
            'correct_dose': YES}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_azt_prophylaxis_yes_dose_given_req(self):
        cleaned_data = {
            'azt_prophylaxis': YES,
            'azt_dose_given': None}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('azt_dose_given', form_validator._errors)

    def test_azt_prophylaxis_yes_dose_given_specified(self):
        cleaned_data = {
            'azt_prophylaxis': YES,
            'azt_dose_given': '4'}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_azt_prophylaxis_no_dose_given_invalid(self):
        cleaned_data = {
            'azt_prophylaxis': NO,
            'azt_dose_given': '4'}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('azt_dose_given', form_validator._errors)

    def test_azt_prophylaxis_no_dose_given_none_valid(self):
        cleaned_data = {
            'azt_prophylaxis': NO,
            'azt_dose_given': None}
        form_validator = InfantNvpDispensingFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
