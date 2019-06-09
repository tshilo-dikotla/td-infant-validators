from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantBirthFeedingFormValidator(InfantFormValidatorMixin,
                                      CrfOffStudyFormValidator,
                                      FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        infant_identifier = self.cleaned_data.get('infant_visit').subject_identifier
        report_datetime = self.cleaned_data.get('report_datetime')
        self.validate_against_birth_date(infant_identifier=infant_identifier,
                                         report_datetime=report_datetime)
