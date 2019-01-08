from edc_constants.constants import YES
from edc_form_validators import FormValidator


class InfantArvFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            YES,
            field='azt_after_birth',
            field_required='azt_dose_date',
            required_msg='Provide date of the first dose for AZT.',
            not_required_msg=(
                'Participant indicated that AZT was NOT provided. '
                'You cannot provide date of first dose')
        )
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
