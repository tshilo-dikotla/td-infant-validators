from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator


class InfantBirthFormValidator(CrfOffStudyFormValidator, FormValidator):

    registered_subject_model = 'edc_registration.registeredsubject'

    maternal_lab_del_model = 'td_maternal.maternallabourdel'

    @property
    def registered_subject_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def maternal_lab_del_cls(self):
        return django_apps.get_model(self.maternal_lab_del_model)

    def clean(self):
        self.subject_identifier = self.cleaned_data.get('subject_identifier')
        super().clean()

        self.validate_dob()
        self.validate_report_datetime()

    def validate_dob(self):
        cleaned_data = self.cleaned_data
        try:
            maternal_identifier = self.registered_subject_cls.objects.get(
                subject_identifier=cleaned_data.get(
                    'subject_identifier')).relative_identifier
            maternal_lab_del = self.maternal_lab_del_cls.objects.get(
                subject_identifier=maternal_identifier)
            dob = cleaned_data.get('dob')
            if dob != maternal_lab_del.delivery_datetime.date():
                msg = {'dob':
                       'Infant dob must match maternal delivery date. Expected'
                       f' {maternal_lab_del.delivery_datetime.date()}, '
                       f'got {dob}'}
                self._errors.update(msg)
                raise ValidationError(msg)

        except self.registered_subject_cls.DoesNotExist:
            raise ValidationError('Registered Subject does not exist.')
        except self.maternal_lab_del_cls.DoesNotExist:
            raise ValidationError('Cannot find maternal labour and delivery '
                                  'form for this infant! This is not expected.')

    def validate_report_datetime(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('report_datetime') and
                cleaned_data.get('report_datetime').date() < cleaned_data.get('dob')):
            msg = {'report_datetime': 'Infant enrollment date cannot be '
                   'before infant date.'}
            self._errors.update(msg)
        try:
            maternal_identifier = self.registered_subject_cls.objects.get(
                subject_identifier=cleaned_data.get(
                    'subject_identifier')).relative_identifier
        except self.registered_subject_cls.DoesNotExist:
            raise ValidationError('Registered Subject does not exist.')
        else:
            try:
                maternal_lab_del = self.maternal_lab_del_cls.objects.get(
                    subject_identifier=maternal_identifier)
            except self.maternal_lab_del_cls.DoesNotExist:
                raise ValidationError(
                    'Cannot find maternal labour and delivery '
                    'form for this infant! This is not expected.')
                raise ValidationError(msg)
            else:
                report_datetime = cleaned_data.get('report_datetime')
                mld_datetime = localtime(maternal_lab_del.delivery_datetime)

                if (report_datetime and report_datetime < mld_datetime):
                    msg = {'report_datetime':
                           'Infant report datetime must be on or after maternal '
                           f'delivery datetime of {mld_datetime}. '
                           f'Got {report_datetime}'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
