from django import forms
from edc_constants.constants import (
    NO, NOT_APPLICABLE, UNKNOWN, YES)
from edc_form_validators import FormValidator

from td_infant.models import (InfantVisit, InfantBirthArv)
from tshilo_dikotla.constants import (
    MODIFIED, DISCONTINUED, NEVER_STARTED, START)


def get_birth_arv_visit_2000(infant_identifier):
    """Check if infant was given AZT at birth"""
    try:
        visit_2000 = InfantVisit.objects.get(
            subject_identifier=infant_identifier,
            appointment__visit_definition__code=2000,
            appointment__visit_instance=0)
        infant_birth_arv = InfantBirthArv.objects.get(infant_visit=visit_2000)
        return infant_birth_arv.azt_discharge_supply
    except InfantBirthArv.DoesNotExist:
        pass


return NOT_APPLICABLE


class InfantArvProphFormValidator(FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == NO:
            raise forms.ValidationError(
                {'prophylatic_nvp': 'Infant is HEU, answer cannot be No.'})
        self.validate_taking_arv_proph_unknown()

    def validate_taking_arv_proph_unknown(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').subject_identifier
        if cleaned_data.get('prophylatic_nvp') == UNKNOWN and
        cleaned_data.get('arv_status') not in ['modified']:
            if get_birth_arv_visit_2000(infant_identifier) not in [UNKNOWN]:
                raise forms.ValidationError(
                    'The azt discharge supply in Infant Birth arv was not'
                    ' answered as UNKNOWN, Q3 cannot be Unknown.')

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == NO:
            raise forms.ValidationError(
                {'prophylatic_nvp': 'Infant is HEU, answer cannot be No.'})

    def validate_taking_arv_proph_yes(self):
        cleaned_data = self.cleaned_data
        arv_proph_mod = self.data.get(
            'infantarvprophmod_set-0-arv_code')
        if cleaned_data.get('prophylatic_nvp') == YES:
            if cleaned_data.get('arv_status') in [START, MODIFIED] and not arv_proph_mod:
                raise forms.ValidationError(
                    {'arv_status': 'Please complete the infant arv proph mods table.'})
            if cleaned_data.get('arv_status') == NEVER_STARTED and arv_proph_mod:
                raise forms.ValidationError(
                    {'arv_status': 'Infant never started prophlaxis, do not complete '
                     'the infant arv proph mods table.'})

