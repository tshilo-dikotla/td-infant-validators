from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from ..form_validators import InfantVisitFormValidator
from .models import Appointment, MaternalConsent, InfantBirth
from .models import RegisteredSubject, TdConsentVersion, SubjectScreening


@tag('iv')
class TestInfantVisitFormValidator(TestCase):

    def setUp(self):

        infant_birth_model = 'td_infant_validators.infantbirth'
        InfantVisitFormValidator.infant_birth_model = infant_birth_model

        self.subject_identifier = '22334-10'
        relative_identifier = '22334'
        RegisteredSubject.objects.create(
            subject_identifier='22334-10',
            relative_identifier=relative_identifier)

        screening_identifier = 'M1234'
        self.maternal_eligibility = SubjectScreening.objects.create(
            subject_identifier=relative_identifier,
            screening_identifier=screening_identifier,
            age_in_years=22)

        self.consent_version = TdConsentVersion.objects.create(
            screening_identifier=screening_identifier, version='3',
            report_datetime=get_utcnow())

        self.subject_consent = MaternalConsent.objects.create(
            subject_identifier=relative_identifier,
            screening_identifier=screening_identifier,
            consent_datetime=get_utcnow(),
            dob=(get_utcnow() - relativedelta(years=25)).date(),
            version='3')

        self.infant_birth = InfantBirth.objects.create(
            subject_identifier=self.subject_identifier,
            report_datetime=get_utcnow())

        self.appointment = Appointment.objects.create(
            subject_identifier=self.subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000')

    def test_current_consent_version_exists(self):
        cleaned_data = {
            'appointment': self.appointment,
            'subject_identifier': self.subject_identifier}
        form_validator = InfantVisitFormValidator(cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
