from django.core.exceptions import ValidationError
from django.apps import apps as django_apps
from edc_form_validators import FormValidator


class InfantVisitFormValidator(FormValidator):

    registered_subject_model = 'edc_registration.registeredsubject'
    subject_screening_model = 'td_maternal.subjectscreening'
    td_consent_version_model = 'td_maternal.tdconsentversion'
    maternal_consent_model = 'td_maternal.subjectconsent'

    @property
    def registered_subject_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def maternal_eligibility_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def consent_version_cls(self):
        return django_apps.get_model(self.td_consent_version_model)

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    def clean(self):
        self.validate_current_consent_version()

    def validate_current_consent_version(self):
        try:
            td_consent_version = self.consent_version_cls.objects.get(
                subjectscreening=self.maternal_eligibility)
        except self.consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Complete mother\'s consent version form before proceeding')
        else:
            try:
                self.maternal_consent_cls.objects.get(
                    screening_identifier=self.maternal_eligibility.screening_identifier,
                    version=td_consent_version.version)
            except self.maternal_consent_cls.DoesNotExist:
                raise ValidationError(
                    'Complete Maternal Consent form for version {} before '
                    'proceeding'.format(td_consent_version.version))

    @property
    def maternal_eligibility(self):
        cleaned_data = self.cleaned_data
        try:
            relative_identifier = self.registered_subject_cls.objects.get(
                subject_identifier=cleaned_data.get('subject_identifier')).relative_identifier
            return self.maternal_eligibility_cls.objects.get(
                subject_identifier=relative_identifier)
        except self.maternal_eligibility_cls.DoesNotExist:
            pass
        except self.registered_subject_cls.DoesNotExist:
            raise ValidationError('Registered Subject does not exist.')
