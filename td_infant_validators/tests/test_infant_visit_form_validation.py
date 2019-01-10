from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from .models import RegisteredSubject, TdConsentVersion, SubjectScreening, MaternalConsent
from ..form_validators import InfantVisitFormValidator


class TestInfantVisitFormValidator(TestCase):

    def setUp(self):
        self.subject_identifier = '22334'
        relative_identifier = '12334'
        RegisteredSubject.objects.create(
            subject_identifier=self.subject_identifier,
            relative_identifier=relative_identifier)
        registered_subject_model = 'td_infant_validators.registeredsubject'
        InfantVisitFormValidator.registered_subject_model =\
            registered_subject_model

        screening_identifier = 'M1234'
        self.maternal_eligibility = SubjectScreening.objects.create(
            subject_identifier=relative_identifier,
            screening_identifier=screening_identifier,
            age_in_years=22)
        subject_screening_model = 'td_infant_validators.subjectscreening'
        InfantVisitFormValidator.subject_screening_model =\
            subject_screening_model

        self.consent_version = TdConsentVersion.objects.create(
            subjectscreening=self.maternal_eligibility, version='1',
            report_datetime=get_utcnow())
        td_consent_version_model = 'td_infant_validators.tdconsentversion'
        InfantVisitFormValidator.td_consent_version_model =\
            td_consent_version_model

        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier=relative_identifier,
            screening_identifier=screening_identifier,
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=25)).date(),
            version='1')
        self.subject_consent_model = 'td_infant_validators.maternalconsent'
        InfantVisitFormValidator.maternal_consent_model =\
            self.subject_consent_model

    def test_current_consent_version_exists(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier}
        form_validator = InfantVisitFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_current_consent_version_does_not_exist(self):
        self.consent_version.delete()
        cleaned_data = {
            'subject_identifier': self.subject_identifier}
        form_validator = InfantVisitFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('__all__', form_validator._errors)

    def test_maternal_consent_exists(self):
        cleaned_data = {
            'subject_identifier': self.subject_identifier}
        form_validator = InfantVisitFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_maternal_consent_does_not_exist(self):
        self.subject_consent.delete()
        cleaned_data = {
            'subject_identifier': self.subject_identifier}
        form_validator = InfantVisitFormValidator(cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('__all__', form_validator._errors)
