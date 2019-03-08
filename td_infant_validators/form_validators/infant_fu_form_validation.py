from django.core.exceptions import ValidationError
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
        try:
            if self.cleaned_data.get('days_hospitalized') is not None:
                condition = self.cleaned_data.get('days_hospitalized') <= 90
                self.applicable_if_true(
                    condition,
                    field_applicable='days_hospitalized',
                    not_applicable_msg='days hospitalized cannot be greater than 90days'
                )
        except ValidationError:
            self._errors.update('Total number of days hospitalized required')
            raise ValidationError('Total number of days hospitalized required')
