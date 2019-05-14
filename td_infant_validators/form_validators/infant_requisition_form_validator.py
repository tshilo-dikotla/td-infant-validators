from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_lab.constants import TUBE

from .form_validator_mixin import InfantFormValidatorMixin


class InfantRequisitionFormValidator(InfantFormValidatorMixin,
                                     FormValidator):

    def clean(self):
        if (self.cleaned_data.get('panel').name == 'dna_pcr'
                and self.cleaned_data.get('item_type') == TUBE):
            msg = {'item_type':
                   'DNA PCR panel must have DBS Card collection type.'
                   'Please correct.'}
            self._errors.update(msg)
            raise ValidationError(msg)
