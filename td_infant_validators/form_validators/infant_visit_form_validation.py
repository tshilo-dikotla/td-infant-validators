from edc_form_validators import FormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantVisitFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('subject_identifier')
        report_datetime = cleaned_data.get('report_datetime')
        self.validate_against_birth_date(infant_identifier=infant_identifier,
                                         report_datetime=report_datetime)
