"""
Configurações de produção para o projeto Django.
Otimizado para segurança e performance.
"""

from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# Permitir todos os hosts temporariamente durante o setup inicial
ALLOWED_HOSTS = ['*']  # Mais permissivo durante o setup

# Configuração para arquivos estáticos em produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configurações adicionais do WhiteNoise para melhor performance
WHITENOISE_MAX_AGE = 31536000  # 1 ano em segundos
WHITENOISE_MANIFEST_STRICT = True
WHITENOISE_USE_FINDERS = False  # Desabilita procura de arquivos em desenvolvimento
WHITENOISE_AUTOREFRESH = False  # Desabilita auto-refresh em produção
WHITENOISE_MIMETYPES = {
    'application/font-woff': 'application/octet-stream',
    'application/font-woff2': 'application/octet-stream',
    'application/vnd.ms-fontobject': 'application/octet-stream',
    'application/x-font-ttf': 'application/octet-stream',
    'application/x-font-woff': 'application/octet-stream',
    'font/opentype': 'application/octet-stream',
    'font/woff': 'application/octet-stream',
    'font/woff2': 'application/octet-stream',
}

# Configurações de segurança para produção
SECURE_SSL_REDIRECT = False  # Temporariamente desativado
SESSION_COOKIE_SECURE = False  # Temporariamente desativado
CSRF_COOKIE_SECURE = False  # Temporariamente desativado
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = None  # Temporariamente desativado
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Temporariamente desativado
SECURE_HSTS_PRELOAD = False  # Temporariamente desativado
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Menos restritivo para desenvolvimento

# Configuração para logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',
    },
}

# Email backend para produção
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 25))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False').lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
