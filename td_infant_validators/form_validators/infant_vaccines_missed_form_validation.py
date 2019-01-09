from edc_constants.constants import YES
from edc_form_validators import FormValidator


class VaccinesMissedFormValidator(FormValidator):

    def clean(self):
        self.validate_vaccine_missed(cleaned_data=self.cleaned_data)
        self.validate_missed_vaccine_fields(cleaned_data=self.cleaned_data)

    def validate_vaccine_missed(self, cleaned_data=None):
        condition = cleaned_data.get(
            'infant_fu_immunizations').vaccines_missed == YES
        self.required_if_true(
            condition,
            field_required='missed_vaccine_name',
            required_msg=('You mentioned that vaccines were missed. Please '
                          'indicate which ones on the table.'),
        )

    def validate_missed_vaccine_fields(self, cleaned_data=None):
        self.required_if_not_none(
            field='missed_vaccine_name',
            field_required='reason_missed',
            required_msg=('You said {} vaccine was missed. Give a reason'
                          ' for missing this vaccine'.format(
                              cleaned_data.get('missed_vaccine_name')))
        )
