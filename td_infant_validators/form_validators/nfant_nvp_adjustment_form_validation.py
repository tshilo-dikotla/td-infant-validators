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

        self.not_applicable_if(
            NO,
            field='dose_adjustment',
            field_applicable='adjusted_dose',
            not_applicable_msg=(
                'Infant\'s dose was not adjusted, please do not give an adjust dose.'
            ))

        self.not_applicable_if(
            YES,
            field='dose_4_weeks',
            field_applicable='incomplete_dose'
        )
