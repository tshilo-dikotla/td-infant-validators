from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class InfantFormValidatorMixin:

    registered_subject_model = 'edc_registration.registeredsubject'
    subject_screening_model = 'td_maternal.subjectscreening'
    td_consent_version_model = 'td_maternal.tdconsentversion'
    maternal_consent_model = 'td_maternal.subjectconsent'
    infant_birth_model = 'td_infant.infantbirth'

    @property
    def registered_subject_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def consent_version_cls(self):
        return django_apps.get_model(self.td_consent_version_model)

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    def validate_against_consent_datetime(self, report_datetime):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        latest_consent = self.validate_against_consent()
        if report_datetime and report_datetime < latest_consent.consent_datetime:
            raise forms.ValidationError(
                "Report datetime cannot be before consent datetime")

    def validate_against_consent(self):
        """Returns an instance of the current maternal consent version form or
        raises an exception if not found."""
        try:
            self.consent_version_cls.objects.get(
                screening_identifier=self.subject_screening.screening_identifier)
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Please complete mother\'s consent version form before proceeding')
        else:
            try:
                latest_consent = self.maternal_consent_cls.objects.get(
                    subject_identifier=self.infant_registered_subject.relative_identifier)
            except self.maternal_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Please complete Maternal Consent form '
                    f'before  proceeding.')
            else:
                return latest_consent

    @property
    def infant_registered_subject(self):
        cleaned_data = self.cleaned_data
        try:
            rs = self.registered_subject_cls.objects.get(
                subject_identifier=cleaned_data.get(
                    'infant_visit').subject_identifier)
        except self.registered_subject_cls.DoesNotExist:
            raise ValidationError('Registered Subject does not exist.')
        else:
            return rs

    @property
    def subject_screening(self):
        try:
            return self.subject_screening_cls.objects.get(
                subject_identifier=self.infant_registered_subject.relative_identifier)
        except self.subject_screening_cls.DoesNotExist:
            raise ValidationError(
                'Maternal Subject Screening does not exist.')
