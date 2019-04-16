from edc_constants.constants import ABNORMAL, NOT_EVALUATED, NO
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantBirthExamFormValidator(InfantFormValidatorMixin, FormValidator):

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))
        self.validate_general_activity()
        self.validate_heent_exam()
        self.validate_resp_exam()
        self.validate_cardiac_exam()
        self.validate_abdominal_exam()
        self.validate_skin_exam()
        self.validate_neuro_exam()

    def validate_general_activity(self):
        self.required_if(
            ABNORMAL,
            field='general_activity',
            field_required='abnormal_activity',
            required_msg='If abnormal, please specify.',
            not_required_msg=('You indicated that there was NO abnormality in '
                              'general activity, yet specified abnormality. '
                              'Please correct')
        )

    def validate_heent_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='heent_exam',
            field_required='heent_no_other',
            required_msg=('You indicated that HEENT exam was not normal. '
                          'Provide answer to Q7.'))

    def validate_resp_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='resp_exam',
            field_required='resp_exam_other',
            required_msg=('You indicated that Respiratory exam was not normal. '
                          'Provide answer to Q9.'))

    def validate_cardiac_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='cardiac_exam',
            field_required='cardiac_exam_other',
            required_msg=('You indicated that Cardiac exam was not normal. '
                          'Provide answer to Q11.'))

    def validate_abdominal_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='abdominal_exam',
            field_required='abdominal_exam_other',
            required_msg=('You indicated that Abdominal exam was not normal. '
                          'Provide answer to Q13.'))

    def validate_skin_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='skin_exam',
            field_required='skin_exam_other',
            required_msg=('You indicated that Skin exam was not normal. '
                          'Provide answer to Q15.'))

    def validate_neuro_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='neurologic_exam',
            field_required='neuro_exam_other',
            required_msg=('You indicated that Neurological exam was not normal. '
                          'Provide answer to Q19.'))
