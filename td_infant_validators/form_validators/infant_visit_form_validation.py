from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantVisitFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_consent_datetime(
            self.cleaned_data.get('report_datetime'))

    @property
    def infant_registered_subject(self):
        cleaned_data = self.cleaned_data
        try:
            rs = self.registered_subject_cls.objects.get(
                subject_identifier=cleaned_data.get(
                    'appointment').subject_identifier)
        except self.registered_subject_cls.DoesNotExist:
            raise ValidationError('Registered Subject does not exist.')
        else:
            return rs
