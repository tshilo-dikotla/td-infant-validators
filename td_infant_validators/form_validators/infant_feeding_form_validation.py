from django.apps import apps as django_apps
from django import forms
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator


class InfantFeedingFormValidator(FormValidator):

    infantfeeding = 'td_infant.infantfeeding'
    infantvisit = 'td_infant.infantvisit'

    def clean(self):
        self.validate_solids()
        self.validate_formula_intro_occur_previous()
        self.validate_formula_intro_date_not_future()
        self.validate_cows_milk()
        self.validate_took_other_milk()
        self.validate_breast_milk_weaning()
        self.validate_breast_milk_completely_weaned()
        self.validate_most_recent_bm_range()

        self.required_if(
            YES,
            field='took_formula',
            field_required='is_first_formula',
            required_msg='Question7: Infant took formula, is this the '
            'first reporting of infant formula use? Please provide YES or NO',
            not_required_msg='Question7: You mentioned that infant did not take formula,'
            ' PLEASE DO NOT PROVIDE FIRST FORMULA USE INFO')

        self.required_if(
            YES,
            field='is_first_formula',
            field_required='date_first_formula',
            required_msg='If this is a first reporting of infant formula'
            ' please provide date and if date is estimated',
            not_required_msg='Question8: You mentioned that infant did not take formula,'
            ' PLEASE DO NOT PROVIDE DATE OF FIRST FORMULA USE')

        self.required_if(
            YES,
            field='is_first_formula',
            field_required='est_date_first_formula',
            required_msg='If this is a first reporting of infant formula'
            ' please provide date and if date is estimated',
            not_required_msg='Question9: You mentioned that infant did not'
            ' take formula, PLEASE DO NOT PROVIDE ESTIMATED DATE')

        self.required_if(
            YES,
            field='other_milk',
            field_required='other_milk_animal',
            required_msg='Question15: The infant took milk from another animal, '
            'please specify which?'
        )
        cleaned_data = self.cleaned_data
        infant_feeding = self.infant_feeding_cls.objects.filter(infant_visit__subject_identifier=cleaned_data.get(
            'infant_visit').appointment.subject_identifier,
            formula_intro_date__isnull=False).exclude(infant_visit=cleaned_data.get(
                'infant_visit')).last()
        condition = self.cleaned_data.get(
            'formula_intro_occur') == YES and not infant_feeding
        self.required_if_true(
            condition,
            field_required='formula_intro_date',
            required_msg='Question3: If received formula milk | foods | liquids since last'
            ' attended visit. Please provide intro date')

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

    def validate_cows_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('cow_milk') == YES:
            if cleaned_data.get('cow_milk_yes') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'Question13: If infant took cows milk. Answer CANNOT be Not Applicable')
        else:
            if not cleaned_data.get('cow_milk_yes') == 'N/A':
                raise forms.ValidationError(
                    'Question13: Infant did not take cows milk. Answer is NOT APPLICABLE')

    def validate_took_other_milk(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('other_milk') == YES:
            if not cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError(
                    'Question15: The infant took milk'
                    ' from another animal, please specify which?')
            if cleaned_data.get('milk_boiled') == NOT_APPLICABLE:
                raise forms.ValidationError('Question16:The infant took milk from another animal, answer'
                                            ' cannot be N/A')
        else:
            if cleaned_data.get('other_milk_animal'):
                raise forms.ValidationError('Question15: The infant did not take milk from any other animal, please'
                                            ' do not provide the name of the animal')

            if cleaned_data.get('milk_boiled') != NOT_APPLICABLE:
                raise forms.ValidationError('Question16: The infant did not take milk from any other animal, the'
                                            ' answer for whether the milk was boiled should be N/A')

    def validate_breast_milk_weaning(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_breastfeed') == YES:
            if cleaned_data.get('complete_weaning') != NOT_APPLICABLE:
                raise forms.ValidationError('Question24: The infant has been breastfed since the last visit, The'
                                            ' answer should be N/A')
        else:
            if cleaned_data.get('complete_weaning') == NOT_APPLICABLE:
                raise forms.ValidationError('Question24: The infant has not been breastfed since the last visit, '
                                            'The answer should not be N/A')

    def validate_breast_milk_completely_weaned(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('ever_breastfeed') == YES and
                cleaned_data.get('weaned_completely') == NO and
                not cleaned_data.get('most_recent_bm')):
            raise forms.ValidationError({'most_recent_bm': 'The infant has not'
                                         ' been weaned off of breast milk. This field'
                                         ' is required.'})
        elif (cleaned_data.get('ever_breastfeed') == NO and
                cleaned_data.get('complete_weaning') == YES and
                cleaned_data.get('most_recent_bm')):
            raise forms.ValidationError({'most_recent_bm': 'The infant has been'
                                         ' weaned off of breast milk before last '
                                         'attended scheduled visit. This field'
                                         ' is not required.'})

    def validate_most_recent_bm_range(self):
        cleaned_data = self.cleaned_data
        prev_infant_feeding = self.infant_feeding_cls.objects.filter(infant_visit__subject_identifier=cleaned_data.get(
            'infant_visit').appointment.subject_identifier,
            most_recent_bm__isnull=False,
            report_datetime__lt=cleaned_data.get('report_datetime')).exclude(infant_visit=cleaned_data.get(
                'infant_visit')).last()

        if(self.infant_feeding_cls.previous_infant_instance and
           (cleaned_data.get('ever_breastfeed') == YES and
                cleaned_data.get('weaned_completely') == YES)):

            if prev_infant_feeding:
                if(not cleaned_data.get('most_recent_bm')
                   or (cleaned_data.get('most_recent_bm') > cleaned_data.get("report_datetime").date()
                       or cleaned_data.get('most_recent_bm') < prev_infant_feeding.most_recent_bm)):

                    raise forms.ValidationError({'most_recent_bm': 'Date of most '
                                                 'recent breastfeeding must be '
                                                 'between last visit date and today.'})

    @property
    def infant_feeding_cls(self):
        return django_apps.get_model(self.infantfeeding)

    @property
    def infant_visit_cls(self):
        return django_apps.get_model(self.infantvisit)

    def validate_formula_intro_date_not_future(self):
        cleaned_data = self.cleaned_data
        if(cleaned_data.get('formula_intro_date') and
           cleaned_data.get('formula_intro_date') >
           cleaned_data.get('infant_visit').report_datetime.date()):
            raise forms.ValidationError({
                'formula_intro_date': 'Date cannot be future to visit date.'
                'Visit date is {}.'.format(
                    cleaned_data.get('infant_visit').report_datetime.date())})

    def validate_formula_intro_occur_previous(self):
        cleaned_data = self.cleaned_data
        infant_feeding = self.infant_feeding_cls.objects.filter(infant_visit__subject_identifier=cleaned_data.get(
            'infant_visit').subject_identifier,
            formula_intro_date__isnull=False,
            report_datetime__lt=cleaned_data.get('report_datetime')).exclude(infant_visit=cleaned_data.get(
                'infant_visit')).last()
        if (infant_feeding and cleaned_data.get('formula_intro_date') and
                cleaned_data.get('formula_intro_date') != infant_feeding.formula_intro_date):
            raise forms.ValidationError({'formula_intro_date':
                                         'Solids intro date does not match date '
                                         'already added in visit {},  '
                                         'which was defined as {}.'.format(infant_feeding.infant_visit.appointment.visit_definition.code,
                                                                           infant_feeding.formula_intro_date)})
        elif infant_feeding:
            cleaned_data[
                'formula_intro_date'] = infant_feeding.formula_intro_date
