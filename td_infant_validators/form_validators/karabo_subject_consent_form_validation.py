from django.apps import apps as django_apps
from django import forms
from django.core.exceptions import ValidationError
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidator


class KaraboSubjectConsentFormValidator(FormValidator):

    maternal_subject_consent = 'td_maternal.subjectconsent'

    def clean(self):

        self.required_if(
            NO,
            field='literacy',
            field_required='witness_name'
        )
        self.validate_maternal_name()
        self.validate_maternal_surname()
        self.validate_maternal_initials()
        self.validate_maternal_omang()
        self.clean_consent_reviewed()
        self.clean_study_questions()
        self.clean_consent_copy()
        self.clean_consent_signature()

    @property
    def maternal_consent_cls(self):
        return django_apps.get_model(self.maternal_subject_consent)

    def validate_maternal_name(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')
        maternal_consent = self.maternal_consent_cls.objects.get(
            subject_identifier)
        if not self.cleaned_data['name'] == maternal_consent.name:
            raise ValidationError(
                {'name': 'Please Enter Maternal Name'
                 ' similar to Tshilo Dikotla'})

    def validate_maternal_surname(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')
        maternal_consent = self.maternal_consent_cls.objects.get(
            subject_identifier)
        if not self.cleaned_data['surname'] == maternal_consent.surname:
            raise ValidationError(
                {'name': 'Please Enter Maternal Surname'
                 ' similar to Tshilo Dikotla'})

    def validate_maternal_initials(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')
        maternal_consent = self.maternal_consent_cls.objects.get(
            subject_identifier)
        if not self.cleaned_data['initials'] == maternal_consent.initials:
            raise ValidationError(
                {'name': 'Please Enter Maternal Initials'
                 ' similar to Tshilo Dikotla'})

    def validate_maternal_omang(self):
        '''Validates maternal name from Tshilo dikotla and Karabo Study
        '''
        subject_identifier = self.cleaned_data.get('subject_identifier')
        maternal_consent = self.maternal_consent_cls.objects.get(
            subject_identifier)
        if not self.cleaned_data['omang'] == maternal_consent.omang:
            raise ValidationError(
                {'name': 'Please Enter Maternal Omang'
                 ' similar to Tshilo Dikotla'})

    def clean_consent_reviewed(self):
        consent_reviewed = self.cleaned_data.get('reviewed')
        if consent_reviewed != YES:
            raise forms.ValidationError(
                'Complete this part of the informed consent process '
                'before continuing.',
                code='invalid')

    def clean_study_questions(self):
        study_questions = self.cleaned_data.get('questions')
        if study_questions != YES:
            raise forms.ValidationError(
                'Complete this part of the informed consent process'
                ' before continuing.',
                code='invalid')

    def clean_consent_copy(self):
        consent_copy = self.cleaned_data.get('offer')
        if consent_copy == NO:
            raise forms.ValidationError(
                'Complete this part of the informed consent process'
                ' before continuing.',
                code='invalid')

    def clean_consent_signature(self):
        consent_signature = self.cleaned_data.get('signed_consent')
        if consent_signature != YES:
            raise forms.ValidationError(
                'Complete this part of the informed consent process'
                ' before continuing.',
                code='invalid')
