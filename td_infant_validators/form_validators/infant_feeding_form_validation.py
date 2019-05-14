from django import forms
from django.apps import apps as django_apps
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantFeedingFormValidator(InfantFormValidatorMixin, FormValidator):

    infantfeeding = 'td_infant.infantfeeding'
    infantvisit = 'td_infant.infantvisit'

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        self.validate_formula_intro_date_not_future()
        self.validate_formula_intro_occur()
        self.validate_solids()
        self.validate_took_formula()

        self.applicable_if(
            YES,
            field='cow_milk',
            field_applicable='cow_milk_yes')

        self.required_if(
            YES,
            field='other_milk',
            field_required='other_milk_animal',
            required_msg='The infant took milk from another animal, '
            'please specify which?'
        )

        self.validate_took_other_milk()

        self.applicable_if(
            YES,
            field='other_milk',
            field_applicable='milk_boiled'
        )

        self.applicable_if(
            NO,
            field='ever_breastfeed',
            field_applicable='complete_weaning')

        self.applicable_if(
            NO,
            field='ever_breastfeed',
            field_applicable='weaned_completely')

        self.applicable_if(
            YES,
            field='took_formula',
            field_applicable='water_used')

        self.validate_most_recent_bm_range()
        self.validate_breast_milk_completely_weaned()
        self.validate_other_feeding()

        self.validate_other_specify(
            field='water_used')

    def validate_formula_intro_date_not_future(self):
        cleaned_data = self.cleaned_data
        if(cleaned_data.get('formula_intro_date') and
           cleaned_data.get('formula_intro_date') >
           cleaned_data.get('infant_visit').report_datetime.date()):
            raise forms.ValidationError({
                'formula_intro_date': 'Date cannot be future to visit date.'
                'Visit date is {}.'.format(
                    cleaned_data.get('infant_visit').report_datetime.date())})

    def validate_formula_intro_date(self, prev_infant_feeding=None):
        cleaned_data = self.cleaned_data
        visit_code = prev_infant_feeding.infant_visit.appointment.visit_code
        if (cleaned_data.get('formula_intro_date') and
                cleaned_data.get(
                    'formula_intro_date') != prev_infant_feeding.formula_intro_date):
            raise forms.ValidationError({
                'formula_intro_date': 'Solids intro date does not match date '
                f'already added in visit {visit_code}, which was defined as '
                f'{prev_infant_feeding.formula_intro_date}.'})
        elif prev_infant_feeding:
            cleaned_data[
                'formula_intro_date'] = prev_infant_feeding.formula_intro_date

    def validate_formula_intro_occur(self):
        cleaned_data = self.cleaned_data
        prev_infant_feeding = self.infant_feeding_cls.objects.filter(
            infant_visit__subject_identifier=cleaned_data.get(
                'infant_visit').appointment.subject_identifier,
            formula_intro_date__isnull=False,
            report_datetime__lt=cleaned_data.get(
                'report_datetime')).exclude(infant_visit=cleaned_data.get(
                    'infant_visit')).exclude(infant_visit=cleaned_data.get(
                        'infant_visit')).last()
        if cleaned_data.get('formula_intro_occur') == YES:
            if prev_infant_feeding:
                self.validate_formula_intro_date(prev_infant_feeding)
            else:
                if not cleaned_data.get('formula_intro_date'):
                    raise forms.ValidationError({
                        'formula_intro_date': 'If received foods since last'
                        ' attended visit. Please provide intro date'})

        elif (cleaned_data.get('formula_intro_occur') in [NO, NOT_APPLICABLE]
              and cleaned_data.get('formula_intro_date')):
            raise forms.ValidationError({
                'formula_intro_date': 'You mentioned no solid foods received'
                ' since last visit in question 4. DO NOT PROVIDE DATE'})

    def validate_solids(self):

        cleaned_data = self.cleaned_data
        if cleaned_data.get('formula_intro_occur') == YES:
            answer = False
            for question in ['fruits_veg', 'cereal_porridge', 'solid_liquid']:
                if cleaned_data.get(question) == YES:
                    answer = True
                    break
            if not answer:
                raise forms.ValidationError(
                    'You should answer YES on either one of the questions '
                    'about the fruits_veg, cereal_porridge or solid_liquid')
        else:
            answer = False
            for question in ['fruits_veg', 'cereal_porridge', 'solid_liquid']:
                if cleaned_data.get(question) == YES:
                    answer = True
                    break
            if answer:
                raise forms.ValidationError(
                    'You should answer NO on all of the questions '
                    'about the fruits_veg, cereal_porridge or solid_liquid')

    def validate_other_feeding(self):
        if self.cleaned_data.get('other_feeding') == YES:
            answer = False
            for question in ['water', 'juice', 'cow_milk',
                             'other_milk', 'solid_liquid', 'rehydration_salts']:
                if self.cleaned_data.get(question) == YES:
                    answer = True
                    break
            if not answer:
                raise forms.ValidationError(
                    'You should answer YES on either one of the questions about'
                    ' the water, juice, cow_milk, other milk, oral rehydration'
                    ' salts or solid_liquid')
        else:
            answer = False
            for question in ['water', 'juice', 'cow_milk',
                             'other_milk', 'solid_liquid', 'rehydration_salts']:
                if self.cleaned_data.get(question) == YES:
                    answer = True
                    break
            if answer:
                raise forms.ValidationError(
                    'You should answer NO on all the questions  about the water'
                    ', juice, cow_milk, other milk, oral rehydration'
                    ' salts or solid_liquid')

    def validate_took_formula(self):
        self.required_if(
            YES,
            field='took_formula',
            field_required='is_first_formula',
            required_msg='Infant took formula, is this the '
            'first reporting of infant formula use? Please provide YES or NO',
            not_required_msg='You mentioned that infant did not take formula,'
            ' PLEASE DO NOT PROVIDE FIRST FORMULA USE INFO')

        self.required_if(
            YES,
            field='is_first_formula',
            field_required='date_first_formula',
            required_msg='If this is a first reporting of infant formula'
            ' please provide date and if date is estimated',
            not_required_msg='Question8: You mentioned that infant did not '
            'take formula, PLEASE DO NOT PROVIDE DATE OF FIRST FORMULA USE')

        self.required_if(
            YES,
            field='is_first_formula',
            field_required='est_date_first_formula',
            required_msg='If this is a first reporting of infant formula'
            ' please provide date and if date is estimated',
            not_required_msg='Question9: You mentioned that infant did not'
            ' take formula, PLEASE DO NOT PROVIDE ESTIMATED DATE')

    def validate_took_other_milk(self):
        self.required_if(
            YES,
            field='other_milk',
            field_required='other_milk_animal',
            required_msg=('The infant took milk from another animal, '
                          'please specify which?'),
            not_required_msg=('The infant did not take milk from any other '
                              'animal, please do not provide the name of the '
                              'animal'))

        self.applicable_if(
            YES,
            field='other_milk',
            field_applicable='milk_boiled')

    def validate_breast_milk_completely_weaned(self):
        cleaned_data = self.cleaned_data

        if (cleaned_data.get('ever_breastfeed') == YES and
                cleaned_data.get('weaned_completely') == NO and
                not cleaned_data.get('most_recent_bm')):
            raise forms.ValidationError({'most_recent_bm': 'The infant has not'
                                         ' been weaned off of breast milk. '
                                         'This field is required.'})
        elif (cleaned_data.get('ever_breastfeed') == NO and
                cleaned_data.get('complete_weaning') == NOT_APPLICABLE and
                cleaned_data.get('most_recent_bm')):
            raise forms.ValidationError({'most_recent_bm': 'The infant has '
                                         'been weaned off of breast milk '
                                         'before last attended scheduled v'
                                         'isit. This field is not required.'})

    def validate_most_recent_bm_range(self):
        cleaned_data = self.cleaned_data

        if (self.instance.previous_infant_feeding and
            (cleaned_data.get('ever_breastfeed') == YES and
                cleaned_data.get('weaned_completely') == YES)):

            if(not cleaned_data.get('most_recent_bm')
               or (cleaned_data.get('most_recent_bm') > cleaned_data.get(
                   "report_datetime").date() or cleaned_data.get(
                       'most_recent_bm') < self.instance.previous_infant_feeding.most_recent_bm)):

                raise forms.ValidationError(
                    {'most_recent_bm': 'Date of most '
                     'recent breastfeeding must be '
                     'between last visit date and today.'})

    @property
    def infant_feeding_cls(self):
        return django_apps.get_model(self.infantfeeding)

    @property
    def infant_visit_cls(self):
        return django_apps.get_model(self.infantvisit)
