from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO_UNKNOWN_NA, YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)

    visit_instance = models.CharField(max_length=25)


class InfantVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)


class InfantBirthArv(models.Model):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=PROTECT)

    azt_discharge_supply = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN_NA,
        verbose_name="Was the infant discharged with a supply of AZT? ",
        help_text="if infant not yet discharged, please enter 'Not applicable'")


class Panel(models.Model):

    name = models.CharField(max_length=25)


class InfantFuPhysical(models.Model):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=PROTECT)

    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,)

    head_circumference = models.DecimalField(
        max_digits=5,
        decimal_places=2,)


class RegisteredSubject(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50,
        unique=True)

    relative_identifier = models.CharField(
        max_length=36,
        null=True,
        blank=True)


class MaternalConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=50)

    consent_datetime = models.DateTimeField()

    dob = models.DateField()

    version = models.CharField(
        max_length=10,
        editable=False)


class MaternalLabourDel(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    delivery_datetime = models.DateTimeField()


class InfantFuImmunizations(models.Model):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=PROTECT)

    vaccines_received = models.CharField(max_length=25)

    vaccines_missed = models.CharField(max_length=25)


class InfantBirth(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50,
        unique=True)

    dob = models.DateField(null=True,
                           blank=True)

    report_datetime = models.DateTimeField(default=get_utcnow)


class InfantFeeding(BaseUuidModel):

    infant_visit = models.OneToOneField(InfantVisit, on_delete=models.PROTECT)

    is_first_formula = models.CharField(
        verbose_name="Is this the first reporting of infant formula use?",
        max_length=15,
        choices=YES_NO,
        blank=True,
        null=True,)

    date_first_formula = models.DateField(
        verbose_name="Date infant formula introduced?",
        blank=True,
        null=True,
        help_text="provide date if this is first reporting of infant formula")

    est_date_first_formula = models.CharField(
        verbose_name="Is date infant formula introduced estimated?",
        max_length=15,
        choices=YES_NO,
        blank=True,
        null=True,
        help_text="provide date if this is first reporting of infant formula")

    formula_intro_occur = models.CharField(
        verbose_name=(
            "Since the last attended scheduled visit has the child received any solid foods?"),
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE)

    formula_intro_date = models.DateField(
        verbose_name=(
            "Date the infant participant first started receiving solids since the last "
            "attended scheduled visit where an infant feeding form was completed"),
        blank=True,
        null=True)

    report_datetime = models.DateField(
        null=True,
        blank=True)

    most_recent_bm = models.DateField(
        verbose_name="Date of most recent breastfeeding ",
        blank=True,
        null=True)

    def previous_infant_instance(self, infant_visit):
        """Returns previous infant visit"""

        visit = ['2000', '2010', '2030', '2060', '2090', '2120']

        try:
            registered_subject = infant_visit.subject_identifier
            previous_visit_code = visit[visit.index(
                self.infant_visit.visit_code) - 1]
            previous_appointment = Appointment.objects.get(
                subject_identifier=registered_subject,
                visit_code=previous_visit_code)
            return InfantVisit.objects.get(appointment=previous_appointment)
        except Appointment.DoesNotExist:
            return None
        except InfantVisit.DoesNotExist:
            return None
        except AttributeError:
            return None


class SubjectScreening(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)

    has_omang = models.CharField(max_length=3)

    age_in_years = age_in_years = models.IntegerField()


class TdConsentVersion(BaseUuidModel):

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)

    version = models.CharField(max_length=3)

    report_datetime = models.DateField(
        null=True,
        blank=True)


class Foods (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = 'td_infant_validators'
        verbose_name = "Foods"
