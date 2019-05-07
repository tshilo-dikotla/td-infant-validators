from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, ABNORMAL
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantFuPhysicalFormValidator(InfantFormValidatorMixin, FormValidator):

    infant_fu_physical_model = 'td_infant.infantfuphysical'

    @property
    def infant_fu_physical_cls(self):
        return django_apps.get_model(self.infant_fu_physical_model)

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_height_and_head_circum(cleaned_data=self.cleaned_data)

        self.required_if(
            ABNORMAL,
            field='general_activity',
            field_required='abnormal_activity',
            required_msg='If abnormal, please specify.',
            not_required_msg=('You indicated that there was NO abnormality in '
                              'general activity, yet specified abnormality. '
                              'Please correct')
        )

        responses = (NO, 'Not_evaluated')

        self.required_if(
            *responses,
            field='heent_exam',
            field_required='heent_no_other',
            required_msg=('You indicated that HEENT exam was not normal. '
                          'Provide answer to Q7.'))

        responses = (NO, 'Not_evaluated')
        self.required_if(
            *responses,
            field='resp_exam',
            field_required='resp_exam_other',
            required_msg=('You indicated that Respiratory exam was not normal. '
                          'Provide answer to Q9.'))

        responses = (NO, 'Not_evaluated')
        self.required_if(
            *responses,
            field='cardiac_exam',
            field_required='cardiac_exam_other',
            required_msg=('You indicated that Cardiac exam was not normal. '
                          'Provide answer to Q11.'))

        self.required_if(
            *responses,
            field='abdominal_exam',
            field_required='abdominal_exam_other',
            required_msg=('You indicated that Abdominal exam was not normal. '
                          'Provide answer to Q16.'))

        self.required_if(
            *responses,
            field='skin_exam',
            field_required='skin_exam_other',
            required_msg=('You indicated that Skin exam was not normal. '
                          'Provide answer to Q18.'))

        self.required_if(
            *responses,
            field='neurologic_exam',
            field_required='neuro_exam_other',
            required_msg=('You indicated that Neurological exam was not normal. '
                          'Provide answer to Q22.'))

    def validate_height_and_head_circum(self, cleaned_data=None):
        visit_codes = ['2000', '2010', '2020', '2060',
                       '2120', '2180', '2240', '2300', '2360']

        if (cleaned_data.get('infant_visit').appointment.visit_code
                not in ['2000', '2010']):

            prev_visit = visit_codes.index(cleaned_data.get(
                'infant_visit').appointment.visit_code) - 1

            while prev_visit > 0:
                try:
                    subject_identifier = cleaned_data.get(
                        'infant_visit').appointment.subject_identifier
                    prev_fu_phy = self.infant_fu_physical_cls.objects.get(
                        infant_visit__appointment__subject_identifier=subject_identifier,
                        infant_visit__appointment__visit_code=visit_codes[prev_visit])
                except self.infant_fu_physical_cls.DoesNotExist:
                    prev_visit = prev_visit - 1
                else:
                    if prev_fu_phy.height:
                        height = cleaned_data.get('height')
                        if cleaned_data.get('height') < prev_fu_phy.height:
                            msg = {'height':
                                   'You stated that the height for the '
                                   f'participant as '
                                   f'{height}, yet in '
                                   f'visit {visit_codes[prev_visit]} you '
                                   'indicated that participant '
                                   'height was {prev_fu_phy.height}. Please '
                                   'correct.'}
                            self._errors.update(msg)
                            raise ValidationError(msg)
                    if prev_fu_phy.head_circumference:
                        head_circumference = cleaned_data.get(
                            'head_circumference')
                        if (cleaned_data.get('head_circumference')
                                < prev_fu_phy.head_circumference):
                            msg = {'head_circumference':
                                   'You stated that the head circumference for'
                                   f' the participant as {head_circumference},'
                                   f' yet in visit {visit_codes[prev_visit]} '
                                   'you indicated that participant height was '
                                   f'{prev_fu_phy.head_circumference}. '
                                   'Please correct.'}
                            self._errors.update(msg)
                            raise ValidationError(msg)
                        break
