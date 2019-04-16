from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantFuFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.required_if(
            YES,
            field='was_hospitalized',
            field_required='days_hospitalized',
            required_msg='If infant was hospitalized, '
            'please provide # of days hospitalized')
