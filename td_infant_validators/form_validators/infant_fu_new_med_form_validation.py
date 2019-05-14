from django import forms
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantFuNewMedFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))


class InfantFuNewMedItemsFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_other_specify(
            other_specify_field='other_medication',
            field='medication',
            required_msg='Please specify other medication.',
            not_required_msg='Please select Other in Medication '
            'in when if Other medication is being record.'
        )
        self.validate_stop_date()

    def validate_stop_date(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('date_first_medication'):
                raise forms.ValidationError(
                    'You have indicated that medication stop date is before its start date. '
                    'Please correct.')
