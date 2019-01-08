from django import forms

from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
# from ..models import InfantNvpAdjustment


class InfantNvpAdjustmentForm(FormValidator):

    def clean(self):
        cleaned_data = super(InfantNvpAdjustmentForm, self).clean()
        self.validate_dose_adjustment()
        self.validate_dose_4_weeks()

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
            field_required='adjusted_dose',
            not_applicable_msg=(
                'Infant\'s dose was not adjusted, please do not give an adjust dose.'
            ))

        self_
        return cleaned_data

    def validate_dose_4_weeks(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('dose_4_weeks') == YES:
            if cleaned_data.get('incomplete_dose'):
                raise forms.ValidationError(
                    'Medication was taken daily for 4 weeks, don\'t give reason for incomplete dose.')
        else:
            if not cleaned_data.get('incomplete_dose'):
                raise forms.ValidationError(
                    'Medication was not taken daily for 4 weeks, please give reason for incomplete.')
