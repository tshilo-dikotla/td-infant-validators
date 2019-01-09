from django.apps import AppConfig as DjangoAppconfig
from django.conf import settings


class AppConfig(DjangoAppconfig):
    name = 'td_infant_validators'
    verbose_name = 'Tshilo Dikotla Infant Form Validators'