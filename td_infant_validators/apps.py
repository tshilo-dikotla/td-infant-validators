from django.apps import AppConfig as DjangoAppconfig
from django.conf import settings


class AppConfig(DjangoAppconfig):
    name = 'td_infant_validators'
    verbose_name = 'Tshilo Dikotla Infant Form Validators'


if settings.APP_NAME == 'td_infant_validators':

    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_metadata.apps import AppConfig as MetadataAppConfig

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'td_infant': ('infant_visit', 'td_infant.infantvisit')}

    class EdcMetadataAppConfig(MetadataAppConfig):
        reason_field = {'infant_visit.infantvisit': 'reason'}

    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}
