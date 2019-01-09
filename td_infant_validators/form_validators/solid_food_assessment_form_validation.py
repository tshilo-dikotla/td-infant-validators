from edc_constants.constants import YES
from edc_form_validators import FormValidator


class SolidFoodAssessementFormValidator(FormValidator):

    def clean(self):

        self.required_if(
            YES,
            field='porridge',
            field_required='porridge_freq',
            required_msg='Question6: Please indicate how many times this child has had porridge in the last week'
        )
        self.required_if(
            YES,
            field='tsabana',
            field_required='tsabana_week',
            required_msg='Question8: Please indicate how many times this child has had tsabana in the last week'
        )

        self.required_if(
            YES,
            field='meat',
            field_required='meat_freq',
            required_msg='Question11: Please indicate how many times the child has had any meat, chicken or fish'
        )

        self.required_if(
            YES,
            field='potatoes',
            field_required='potatoes_freq',
            required_msg='Question13: Please indicate how many times the child has had any potatoes'
        )

        self.required_if(
            YES,
            field='carrot_swt_potato',
            field_required='carrot_swt_potato_freq',
            required_msg='Question15: Please indicate how many times this child has had carrot, pumpkin or sweet potato'
        )

        self.required_if(
            YES,
            field='carrot_swt_potato',
            field_required='carrot_swt_potato_freq',
            required_msg='Question15: Please indicate how many times this child has had carrot, pumpkin or sweet potato'
        )

        self.required_if(
            YES,
            field='green_veg',
            field_required='green_veg_freq',
            required_msg='Question17: Please indicate how many times this child has had green vegetables in the last week'
        )

        self.required_if(
            YES,
            field='fresh_fruits',
            field_required='fresh_fruits_freq',
            required_msg='Question19: Please indicate how many times this child has had fresh fruits in the last week'
        )

        self.required_if(
            YES,
            field='fullcream_milk',
            field_required='fullcream_milk_freq',
            required_msg='Question21: Please indicate how many times this child has had full cream milk in the last week'
        )

        self.required_if(
            YES,
            field='skim_milk',
            field_required='skim_milk_freq',
            required_msg='Question23: Please indicate how many times this child has had skim milk in the last week'
        )

        self.required_if(
            YES,
            field='raw_milk',
            field_required='raw_milk_freq',
            required_msg='Question25: Please indicate how many times this child has had raw milk in the last week'
        )

        self.required_if(
            YES,
            field='juice',
            field_required='juice_freq',
            required_msg='Question27: Please indicate how many times this child has had juice in the last week'
        )

        self.required_if(
            YES,
            field='eggs',
            field_required='eggs_freq',
            required_msg='Question29: Please indicate how many times this child has had eggs in the last week'
        )

        self.required_if(
            YES,
            field='yogurt',
            field_required='yogurt_freq',
            required_msg='Question31: Please indicate how many times this child has had yogurt in the last week'
        )

        self.required_if(
            YES,
            field='cheese',
            field_required='cheese_freq',
            required_msg='Question33: Please indicate how many times this child has had Cheese in the last week'
        )

        self.m2m_other_specify(
            'Other',
            m2m_field='solid_foods',
            field_other='solid_foods_other',

        )
