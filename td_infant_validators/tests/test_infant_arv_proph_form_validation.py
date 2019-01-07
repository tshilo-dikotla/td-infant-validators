from django.test import TestCase
from django.utils import timezone
from edc_constants.constants import YES


from tshilo_dikotla.constants import MODIFIED
from .models import InfantVisit


class TestInfantArvProphForm(TestCase):

    def setUp(self):
        self.infant_visit = InfantVisit(appointment=self.appointment)
        self.data = {
            'report_datetime': timezone.now(),
            'infant_visit': self.infant_visit.id,
            'prophylatic_nvp': YES,
            'arv_status': MODIFIED,
        }

    def test_validate_taking_arv_proph_unknown(self):
        pass
