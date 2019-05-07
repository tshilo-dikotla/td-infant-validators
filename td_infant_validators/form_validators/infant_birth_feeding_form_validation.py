from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantBirthFeedingFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        print("feeding form validator class")
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        infant_identifier = self.cleaned_data.get('infant_visit').subject_identifier
        report_datetime = self.cleaned_data.get('report_datetime')
        self.validate_against_birth_date(infant_identifier=infant_identifier,
                                         report_datetime=report_datetime)
