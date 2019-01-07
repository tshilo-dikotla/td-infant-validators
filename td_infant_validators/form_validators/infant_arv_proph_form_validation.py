from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from edc_form_validators import FormValidator


class InfantArvProphFormValidator(FormValidator):
    pass