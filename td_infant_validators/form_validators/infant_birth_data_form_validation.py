from django.core.exceptions import ValidationError
from edc_constants.constants import (
    NO, NOT_APPLICABLE, UNKNOWN, YES)
from edc_form_validators import FormValidator


class InfantBirthDataFormValidator(FormValidator):

    def clean(self):
        cleaned_data = self.cleaned_data
        self.validate_apgar_score(cleaned_data)

    def validate_apgar_score(self, cleaned_data):
        if cleaned_data.get('apgar_score') == YES:
            if not cleaned_data.get('apgar_score_min_1') == 0:
                if not cleaned_data.get('apgar_score_min_1'):
                    self._errors.update(
                        {'apgar_score_min_1':
                         'If Apgar scored performed, then you should answer At 1 minute(Q7).'
                         })
                    raise ValidationError(
                        'If Apgar scored performed, then you should answer At 1 minute(Q7).')
            if not cleaned_data.get('apgar_score_min_5') == 0:
                if not cleaned_data.get('apgar_score_min_5'):
                    self._errors.update(
                        {'apgar_score_min_5':
                         'If Apgar scored performed, then you should answer At 5 minute(Q8).'
                         })
                    raise ValidationError(
                        'If Apgar scored performed, then you should answer At 5 minute(Q8).')
        else:
            if cleaned_data.get('apgar_score_min_1'):
                self._errors.update(
                    {'apgar_score_min_1':
                        'If Apgar scored was NOT performed, then you should NOT answer at '
                     '1 minute(Q7).'})
                raise ValidationError('If Apgar scored was NOT performed, then you should NOT answer at '
                                      '1 minute(Q7).')
            if cleaned_data.get('apgar_score_min_5'):

                self._errors.update(
                    {'apgar_score_min_5': 'If Apgar scored was NOT performed, then you should NOT answer at 5 '
                     'minute(Q8).'})
                raise ValidationError('If Apgar scored was NOT performed, then you should NOT answer at 5 '
                                      'minute(Q8).')
            if cleaned_data.get('apgar_score_min_10'):
                self._errors.update({'apgar_score_min_10': 'If Apgar scored was NOT performed, then you should NOT answer at 10 '
                                     'minute(Q9).'})
                raise ValidationError('If Apgar scored was NOT performed, then you should NOT answer at 10 '
                                      'minute(Q9).')
