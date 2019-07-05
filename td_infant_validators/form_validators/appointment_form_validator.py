from edc_form_validators import FormValidator

from edc_appointment.form_validators import (
    AppointmentFormValidator as BaseAppointmentFormValidator)


class AppointmentFormValidator(BaseAppointmentFormValidator, FormValidator):

    appointment_model = 'td_infant.appointment'

    def clean(self):
        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get('subject_identifier')
        super().clean()

    def validate_appt_new_or_complete(self):
        pass
