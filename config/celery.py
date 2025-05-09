"""
Configuração do Celery para tarefas assíncronas.
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Definir variável de ambiente para configurações
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

# Criar instância do Celery
app = Celery('logoss')

# Usar configurações do Django para o Celery
# namespace='CELERY' significa que todas as configurações do Celery
# devem ter o prefixo CELERY_ no arquivo settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar tarefas automaticamente de todos os apps registrados
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """Tarefa para debug do Celery."""
    print(f'Request: {self.request!r}')
