from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow

from ..form_validators import InfantBirthFormValidator
from .models import RegisteredSubject, InfantBirth, MaternalLabourDel


class TestInfantBirthFormValidator(TestCase):

    def setUp(self):
        registered_subject_model = 'td_infant_validators.registeredsubject'
        InfantBirthFormValidator.registered_subject_model = \
            registered_subject_model

        maternal_lab_del_model = 'td_infant_validators.maternallabourdel'
        InfantBirthFormValidator.maternal_lab_del_model = \
            maternal_lab_del_model

        self.subject_identifier = '22334'
        relative_identifier = '12334'
        self.reg_subj = RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            relative_identifier=relative_identifier)

        InfantBirth.objects.create(
            subject_identifier=self.subject_identifier,
            dob=(get_utcnow() - relativedelta(months=2)).date())

        self.maternal_lab_del = MaternalLabourDel.objects.create(
            subject_identifier=relative_identifier,
            delivery_datetime=get_utcnow() - relativedelta(months=2))

    def test_infant_dob_match_delivery_date(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'report_datetime': self.maternal_lab_del.delivery_datetime,
            'dob': self.maternal_lab_del.delivery_datetime.date()}
        form_validator = InfantBirthFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_infant_dob_does_not_match_delivery_date(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'report_datetime': self.maternal_lab_del.delivery_datetime,
            'dob': get_utcnow().date()}
        form_validator = InfantBirthFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('dob', form_validator._errors)

    def test_registered_subject_does_not_exist(self):
        self.reg_subj.delete()
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'report_datetime': self.maternal_lab_del.delivery_datetime,
            'dob': self.maternal_lab_del.delivery_datetime.date()}
        form_validator = InfantBirthFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('__all__', form_validator._errors)

    def test_maternal_lab_del_does_not_exist(self):
        self.maternal_lab_del.delete()
        cleaned_data = {
            'subject_identifier': self.subject_identifier,
            'report_datetime': self.maternal_lab_del.delivery_datetime,
            'dob': self.maternal_lab_del.delivery_datetime.date()}
        form_validator = InfantBirthFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('__all__', form_validator._errors)
