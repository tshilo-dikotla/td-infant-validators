from django.core.exceptions import ValidationError
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class KaraboTBHistoryFormValidator(InfantFormValidatorMixin,
                                   CrfOffStudyFormValidator,
                                   FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        fields = ['coughing', 'fever', 'weight_loss',
                  'night_sweats', 'diagnosis']

        for field in fields:
            qs = self.cleaned_data.get(field + '_rel')
            if qs and qs.count() >= 1:
                selected = {obj.short_name: obj.name for obj in qs}
                if self.cleaned_data.get(field) in [NO, 'Dont_know']:
                    if NOT_APPLICABLE not in selected:
                        message = {
                            field + '_rel':
                            'This field is not applicable.'}
                        self._errors.update(message)
                        raise ValidationError(message)

                    elif NOT_APPLICABLE in selected and qs.count() > 1:
                        message = {
                            field + '_rel':
                            'This field should be Not applicable only.'}
                        self._errors.update(message)
                        raise ValidationError(message)
                elif (self.cleaned_data.get(field) == YES and
                        NOT_APPLICABLE in selected):
                    message = {
                        field + '_rel':
                        'This field is applicable.'}
                    self._errors.update(message)
                    raise ValidationError(message)

            self.m2m_other_specify(
                OTHER,
                m2m_field=field + '_rel',
                field_other='other_' + field + '_rel')
