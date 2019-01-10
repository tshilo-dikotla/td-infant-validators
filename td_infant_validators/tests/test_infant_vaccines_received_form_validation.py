from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO
from .models import InfantFuImmunizations, InfantBirth, InfantVisit, Appointment
from ..form_validators import VaccinesReceivedFormValidator
from dateutil.relativedelta import relativedelta


@tag('received')
class TestVaccinesReceivedFormValidator(TestCase):

    def setUp(self):
        subject_identifier = '22334'
        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='1000')

        infant_visit = InfantVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)
        self.infant_fu_immunizations = InfantFuImmunizations.objects.create(
            infant_visit=infant_visit,
            vaccines_received=YES,
            vaccines_missed=NO)

        InfantBirth.objects.create(
            subject_identifier=subject_identifier,
            dob=(get_utcnow() - relativedelta(months=7)).date())
        infant_birth_model = 'td_infant_validators.infantbirth'
        VaccinesReceivedFormValidator.infant_birth_model = infant_birth_model

    def test_infant_fu_immunization_vaccine_received_yes_name_required(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': None,
            'date_given': get_utcnow().date()
        }
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('received_vaccine_name', form_validator._errors)

    def test_infant_fu_immunization_vaccine_received_yes_name_given(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Polio',
            'date_given': get_utcnow().date(),
            'infant_age': '2'
        }
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unexpectedly. Got{e}')

    def test_date_given_before_birth_date_invalid(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Polio',
            'date_given': get_utcnow().date() - relativedelta(months=10),
            'infant_age': '2'
        }
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('date_given', form_validator._errors)

    def test_date_given_after_birth_date_valid(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Polio',
            'date_given': get_utcnow().date(),
            'infant_age': '2'
        }
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError raised unexpectedly. Got{e}')

    def test_received_vaccine_date_given_required(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Polio',
            'date_given': None,
            'infant_age': '2'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('date_given', form_validator._errors)

    def test_received_vaccine_date_given_provided(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Polio',
            'date_given': get_utcnow().date(),
            'infant_age': '4'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_received_vaccine_none_date_given_invalid(self):
        self.infant_fu_immunizations.vaccines_received = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': None,
            'date_given': get_utcnow().date()}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('date_given', form_validator._errors)

    def test_received_vaccine_none_date_given_none_valid(self):
        self.infant_fu_immunizations.vaccines_received = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': None,
            'date_given': None}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_received_vaccine_infant_age_required(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Polio',
            'date_given': get_utcnow().date(),
            'infant_age': None}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_age', form_validator._errors)

    def test_received_vaccine_infant_age_provided(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Polio',
            'date_given': get_utcnow().date(),
            'infant_age': '18'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_received_vaccine_none_infant_age_invalid(self):
        self.infant_fu_immunizations.vaccines_received = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': None,
            'date_given': None,
            'infant_age': '4'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_age', form_validator._errors)

    def test_received_vaccine_none_infant_age_none_valid(self):
        self.infant_fu_immunizations.vaccines_received = NO
        self.infant_fu_immunizations.save()
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': None,
            'date_given': None,
            'infant_age': None}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_bcg_administered_at_correct_age(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'BCG',
            'date_given': get_utcnow().date(),
            'infant_age': 'At Birth'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_bcg_adminstered_infant_age_incorrect(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'BCG',
            'date_given': get_utcnow().date(),
            'infant_age': '4'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_age', form_validator._errors)

    def test_hepatitis_b_administered_at_correct_age(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Hepatitis_B',
            'date_given': get_utcnow().date(),
            'infant_age': '2'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_hepatitis_b_adminstered_infant_age_incorrect(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Hepatitis_B',
            'date_given': get_utcnow().date(),
            'infant_age': '18'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_age', form_validator._errors)

    def test_dpt_administered_at_correct_age(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'DPT',
            'date_given': get_utcnow().date(),
            'infant_age': '2'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_dpt_adminstered_infant_age_incorrect(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'DPT',
            'date_given': get_utcnow().date(),
            'infant_age': '18'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_age', form_validator._errors)

    def test_haem_administered_at_correct_age(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Haemophilus_influenza',
            'date_given': get_utcnow().date(),
            'infant_age': '4'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_haem_adminstered_infant_age_incorrect(self):
        cleaned_data = {
            'infant_fu_immunizations': self.infant_fu_immunizations,
            'received_vaccine_name': 'Haemophilus_influenza',
            'date_given': get_utcnow().date(),
            'infant_age': '6'}
        form_validator = VaccinesReceivedFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('infant_age', form_validator._errors)
