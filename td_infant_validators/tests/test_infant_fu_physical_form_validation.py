from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, ABNORMAL, NORMAL
from .models import (Appointment, InfantVisit, InfantBirth,
                     InfantFuPhysical, RegisteredSubject, MaternalConsent)
from ..form_validators import InfantFuPhysicalFormValidator


class TestInfantFuPhysicalFormValidator(TestCase):

    def setUp(self):
        subject_identifier = '22334'
        relative_identifier = '12334'
        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000')
        self.infant_visit = InfantVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)

        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2010')
        self.infant_visit = InfantVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)
        InfantFuPhysical.objects.create(
            infant_visit=self.infant_visit,
            height=1200,
            head_circumference=300)
        infant_fu_physical_model = 'td_infant_validators.infantfuphysical'
        InfantFuPhysicalFormValidator.infant_fu_physical_model =\
            infant_fu_physical_model

        InfantBirth.objects.create(
            subject_identifier=subject_identifier,
            dob=(get_utcnow() - relativedelta(months=7)).date())
        infant_birth_model = 'td_infant_validators.infantbirth'
        InfantFuPhysicalFormValidator.infant_birth_model =\
            infant_birth_model

        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2020')
        self.infant_visit = InfantVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)

        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            relative_identifier=relative_identifier)
        registered_subject_model = 'td_infant_validators.registeredsubject'
        InfantFuPhysicalFormValidator.registered_subject_model =\
            registered_subject_model

        MaternalConsent.objects.create(
            subject_identifier=relative_identifier,
            consent_datetime=get_utcnow() - relativedelta(days=10),
            dob=(get_utcnow() - relativedelta(years=23)).date())
        maternal_consent_model = 'td_infant_validators.maternalconsent'
        InfantFuPhysicalFormValidator.maternal_consent_model =\
            maternal_consent_model

    def test_height_not_less_than_prev_fu_phy_height(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow())
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_height_less_than_prev_fu_phy_height_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1000,
            head_circumference=350,
            report_datetime=get_utcnow())
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('height', form_validator._errors)

    def test_head_cmfrnc_not_less_than_prev_fu_phy_cmfrnc(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow())
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_head_cmfrnc_less_than_prev_fu_phy_cmfrnc_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=200,
            report_datetime=get_utcnow())
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('head_circumference', form_validator._errors)

    def test_report_datetime_before_consent_datetime_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow() - relativedelta(days=11))
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('report_datetime', form_validator._errors)

    def test_report_datetime_after_consent_datetime_valid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow())
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_report_datetime_before_infant_dob_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow() - relativedelta(months=11))
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('report_datetime', form_validator._errors)

    def test_report_datetime_after_infant_dob_valid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow())
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_general_activity_abnormal_not_specified(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=ABNORMAL,
            abnormal_activity=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('abnormal_activity', form_validator._errors)

    def test_general_activity_abnormal_specified(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=ABNORMAL,
            abnormal_activity='Some creepy stuff')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_general_activity_normal_abn_activity_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity='Some creepy stuff')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('abnormal_activity', form_validator._errors)

    def test_general_activity_normal_abn_activity_none_valid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_heent_exam_yes_heent_no_other_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            heent_exam=YES,
            heent_no_other='specified')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('heent_no_other', form_validator._errors)

    def test_heent_exam_yes_heent_no_other_none_valid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            heent_exam=YES,
            heent_no_other=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_heent_exam_no_heent_no_other_required(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            heent_exam=NO,
            heent_no_other=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('heent_no_other', form_validator._errors)

    def test_heent_exam_no_heent_no_other_specified(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            heent_exam=NO,
            heent_no_other='specified')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_resp_exam_yes_resp_exam_other_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            resp_exam=YES,
            resp_exam_other='specified')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('resp_exam_other', form_validator._errors)

    def test_resp_exam_yes_resp_exam_other_none_valid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            resp_exam=YES,
            resp_exam_other=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_resp_exam_no_resp_exam_other_required(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            resp_exam=NO,
            resp_exam_other=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('resp_exam_other', form_validator._errors)

    def test_resp_exam_no_resp_exam_other_specified(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            resp_exam=NO,
            resp_exam_other='specified')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_cardiac_exam_yes_cardiac_exam_other_invalid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            cardiac_exam=YES,
            cardiac_exam_other='specified')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cardiac_exam_other', form_validator._errors)

    def test_cardiac_exam_yes_cardiac_exam_other_none_valid(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            cardiac_exam=YES,
            cardiac_exam_other=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_cardiac_exam_no_cardiac_exam_other_required(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            cardiac_exam=NO,
            cardiac_exam_other=None)
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('cardiac_exam_other', form_validator._errors)

    def test_cardiac_exam_no_cardiac_exam_other_specified(self):
        cleaned_data = dict(
            infant_visit=self.infant_visit,
            height=1300,
            head_circumference=350,
            report_datetime=get_utcnow(),
            general_activity=NORMAL,
            abnormal_activity=None,
            cardiac_exam=NO,
            cardiac_exam_other='specified')
        form_validator = InfantFuPhysicalFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
