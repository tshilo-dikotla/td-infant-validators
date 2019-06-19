from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class KaraboOffstudyFormValidator(InfantFormValidatorMixin,
                                  FormValidator):

    def clean(self):

        self.validate_other_specify(
            field='reason',
            other_specify_field='reason_other',
        )

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        self.validate_against_visit_date(
            self.cleaned_data.get('offstudy_date'))
