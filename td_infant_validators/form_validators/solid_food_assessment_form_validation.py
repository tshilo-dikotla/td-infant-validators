from django import forms
from edc_constants.constants import YES, OTHER
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

        self.m2m_required_if(
            YES,
            field='rations',
            m2m_field='rations_receviced')

        self.m2m_other_specify(
            OTHER,
            m2m_field='rations_receviced',
            field_other='rations_receviced_other'
        )
