from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator


class InfantNvpAdjustmentFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='dose_adjustment',
            field_required='adjusted_dose',
            required_msg=(
                'If there was a dose adjustment, please give the adjusted dose.'
            ))

        self.required_if(
            NO,
            field='dose_4_weeks',
            field_required='incomplete_dose'
        )
