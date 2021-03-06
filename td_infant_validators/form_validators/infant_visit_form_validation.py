from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_action_item.site_action_items import site_action_items
from edc_constants.constants import ON_STUDY, NEW, NO, OFF_STUDY, YES, OTHER
from edc_constants.constants import PARTICIPANT, ALIVE, DEAD
from edc_form_validators import FormValidator
from edc_visit_tracking.constants import COMPLETED_PROTOCOL_VISIT
from edc_visit_tracking.constants import SCHEDULED, LOST_VISIT, MISSED_VISIT
from edc_visit_tracking.form_validators import VisitFormValidator
from td_prn.action_items import INFANTOFF_STUDY_ACTION

from .crf_offstudy_form_validator import CrfOffStudyFormValidator
from .form_validator_mixin import InfantFormValidatorMixin


class InfantVisitFormValidator(VisitFormValidator, CrfOffStudyFormValidator,
                               InfantFormValidatorMixin, FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.report_datetime = cleaned_data.get('report_datetime')

        self.subject_identifier = self.cleaned_data.get(
            'appointment').subject_identifier
        super().clean()

        self.validate_against_birth_date(infant_identifier=self.subject_identifier,
                                         report_datetime=self.report_datetime)

        self.validate_other_specify('information_provider')

        self.validate_study_status()

        self.validate_covid_visit_not_present()

        self.validate_death()

        self.validate_is_present()

        self.validate_last_alive_date()

        self.validate_is_karabo_eligible()

    def validate_covid_visit_not_present(self):
        if (self.cleaned_data.get('covid_visit') == YES
                and self.cleaned_data.get('is_present') == YES):
            msg = {'is_present': 'This visit is indicated as a telephonic '
                   'visit occurring during COVID-19. The participant cannot '
                   'be present.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_is_karabo_eligible(self):
        karabo_consent_model_cls = django_apps.get_model(
            'td_maternal.karabosubjectconsent')

        karabo_screening_model_cls = django_apps.get_model(
            'td_maternal.karabosubjectscreening')
        try:
            karabo_screening = karabo_screening_model_cls.objects.get(
                subject_identifier=self.subject_identifier[:-3])
        except karabo_screening_model_cls.DoesNotExist:
            pass
        else:
            if karabo_screening.is_eligible:
                try:
                    karabo_consent_model_cls.objects.get(
                        subject_identifier=self.subject_identifier[:-3])
                except karabo_consent_model_cls.DoesNotExist:
                    msg = {'__all__': 'Participant is eligible for Karabo '
                           'sub-study, please complete Karabo subject consent '
                           'first.'}
                    self._errors.update(msg)
                    raise ValidationError(msg)

    def validate_data_collection(self):
        if (self.cleaned_data.get('reason') == SCHEDULED
                and self.cleaned_data.get('study_status') == ON_STUDY
                and self.cleaned_data.get('require_crfs') == NO):
            msg = {'require_crfs': 'This field must be yes if participant'
                   'is on study and present.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_is_present(self):

        reason = self.cleaned_data.get('reason')

        if (reason == LOST_VISIT and
                self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant has been lost to follow up, '
                   'study status should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        if (reason == COMPLETED_PROTOCOL_VISIT and
                self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant is completing protocol, '
                   'study status should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if self.cleaned_data.get('is_present') == YES:
            if self.cleaned_data.get('info_source') != PARTICIPANT:
                raise forms.ValidationError(
                    {'info_source': 'Source of information must be from '
                     'participant if participant is present.'})

    def validate_death(self):
        if (self.cleaned_data.get('survival_status') == DEAD
                and self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant is deceased, study status '
                   'should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        if self.cleaned_data.get('survival_status') != ALIVE:
            if (self.cleaned_data.get('is_present') == YES
                    or self.cleaned_data.get('info_source') == PARTICIPANT):
                msg = {'survival_status': 'Participant cannot be present or '
                       'source of information if their survival status is not'
                       'alive.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_last_alive_date(self):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        infant_birth = self.validate_against_birth_date(
            infant_identifier=self.subject_identifier,
            report_datetime=self.report_datetime)
        last_alive_date = self.cleaned_data.get('last_alive_date')
        if last_alive_date and last_alive_date < infant_birth.report_datetime.date():
            msg = {'last_alive_date': 'Date cannot be before birth date'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_reason_and_info_source(self):
        pass

    def validate_study_status(self):
        infant_offstudy_cls = django_apps.get_model(
            'td_prn.infantoffstudy')
        action_cls = site_action_items.get(
            infant_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item = action_item_model_cls.objects.get(
                subject_identifier=self.cleaned_data.get(
                    'appointment').subject_identifier,
                action_type__name=INFANTOFF_STUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                infant_offstudy_cls.objects.get(
                    subject_identifier=self.cleaned_data.get('appointment').subject_identifier)
            except infant_offstudy_cls.DoesNotExist:
                pass
            else:
                if self.cleaned_data.get('study_status') == ON_STUDY:
                    raise forms.ValidationError(
                        {'study_status': 'Participant has been taken offstudy.'
                         ' Cannot be indicated as on study.'})
        else:
            if (action_item.parent_reference_model_obj
                and self.cleaned_data.get(
                    'report_datetime') >= action_item.parent_reference_model_obj.report_datetime):
                raise forms.ValidationError(
                    'Participant is scheduled to go offstudy.'
                    ' Cannot edit visit until offstudy form is completed.')

    def validate_required_fields(self):

        self.required_if(
            MISSED_VISIT,
            field='reason',
            field_required='reason_missed')

        self.required_if(
            OTHER,
            field='info_source',
            field_required='info_source_other')
