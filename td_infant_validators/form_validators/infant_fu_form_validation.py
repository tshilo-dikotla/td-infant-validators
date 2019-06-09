from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantFuFormValidator(InfantFormValidatorMixin, CrfOffStudyFormValidator,
                            FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

        self.required_if(
            YES,
            field='was_hospitalized',
            field_required='days_hospitalized',
            required_msg='If infant was hospitalized, '
            'please provide # of days hospitalized')
