from django.apps import apps as django_apps
from django import forms
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_form_validators import FormValidator


class InfantFeedingFormValidator(FormValidator):

    infantfeeding = 'td_infant.infantfeeding'
    infantvisit = 'td_infant.infantvisit'

    def clean(self):
        #         self.validate_formula_intro_occur_previous()
        self.validate_formula_intro_date_not_future()
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

        self.required_if(
            YES,
            field='took_formula',
            field_required='is_first_formula',
            required_msg='Question7: Infant took formula, is this the '
            'first reporting of infant formula use? Please provide YES or NO')

        self.required_if(
            YES,
            field='is_first_formula',
            field_required='date_first_formula',
            required_msg='If this is a first reporting of infant formula'
            ' please provide date and if date is estimated')

        self.required_if(
            YES,
            field='is_first_formula',
            field_required='est_date_first_formula',
            required_msg='If this is a first reporting of infant formula'
            ' please provide date and if date is estimated')

        self.not_required_if(
            NO,
            field='is_first_formula',
            field_required='date_first_formula',
            required_msg='Question8: You mentioned that is not the '
            'first reporting of infant formula PLEASE DO NOT PROVIDE DATE'
        )

        self.not_required_if(
            NO,
            field='is_first_formula',
            field_required='date_first_formula',
            required_msg='Question8: You mentioned that is not the '
            'first reporting of infant formula PLEASE DO NOT PROVIDE DATE'
        )

        self.not_required_if(
            NO,
            field='is_first_formula',
            field_required='est_date_first_formula',
            required_msg='Question9: You mentioned that is not the '
            'first reporting of infant formula PLEASE DO NOT PROVIDE EST DATE'
        )

        self.required_if(
            YES,
            field='took_formula',
            field_required='is_first_formula',
            required_msg='Question7: You mentioned that infant did not take formula,'
            ' PLEASE DO NOT PROVIDE FIRST FORMULA USE INFO'
        )

        self.required_if(
            YES,
            field='took_formula',
            field_required='date_first_formula',
            required_msg='Question8: You mentioned that infant did not take formula,'
            ' PLEASE DO NOT PROVIDE DATE OF FIRST FORMULA USE'
        )

        self.required_if(
            YES,
            field='took_formula',
            field_required='est_date_first_formula',
            required_msg='Question9: You mentioned that infant did not take formula,'
            ' PLEASE DO NOT PROVIDE ESTIMATED DATE OF FIRST FORMULA USE'
        )

        self.required_if(
            YES,
            field='other_milk',
            field_required='other_milk_animal',
            required_msg='Question15: The infant took milk from another animal, '
            'please specify which?'
        )

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
            'infant_visit').appointment.registered_subject.subject_identifier,
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
