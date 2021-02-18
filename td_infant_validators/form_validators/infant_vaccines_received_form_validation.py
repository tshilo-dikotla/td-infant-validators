from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class VaccinesReceivedFormValidator(InfantFormValidatorMixin,
                                    FormValidator):

    infant_birth_model = 'td_infant.infantbirth'

    @property
    def infant_birth_cls(self):
        return django_apps.get_model(self.infant_birth_model)

    def clean(self):
        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_vaccine_received(cleaned_data=self.cleaned_data)
        self.validate_date_not_before_birth(cleaned_data=self.cleaned_data)
        self.validate_received_vaccine_fields(cleaned_data=self.cleaned_data)
        self.validate_vaccination_at_birth(cleaned_data=self.cleaned_data)
        self.validate_hepatitis_vaccine(cleaned_data=self.cleaned_data)
        self.validate_dpt_vaccine(cleaned_data=self.cleaned_data)
        self.validate_haemophilus_vaccine(cleaned_data=self.cleaned_data)
        self.validate_pcv_vaccine(cleaned_data=self.cleaned_data)
        self.validate_polio_vaccine(cleaned_data=self.cleaned_data)
        self.validate_rotavirus_vaccine(cleaned_data=self.cleaned_data)
        self.validate_measles_vaccine(cleaned_data=self.cleaned_data)
        self.validate_pentavalent_vaccine(cleaned_data=self.cleaned_data)
        self.validate_vitamin_a_vaccine(cleaned_data=self.cleaned_data)
        self.validate_ipv_vaccine(cleaned_data=self.cleaned_data)
        self.validate_diptheria_tetanus_vaccine(cleaned_data=self.cleaned_data)

    def validate_vaccine_received(self, cleaned_data=None):
        condition = cleaned_data.get(
            'infant_fu_immunizations').vaccines_received == YES
        self.required_if_true(
            condition,
            field_required='received_vaccine_name',
            required_msg=('You mentioned that vaccines were received. Please '
                          'indicate which ones on the table.')
        )

    def validate_date_not_before_birth(self, cleaned_data=None):
        infant_identifier = cleaned_data.get(
            'infant_fu_immunizations').infant_visit.subject_identifier
        try:
            infant_birth = self.infant_birth_cls.objects.get(
                subject_identifier=infant_identifier)
            infant_birth_date = infant_birth.dob
            if (cleaned_data.get('date_given') and
                    cleaned_data.get('date_given') < infant_birth_date):
                msg = {'date_given':
                       'Vaccine date cannot be before infant date of birth.'}
                self._errors.update(msg)
                raise ValidationError(msg)
        except self.infant_birth_cls.DoesNotExist:
            raise ValidationError('Infant Birth Form has not been completed.')

    def validate_received_vaccine_fields(self, cleaned_data=None):
        fields_required = ('date_given', 'infant_age')
        for required in fields_required:
            self.required_if_not_none(
                field='received_vaccine_name',
                field_required=required,
                required_msg=('You provided a vaccine name {}. {} field '
                              'is required. Please correct'.format(
                                  cleaned_data.get('received_vaccine_name'),
                                  required)),
            )

    def validate_vaccination_at_birth(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'BCG':
            if cleaned_data.get('infant_age') not in ['At Birth', 'After Birth']:
                msg = {'infant_age':
                       'BCG vaccination is ONLY given at birth or few'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_hepatitis_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'Hepatitis_B':
            if cleaned_data.get('infant_age') not in ['At Birth', '2', '3', '4', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'Hepatitis B can only be administered '
                       'at birth or 2 or 3 or 4 months of infant life'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_dpt_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'DPT':
            if cleaned_data.get('infant_age') not in ['2', '3', '4', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'DPT. Diphtheria, Pertussis and Tetanus can only '
                       'be administered at 2 or 3 or 4 months ONLY.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_haemophilus_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'Haemophilus_influenza':
            if cleaned_data.get('infant_age') not in ['2', '3', '4', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'Haemophilus Influenza B vaccine can only be given '
                       'at 2 or 3 or 4 months of infant life.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_pcv_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'PCV_Vaccine':
            if cleaned_data.get('infant_age') not in ['2', '3', '4', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'The PCV [Pneumonia Conjugated Vaccine], can ONLY be '
                       'administered at 2 or 3 or 4 months of infant life.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_polio_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'Polio':
            if cleaned_data.get('infant_age') not in ['2', '3', '4', '18', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'Polio vaccine can only be administered at '
                       '2 or 3 or 4 or 18 months of infant life'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_rotavirus_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'Rotavirus':
            if cleaned_data.get('infant_age') not in ['2', '3', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'Rotavirus is only administered at 2 or 3 months '
                       'of infant life'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_measles_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'Measles':
            if cleaned_data.get('infant_age') not in ['9', '18', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'Measles vaccine is only administered at 9 or 18 '
                       'months of infant life.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_pentavalent_vaccine(self, cleaned_data=None):
        if (cleaned_data.get('received_vaccine_name') == 'Pentavalent' and
                cleaned_data.get('infant_age') not in ['2', '3', '4', 'catch_up_vaccine']):
            msg = {'infant_age':
                   'The Pentavalent vaccine can only be administered '
                   'at 2 or 3 or 4 months of infant life.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_vitamin_a_vaccine(self, cleaned_data=None):
        if (cleaned_data.get('received_vaccine_name') == 'Vitamin_A' and
                cleaned_data.get('infant_age') not in ['6-11', '9', '9-12',
                                                       '12-17', '18', '18-29',
                                                       '24-29', '30-35',
                                                       '36-41', '42-47',
                                                       'catch_up_vaccine']):
            msg = {'infant_age':
                   'Vitamin A is given to children between 6-41 months '
                   'of life'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_ipv_vaccine(self, cleaned_data=None):
        if (cleaned_data.get('received_vaccine_name') == 'inactivated_polio_vaccine' and
                cleaned_data.get('infant_age') not in ['4', '9-12', 'catch_up_vaccine']):
            msg = {'infant_age':
                   'IPV vaccine is only given at 4 Months. '
                   'of life or 9-12 months'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_diptheria_tetanus_vaccine(self, cleaned_data=None):
        if cleaned_data.get('received_vaccine_name') == 'diphtheria_tetanus':
            if cleaned_data.get('infant_age') not in ['18', 'catch_up_vaccine']:
                msg = {'infant_age':
                       'Measles vaccine is only administered at 18 '
                       'months of infant life.'}
                self._errors.update(msg)
                raise ValidationError(msg)
