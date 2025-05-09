"""
Roteador de banco de dados para gerenciar conexões com PostgreSQL e Oracle.
"""


class DatabaseRouter:
    """
    Roteador para direcionar modelos específicos para bancos diferentes.
    Por padrão, usa o PostgreSQL ('default'). Modelos específicos podem ser
    dirigidos para o Oracle ('oracle') conforme necessário.
    """

    def db_for_read(self, model, **hints):
        """
        Direciona leituras para o banco apropriado.
        """
        # Por padrão, todos os modelos vão para o PostgreSQL
        if hasattr(model, '_meta') and hasattr(model._meta, 'app_label'):
            # Exemplo: modelos dentro do app 'legacy' vão para o Oracle
            if model._meta.app_label == 'legacy':
                return 'oracle'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Direciona escritas para o banco apropriado.
        """
        # Mesma lógica do db_for_read
        if hasattr(model, '_meta') and hasattr(model._meta, 'app_label'):
            if model._meta.app_label == 'legacy':
                return 'oracle'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relações entre objetos no mesmo banco.
        """
        # Objetos podem se relacionar se estiverem no mesmo banco
        # ou se ambos estiverem em bancos que usamos
        db_list = ('default', 'oracle')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Define onde as migrações podem ser executadas.
        """
        # Migrações para o app 'legacy' não devem ser aplicadas
        # (normalmente são tabelas já existentes no Oracle)
        if app_label == 'legacy' and db == 'default':
            return False
        
        # Para todos os outros casos, permitimos migrações
        return True
