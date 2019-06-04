from django import forms
from django.apps import apps as django_apps
from edc_constants.constants import NEW, NO

from edc_action_item.site_action_items import site_action_items
from td_prn.action_items import INFANTOFF_STUDY_ACTION
from td_prn.action_items import INFANT_DEATH_REPORT_ACTION


class InfantCRFFormValidator:

    def clean(self):
        if self.instance and not self.instance.id:
            self.validate_offstudy_model()
        super().clean()

    def validate_offstudy_model(self):
        infant_offstudy_cls = django_apps.get_model(
            'td_prn.infantoffstudy')
        action_cls = site_action_items.get(
            infant_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        self.infant_visit = self.cleaned_data.get('infant_visit') or None

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                action_type__name=INFANTOFF_STUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                infant_offstudy_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except infant_offstudy_cls.DoesNotExist:
                pass
            else:
                raise forms.ValidationError(
                    'Participant has been taken offstudy. Cannot capture any '
                    'new data.')
        else:
            if not self.infant_visit or self.infant_visit.require_crfs == NO:
                raise forms.ValidationError(
                    'Participant is scheduled to be taken offstudy without '
                    'any new data collection. Cannot capture any new data.')
