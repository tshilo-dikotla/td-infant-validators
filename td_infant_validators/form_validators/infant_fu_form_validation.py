from edc_constants.constants import YES
from edc_form_validators import FormValidator


class InfantFuFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='was_hospitalized',
            field_required='days_hospitalized',
            required_msg='If infant was hospitalized, '
            'please provide # of days hospitalized')
