from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantRequisitionFormValidator(InfantFormValidatorMixin,
                                     CrfOffStudyFormValidator, FormValidator):

    def clean(self):
        if self.cleaned_data.get('panel'):
            if (self.cleaned_data.get('panel').name != 'dna_pcr'
                    and self.cleaned_data.get('item_type') == 'dbs'):
                msg = {'item_type':
                       'DBS Card collection type is only applicable for DNA '
                       'PCR panel. Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
