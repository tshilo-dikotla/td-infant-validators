from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator


class InfantNvpDispensingFormValidator(FormValidator):

    def clean(self):
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

        if self.cleaned_data.get('azt_dose_given'):
            try:
                azt_dose_given = float(self.cleaned_data.get('azt_dose_given'))
            except ValueError:
                msg = {'azt_dose_given': 'Please enter a valid number.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            else:
                if azt_dose_given <= 0:
                    msg = {'azt_dose_given':
                           'Dose cannot be 0 or less.'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
