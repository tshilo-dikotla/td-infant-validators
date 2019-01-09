from django import forms
from edc_constants.constants import YES
from edc_form_validators import FormValidator


class InfantFuNewMedItemsForm(FormValidator):

    def clean(self):

        condition = self.cleaned_data.get(
            'infant_fu_med').new_medications == YES
        self.required_if_true(
            condition,
            field='infant_fu_med',
            field_required='medication',
            required_msg=(
                'You have indicated that participant took medications.'
                'Please provide them.'))

        self.validate_other_specify(
            other_specify_field='other_medication',
            field='medication',
            required_msg='Please specify other medication.',
            not_required_msg='Please select Other in Medication '
            'in when if Other medication is being record.'
        )

    def validate_stop_date(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('stop_date'):
            if cleaned_data.get('stop_date') < cleaned_data.get('date_first_medication'):
                raise forms.ValidationError(
                    'You have indicated that medication stop date is before its start date. '
                    'Please correct.')

#     def validate_new_medications(self):
#         cleaned_data = self.cleaned_data
#         if cleaned_data.get('infant_fu_med').new_medications == YES:
#             if not cleaned_data.get('medication'):
#                 raise forms.ValidationError(
#                     'You have indicated that participant took medications. Please provide them.')
#         if cleaned_data.get('infant_fu_med').new_medications == NO:
#             raise forms.ValidationError('You indicated that no medications were taken. You cannot provide the '
#                                         'medication. Please correct')


#     def validate_other(self):
#         cleaned_data = self.cleaned_data
#         if cleaned_data.get('medication') == OTHER and not cleaned_data.get('other_medication'):
#             raise forms.ValidationError('Please specify other medication.')
#         if not cleaned_data.get('medication') == OTHER and cleaned_data.get('other_medication'):
#             raise forms.ValidationError('Please select Other in Medication '
#                                         'in when if Other medication is being record.')
