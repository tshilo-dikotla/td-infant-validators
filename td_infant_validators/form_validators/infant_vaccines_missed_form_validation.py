from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class VaccinesMissedFormValidator(InfantFormValidatorMixin,
                                  CrfOffStudyFormValidator,
                                  FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_fu_immunizations').infant_visit.appointment.subject_identifier
        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_other_specify('reason_missed')

        self.validate_vaccine_missed(cleaned_data=self.cleaned_data)
        self.validate_missed_vaccine_fields(cleaned_data=self.cleaned_data)

    def validate_vaccine_missed(self, cleaned_data=None):
        condition = cleaned_data.get(
            'infant_fu_immunizations').vaccines_missed == YES
        self.required_if_true(
            condition,
            field_required='missed_vaccine_name',
            required_msg=('You mentioned that vaccines were missed. Please '
                          'indicate which ones on the table.'),
        )

    def validate_missed_vaccine_fields(self, cleaned_data=None):
        self.required_if_not_none(
            field='missed_vaccine_name',
            field_required='reason_missed',
            required_msg=('You said {} vaccine was missed. Give a reason'
                          ' for missing this vaccine'.format(
                              cleaned_data.get('missed_vaccine_name')))
        )
