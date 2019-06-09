from django import forms
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, OTHER, NOT_APPLICABLE
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class SolidFoodAssessementFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        age_solid_food = self.cleaned_data.get('age_solid_food')
        if age_solid_food and int(age_solid_food) < 0:
            raise forms.ValidationError({
                'age_solid_food': 'Value of age solid food cannot be negative'
            })

        fields = ['porridge', 'tsabana', 'meat', 'potatoes', 'carrot_swt_potato',
                  'green_veg', 'fresh_fruits', 'fullcream_milk', 'skim_milk',
                  'raw_milk', 'juice', 'eggs', 'yogurt', 'cheese']

        special_fields = {'meat': 'meat, chicken or fish',
                          'carrot_swt_potato': 'carrot, pumpkin or sweet potato',
                          'green_veg': 'green vegetables'}

        for field in fields:
            if field == 'tsabana':
                f_required = 'tsabana_week'
            else:
                f_required = field + '_freq'

            f_message = special_fields.get('field') or field.split('_')

            self.required_if(
                YES,
                field=field,
                field_required=f_required,
                required_msg=('Please indicate how many times this '
                              f'child has had {f_message} in the last week.')
            )

        self.m2m_other_specify(
            OTHER,
            m2m_field='solid_foods',
            field_other='solid_foods_other'
        )

        qs = self.cleaned_data.get('rations_receviced')
        if qs and qs.count() >= 1:
            selected = {obj.short_name: obj.name for obj in qs}
            if (self.cleaned_data.get('rations') == YES and
                    NOT_APPLICABLE in selected):
                message = {
                    'rations_receviced':
                    'This field is applicable.'}
                self._errors.update(message)
                raise ValidationError(message)
            elif (self.cleaned_data.get('rations') != YES and
                    NOT_APPLICABLE not in selected):
                message = {
                    'rations_receviced':
                    'This field is not applicable.'}
                self._errors.update(message)
                raise ValidationError(message)

        self.m2m_other_specify(
            OTHER,
            m2m_field='rations_receviced',
            field_other='rations_receviced_other'
        )
