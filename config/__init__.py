"""
Configuração do Celery para o projeto.
"""

# Isso vai garantir que o app seja sempre importado quando Django iniciar
from __future__ import absolute_import, unicode_literals

# Esta linha irá fazer com que o celery sempre encontre e carregue o app
# from .celery import app as celery_app

# __all__ = ('celery_app',)