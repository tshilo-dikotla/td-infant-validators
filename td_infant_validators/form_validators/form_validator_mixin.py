from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class InfantFormValidatorMixin:

    infant_birth_model = 'td_infant.infantbirth'

    @property
    def infant_birth_cls(self):
        return django_apps.get_model(self.infant_birth_model)

    def validate_against_birth_date(self, infant_identifier=None,
                                    report_datetime=None):

        try:
            infant_birth = self.infant_birth_cls.objects.get(
                subject_identifier=infant_identifier)
        except self.infant_birth_cls.DoesNotExist:
            raise ValidationError(
                'Please complete Infant Birth form '
                f'before  proceeding.')
        else:
            if report_datetime and report_datetime < infant_birth.report_datetime:
                raise forms.ValidationError(
                    "Report datetime cannot be before enrollemt datetime.")

    def validate_against_visit_datetime(self, report_datetime):
        infant_visit = self.cleaned_data.get('infant_visit')
        if report_datetime and report_datetime < infant_visit.report_datetime:
            raise forms.ValidationError(
                "Report datetime cannot be before visit datetime.")
