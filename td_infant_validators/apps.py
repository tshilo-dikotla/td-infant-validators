from django.apps import AppConfig as DjangoApponfig
# from edc_visit_tracking.apps import (
#     AppConfig as BaseEdcVisitTrackingAppConfig)


class AppConfig(DjangoApponfig):
    name = 'td_infant_validators'
    verbose_name = 'Tshilo Dikotla Infant Form Validators'


# class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
#     visit_models = {
#         'td_infant': ('infant_visit', 'td_infant.infantvisit')}
