from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantBirthDataFormValidator(InfantFormValidatorMixin,
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
        self.validate_apgar_score()

    def validate_apgar_score(self):
        agpar_list = ['apgar_score_min_1', 'apgar_score_min_5',
                      'apgar_score_min_10']

        for agpar in agpar_list:
            self.required_if(
                YES,
                field='apgar_score',
                field_required=agpar,
                required_msg='If Apgar scored performed, this field is required.')
