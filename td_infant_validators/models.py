from django.conf import settings

if settings.APP_NAME == 'td_infant_validators':
    from .tests import models
