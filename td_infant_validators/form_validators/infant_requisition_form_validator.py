from django.core.exceptions import ValidationError
from edc_constants.constants import YES
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

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.required_if(
            YES,
            field='is_drawn',
            field_required='volume_units')

        panel = self.cleaned_data.get('panel').name
        volume_units = self.cleaned_data.get('volume_units')
        estimated_volume = self.cleaned_data.get('estimated_volume')

        if self.cleaned_data.get('is_drawn') == YES:
            if panel == 'infant_paxgene':
                if volume_units != 'Drops':
                    raise ValidationError({
                        'volume_units': 'Volume units for paxgene '
                        'should be in drops'})

                if estimated_volume and \
                        estimated_volume not in range(5, 11):
                    raise ValidationError({
                        'estimated_volume': 'Volume value for paxgene'
                        ' should be between 5 -10 drops'})
            else:
                if volume_units and volume_units == 'Drops':
                    raise ValidationError({
                        'volume_units': f'Volume units for {panel} '
                        'should be in mL'})
        super().clean()
