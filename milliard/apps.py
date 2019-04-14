from django.apps import AppConfig


#class MilliardConfig(AppConfig):
#    name = 'milliard'

import re
if re.match (r'^[а-яА-ЯёЁa-zA-Z\s]+$', ' '):
    print (1000)

