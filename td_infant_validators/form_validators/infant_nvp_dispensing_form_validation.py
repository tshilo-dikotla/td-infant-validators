from django.core.exceptions import ValidationError
from edc_constants.constants import YES, NO
from edc_form_validators import FormValidator

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantNvpDispensingFormValidator(InfantFormValidatorMixin,
                                       CrfOffStudyFormValidator,
                                       FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').appointment.subject_identifier
        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.required_if(
            YES,
            field='nvp_prophylaxis',
            field_required='azt_prophylaxis',
            required_msg=('Was the infant given AZT infant prophylaxis? '
                          'Please answer YES or NO.'),
            inverse=False)
        self.not_required_if(
            YES,
            field='nvp_prophylaxis',
            field_required='reason_not_given',
            not_required_msg='Infant received NVP prophylaxis, do not give reason.'
        )
        self.required_if(
            YES,
            field='nvp_prophylaxis',
            field_required='nvp_admin_date',
            required_msg='Please give the NVP infant prophylaxis date.',
        )
        self.required_if(
            YES,
            field='nvp_prophylaxis',
            field_required='medication_instructions',
            required_msg=('If the Infant received NVP prophylaxis, was the mother '
                          'given instructions on how to administer the medication?'),
            inverse=False
        )
        self.required_if(
            YES,
            field='nvp_prophylaxis',
            field_required='dose_admin_infant',
            required_msg='Please give the NVP prophylaxis dosage information.'
        )
        self.required_if(
            YES,
            field='nvp_prophylaxis',
            field_required='correct_dose',
            required_msg='Was the correct NVP prophylaxis dose given?',
            inverse=False
        )
        self.required_if(
            YES,
            field='azt_prophylaxis',
            field_required='azt_dose_given',
            required_msg=('Infant received AZT prophylaxis, please give the dose'
                          ' administered.'),
            not_required_msg=('Infant did NOT receive AZT prophylaxis, please do'
                              'not give the dose.'))

        self.required_if(
            NO,
            field='correct_dose',
            field_required='corrected_dose'
        )

        self.validate_char_float('azt_dose_given')

    def validate_char_float(self, value):
        if self.cleaned_data.get(value):
            try:
                float_value = float(self.cleaned_data.get(value))
            except ValueError:
                msg = {value: 'Please enter a valid number.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            else:
                if float_value <= 0:
                    msg = {value:
                           'Dose cannot be 0 or less.'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
