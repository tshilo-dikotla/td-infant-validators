from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantBirthDataFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
