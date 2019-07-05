from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantNvpAdjustmentFormValidator(InfantFormValidatorMixin,
                                       CrfOffStudyFormValidator,
                                       FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

        self.required_if(
            YES,
            field='dose_adjustment',
            field_required='adjusted_dose',
            required_msg=(
                'If there was a dose adjustment, please give the adjusted dose.'
            ))

        self.required_if(
            NO,
            field='dose_4_weeks',
            field_required='incomplete_dose'
        )
