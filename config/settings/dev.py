"""
Configurações de desenvolvimento para o projeto Django.
"""

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-development-key-for-testing-only')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# CORS settings para desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True

# Debug Toolbar
INTERNAL_IPS = ['127.0.0.1', '::1']

# Email backend para desenvolvimento
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuração simplificada para arquivos estáticos em desenvolvimento
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuração para migrations
MIGRATION_MODULES = {
    'sites': 'django.contrib.sites.migrations',
}

# Ativar o Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}