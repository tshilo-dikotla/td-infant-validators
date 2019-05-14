from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from edc_constants.constants import YES, OTHER
from ..form_validators import KaraboTBHistoryFormValidator


@tag('karabo_history')
class TestKaraboTBHistoryForm(TestCase):

    def setUp(self):
        self.data = {
            'coughing': YES,
            'coughing_rel': OTHER,
            'other_coughing_rel': None,
            'fever': YES,
            'fever_rel': OTHER,
            'other_fever_rel': 'Father',
            'weight_loss': YES,
            'weight_loss_rel': '',
            'other_weight_loss': '',
            'night_sweats': YES,
            'night_sweats_rel': OTHER,
            'other_night_sweats': '',
            'diagnosis': YES,
            'diagnosis_rel': YES,
            'other_diagnosis_rel': OTHER,
            'tb_exposure': YES,
            'tb_exposure_det': ''
        }

    def test_other_coughing_rel_required(self):
        tb_history = KaraboTBHistoryFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, tb_history.validate)

    def test_other_fever_rel_required(self):
        self.data['other_fever_rel'] = None
        tb_history = KaraboTBHistoryFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, tb_history.validate)

    def test_other_weight_loss_rel_required(self):
        self.data['weight_loss_rel'] = None
        tb_history = KaraboTBHistoryFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, tb_history.validate)

    def test_other_night_sweats_rel_required(self):
        self.data['night_sweats_rel'] = None
        tb_history = KaraboTBHistoryFormValidator(
            cleaned_data=self.data)
        self.assertRaises(ValidationError, tb_history.validate)
