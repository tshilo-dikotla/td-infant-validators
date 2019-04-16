from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, NOT_APPLICABLE, UNKNOWN
from edc_form_validators import FormValidator


class InfantArvProphFormValidator(FormValidator):

    infantvisit = 'td_infant.infantvisit'
    infantbirtharv = 'td_infant.infantbirtharv'

    @property
    def infant_visit_cls(self):
        return django_apps.get_model(self.infantvisit)

    @property
    def infant_birth_arv_cls(self):
        return django_apps.get_model(self.infantbirtharv)

    def get_birth_arv_visit_2000(self, infant_identifier):
        """Check if infant was given AZT at birth"""

        try:
            visit_2000 = self.infant_visit_cls.objects.get(
                subject_identifier=infant_identifier,
                appointment__visit_code=2000,
                appointment__visit_instance=0)
            infant_birth_arv = self.infant_birth_arv_cls.objects.get(
                infant_visit=visit_2000)
            return infant_birth_arv.azt_discharge_supply
        except self.infant_birth_arv_cls.DoesNotExist:
            pass

        return NOT_APPLICABLE

    def clean(self):
        self.validate_taking_arv_proph_unknown()
        self.validate_taking_arv_proph_no()

    def validate_taking_arv_proph_unknown(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').subject_identifier
        if cleaned_data.get('prophylatic_nvp') == UNKNOWN and \
                cleaned_data.get('arv_status') not in ['modified']:
            if self.get_birth_arv_visit_2000(infant_identifier) not in [UNKNOWN]:
                self._errors.update(
                    {'prophylatic_nvp':
                     'The azt discharge supply in Infant Birth arv was not'
                     ' answered as UNKNOWN, Q3 cannot be Unknown.'})
                raise forms.ValidationError(
                    'The azt discharge supply in Infant Birth arv was not'
                    ' answered as UNKNOWN, Q3 cannot be Unknown.')

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == NO:
            self._errors.update(
                {'prophylatic_nvp': 'Infant is HEU, answer cannot be No.'})
            raise ValidationError(
                {'prophylatic_nvp': 'Infant is HEU, answer cannot be No.'})
