from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator


class InfantBirthFormValidator(FormValidator):

    registered_subject_model = 'edc_registration.registeredsubject'

    maternal_lab_del_model = 'td_maternal.maternallabourdel'

    @property
    def registered_subject_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def maternal_lab_del_cls(self):
        return django_apps.get_model(self.maternal_lab_del_model)

    def clean(self):
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
            if not dob == maternal_lab_del.delivery_datetime.date():
                msg = {'dob':
                       'Infant dob must match maternal delivery date of'
                       f' {maternal_lab_del.delivery_datetime.date()}. '
                       f'You wrote {dob}'}
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
                   'before infant date of birth.'}
            self._errors.update(msg)
            raise ValidationError(msg)
