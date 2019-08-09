from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantArvProphFormValidator(InfantFormValidatorMixin,
                                  CrfOffStudyFormValidator,
                                  FormValidator):

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
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_taking_arv_proph_unknown()
        self.validate_taking_arv_proph_no()

    def validate_taking_arv_proph_unknown(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').subject_identifier
        if cleaned_data.get('prophylatic_nvp') == 'Unknown' and \
                cleaned_data.get('arv_status') not in ['modified']:
            if self.get_birth_arv_visit_2000(infant_identifier) not in ['Unknown']:
                msg = {'prophylatic_nvp':
                       'The azt discharge supply in Infant Birth arv was not'
                       ' answered as \'Unknown\', Q3 cannot be Unknown.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_taking_arv_proph_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prophylatic_nvp') == NO:
            msg = {'prophylatic_nvp': 'Infant is HEU, answer cannot be No.'}
            self._errors.update(msg)
            raise ValidationError(msg)
