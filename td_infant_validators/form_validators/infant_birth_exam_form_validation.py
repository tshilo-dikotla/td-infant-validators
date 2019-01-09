from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.constants import ABNORMAL, NOT_EVALUATED, NO


class InfantBirthExamFormValidator(FormValidator):

    registered_subject_model = 'edc_registration.registeredsubject'

    maternal_consent_model = 'td_maternal.subjectconsent'

    @property
    def registered_subject_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    def clean(self):
        self.validate_report_datetime(cleaned_data=self.cleaned_data)
        self.validate_general_activity()
        self.validate_heent_exam()
        self.validate_resp_exam()
        self.validate_cardiac_exam()
        self.validate_abdominal_exam()
        self.validate_skin_exam()
        self.validate_neuro_exam()

    def relative_identifier(self, infant_identifier):
        return self.registered_subject_cls.objects.get(
            subject_identifier=infant_identifier).relative_identifier

    def validate_report_datetime(self, cleaned_data=None):
        relative_identifier = self.relative_identifier(
            cleaned_data.get('infant_visit').subject_identifier)
        maternal_consent = self.maternal_consent_cls.objects.filter(
            subject_identifier=relative_identifier).order_by('consent_datetime').last()
        if maternal_consent:
            if cleaned_data.get('report_datetime') < maternal_consent.consent_datetime:
                msg = {'report_datetime':
                       'report_datetime CANNOT be before consent datetime'}
                self._errors.update(msg)
                raise ValidationError(msg)
            if cleaned_data.get('report_datetime').date() < maternal_consent.dob:
                msg = {'report_datetime':
                       'report_datetime CANNOT be before dob'}
                self._errors.update(msg)
                raise ValidationError(msg)
        else:
            raise ValidationError('Maternal Consent form does not exist.')

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
