from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantRequisitionFormValidator(InfantFormValidatorMixin,
                                     FormValidator):

    def clean(self):
        if self.cleaned_data.get('panel'):
            if (self.cleaned_data.get('panel').name != 'dna_pcr'
                    and self.cleaned_data.get('item_type') == 'dbs'):
                msg = {'item_type':
                       'DBS Card collection type is only applicable for DNA '
                       'PCR panel. Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)
