from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow

from ..form_validators import KaraboOffstudyFormValidator
from .models import InfantVisit, Appointment


@tag('karabo_offstudy')
class TestKaraboOffStudyForm(TestCase):

    def setUp(self):
        appointment = Appointment.objects.create(
            subject_identifier='2334432',
            appt_datetime=get_utcnow() - relativedelta(days=4),
            visit_code='2000',
            visit_instance='0')

        self.infant_visit = InfantVisit.objects.create(
            subject_identifier='12345323',
            appointment=appointment,
            report_datetime=get_utcnow() - relativedelta(days=4))

        self.data = {
            'infant_visit': self.infant_visit,
            'report_datetime': get_utcnow(),
            'offstudy_date': get_utcnow().date(),
            'offschedule_datetime': get_utcnow(),
            'reason': 'blahblah',
            'reason_other': None,
            'comment': 'blahblah'
        }

    def test_karabo_form_valid(self):
        karabo_offstudy = KaraboOffstudyFormValidator(
            cleaned_data=self.data)
        try:
            karabo_offstudy.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_other_coughing_rel_required(self):
        offschedule_datetime = self.data.get('offschedule_datetime')
        self.data['offschedule_datetime'] = (
            offschedule_datetime - relativedelta(days=4))
        karabo_offstudy = KaraboOffstudyFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, karabo_offstudy.validate)
