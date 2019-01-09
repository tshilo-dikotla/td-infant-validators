from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, NOT_EVALUATED, ABNORMAL
from edc_form_validators import FormValidator


class InfantFuPhysicalFormValidator(FormValidator):

    infant_fu_physical_model = 'td_infant.infantfuphysical'

    infant_birth_model = 'td_infant.infantbirth'

    registered_subject_model = 'edc_registration.registeredsubject'

    maternal_consent_model = 'td_maternal.subjectconsent'

    @property
    def infant_fu_physical_cls(self):
        return django_apps.get_model(self.infant_fu_physical_model)

    @property
    def infant_birth_cls(self):
        return django_apps.get_model(self.infant_birth_model)

    @property
    def registered_subject_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_consent_model)

    def clean(self):
        self.validate_height_and_head_circum(cleaned_data=self.cleaned_data)
        self.validate_report_datetime(cleaned_data=self.cleaned_data)
        self.validate_general_activity()
        self.validate_heent_exam()
        self.validate_resp_exam()
        self.validate_cardiac_exam()
        self.validate_abdominal_exam()
        self.validate_skin_exam()
        self.validate_neuro_exam()

    def validate_height_and_head_circum(self, cleaned_data=None):
        visit_codes = ['2000', '2010', '2020', '2060',
                       '2120', '2180', '2240', '2300', '2360']
        if (not cleaned_data.get('infant_visit').appointment.visit_code == '2000' and
                not cleaned_data.get('infant_visit').appointment.visit_code == '2010'):
            prev_visit = visit_codes.index(cleaned_data.get(
                'infant_visit').appointment.visit_code) - 1
            while prev_visit > 0:
                try:
                    subject_identifier = cleaned_data.get(
                        'infant_visit').appointment.subject_identifier
                    prev_fu_phy = self.infant_fu_physical_cls.objects.get(
                        infant_visit__appointment__subject_identifier=subject_identifier,
                        infant_visit__appointment__visit_code=visit_codes[prev_visit])
                    if prev_fu_phy.height:
                        if cleaned_data.get('height') < prev_fu_phy.height:
                            msg = {'height':
                                   'You stated that the height for the participant '
                                   'as {}, yet in visit {} you indicated that participant '
                                   'height was {}. Please correct.'.format(
                                       cleaned_data.get(
                                           'height'), visit_codes[prev_visit],
                                       prev_fu_phy.height)}
                            self._errors.update(msg)
                            raise ValidationError(msg)
                    if prev_fu_phy.head_circumference:
                        if cleaned_data.get('head_circumference') < prev_fu_phy.head_circumference:
                            msg = {'head_circumference':
                                   'You stated that the head circumference for the participant as {}, '
                                   'yet in visit {} you indicated that participant height was {}. '
                                   'Please correct.'.format(
                                       cleaned_data.get('head_circumference'),
                                       visit_codes[prev_visit], prev_fu_phy.head_circumference)}
                            self._errors.update(msg)
                            raise ValidationError(msg)
                        break
                except self.infant_fu_physical_cls.DoesNotExist:
                    prev_visit = prev_visit - 1

    def relative_identifier(self, infant_identifier):
        try:
            return self.registered_subject_cls.objects.get(
                subject_identifier=infant_identifier).relative_identifier
        except self.registered_subject_cls.DoesNotExist:
            raise ValidationError('Registered Subject does not exist.')

    def validate_report_datetime(self, cleaned_data=None):
        try:
            subject_identifier = cleaned_data.get(
                'infant_visit').subject_identifier
            infant_birth = self.infant_birth_cls.objects.get(
                subject_identifier=subject_identifier)
            if cleaned_data.get('report_datetime').date() < infant_birth.dob:
                msg = {'report_datetime':
                       'report_datetime can not be before the infant dob.'}
                self._errors.update(msg)
                raise ValidationError(msg)
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
            else:
                raise ValidationError('Maternal Consent form does not exist.')
        except self.infant_birth_cls.DoesNotExist:
            raise ValidationError('Infant Birth does not exist.')

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
                          'Provide answer to Q16.'))

    def validate_skin_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='skin_exam',
            field_required='skin_exam_other',
            required_msg=('You indicated that Skin exam was not normal. '
                          'Provide answer to Q18.'))

    def validate_neuro_exam(self):
        responses = (NO, NOT_EVALUATED)
        self.required_if(
            *responses,
            field='neurologic_exam',
            field_required='neuro_exam_other',
            required_msg=('You indicated that Neurological exam was not normal. '
                          'Provide answer to Q22.'))
