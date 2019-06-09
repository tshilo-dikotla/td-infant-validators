from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator
from td_infant_validators.form_validators import CrfOffStudyFormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantFuDxFormValidator(InfantFormValidatorMixin, CrfOffStudyFormValidator, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))


class InfantFuDxItemsFormValidator(InfantFormValidatorMixin,
                                   CrfOffStudyFormValidator, FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        self.validate_health_facility(cleaned_data=self.cleaned_data)

        responses = ('Other serious (grade 3 or 4)infection(not listed above),specify',
                     'Other serious (grade 3 or 4) non-infectious(not listed above),specify',
                     'Other abnormallaboratory tests(other than tests listed above '
                     'or tests done as part of this study), specify test and result',
                     'New congenital abnormality not previously identified?,specify')

        self.required_if(
            *responses,
            field='fu_dx',
            field_required='fu_dx_specify'
        )

    def validate_health_facility(self, cleaned_data=None):
        if cleaned_data.get('health_facility') == NO:
            if cleaned_data.get('was_hospitalized') == YES:
                msg = {'health_facility':
                       'You indicated that participant was hospitalized, therefore '
                       'the participant was seen at a health facility. Please correct'}
                self._errors.update(msg)
                raise ValidationError(msg)
