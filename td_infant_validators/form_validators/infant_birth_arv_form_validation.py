from django.core.exceptions import ValidationError
from edc_constants.constants import YES, UNKNOWN
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantBirthArvFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.required_if(
            YES,
            field='azt_after_birth',
            field_required='azt_dose_date',
            required_msg='Provide date of the first dose for AZT.',
            not_required_msg=(
                'Participant indicated that AZT was NOT provided. '
                'You cannot provide date of first dose')
        )

        if (self.cleaned_data.get('azt_after_birth')
            and (self.cleaned_data.get('azt_after_birth') == UNKNOWN
                 and self.cleaned_data.get('azt_additional_dose') != UNKNOWN)):
            msg = {'azt_additional_dose': 'If Q3 is \'unknown\', '
                   'this field must be \'unknown.\''}
            self._errors.update(msg)
            raise ValidationError(msg)
        else:
            self.applicable_if(
                YES,
                field='azt_after_birth',
                field_applicable='azt_additional_dose'
            )

        self.required_if(
            YES,
            field='sdnvp_after_birth',
            field_required='nvp_dose_date',
            required_msg=('If infant has received single dose NVP then provide'
                          'NVP date.'),
            not_required_msg=('Participant indicated that NVP was NOT provided'
                              'You cannot provide date of first dose.')
        )
