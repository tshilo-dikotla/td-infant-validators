import datetime
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_form_validators import FormValidator

from .form_validator_mixin import InfantFormValidatorMixin


class InfantCovidScreeningFormValidator(InfantFormValidatorMixin,
                                        FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'infant_visit').subject_identifier

        super().clean()

        self.validate_against_visit_datetime(
            self.cleaned_data.get('report_datetime'))

        covid_fields = ['covid_test_date',
                        'is_test_date_estimated',
                        'covid_results']

        for value in covid_fields:
            self.required_if(
                YES,
                field='covid_tested',
                field_required=value)

        self.validate_covid_test_date('covid_test_date')

        household_fields = ['household_test_date',
                            'is_household_test_estimated']

        for value in household_fields:
            self.required_if(
                YES,
                field='household_positive',
                field_required=value)

        self.validate_covid_test_date('household_test_date')

    def validate_covid_test_date(self, test_date):

        year_begin_date = datetime.date(2020, 1, 1)

        test_date_val = self.cleaned_data.get(test_date)

        if (test_date_val and (test_date_val < year_begin_date)):
            msg = {
                test_date: f'Test date cannot be before {year_begin_date}.'}
            self._errors.update(msg)
            raise ValidationError(msg)
