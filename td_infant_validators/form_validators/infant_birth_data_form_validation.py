from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantBirthDataFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        infant_identifier = cleaned_data.get('infant_visit').subject_identifier
        self.validate_against_birth_date(infant_identifier=infant_identifier,
                                         report_datetime=cleaned_data.get(
                                             'report_datetime'))
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
