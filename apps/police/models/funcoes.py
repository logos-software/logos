from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from apps.police.choices import FuncaoChoices
from apps.utils.models import BaseModel


class GrupoFuncao(BaseModel):
    """
    Modelo para representar grupos de funções policiais
    """
    nome = models.CharField(
        'Nome do Grupo',
        max_length=50,
        unique=True,
        help_text='Nome do grupo de função'
    )

    class Meta:
        verbose_name = 'Grupo de Função'
        verbose_name_plural = 'Grupos de Funções'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Funcao(BaseModel):
    """
    Modelo para representar funções policiais
    """
    nome = models.CharField(
        'Nome da Função',
        max_length=50,
        help_text='Nome da função policial'
    )
    grupo = models.ForeignKey(
        GrupoFuncao,
        on_delete=models.PROTECT,
        related_name='funcoes',
        verbose_name='Grupo de Função'
    )
    tipo = models.CharField(
        max_length=1,
        choices=FuncaoChoices.choices,
        default=FuncaoChoices.GERAL
    )

    class Meta:
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['tipo']),
        ]

    def __str__(self):
        return f"{self.nome} - {self.grupo.nome}"

    def clean(self):
        """Validações personalizadas"""
        if not self.nome:
            raise ValidationError('O nome da função é obrigatório')


class HistoricoFuncao(BaseModel):
    """
    Modelo para registrar o histórico de funções do policial
    """
    policial = models.ForeignKey(
        'police.Policial',
        on_delete=models.PROTECT,
        related_name='historico_funcoes',
        verbose_name='Policial'
    )
    funcao = models.ForeignKey(
        'Funcao',
        on_delete=models.PROTECT,
        related_name='historicos',
        verbose_name='Função'
    )
    data_inicio = models.DateField(
        'Data Início',
        default=timezone.now
    )
    data_fim = models.DateField(
        'Data Fim',
        null=True,
        blank=True
    )
    matricula_sad = models.CharField(
        'Matrícula SAD',
        max_length=20,
        blank=True,
        null=True,
        help_text='Matrícula no Sistema de Administração'
    )
    documento_numero = models.CharField(
        'Número do Documento',
        max_length=100,
        help_text='Número/Descrição do documento que designou a função (ex: BOL PM Nº 001/2025)'
    )
    documento_arquivo = models.FileField(
        'Arquivo do Documento',
        upload_to='documentos/funcoes/%Y/%m/',
        null=True,
        blank=True,
        help_text='Arquivo digital do documento (PDF, DOC, etc)'
    )
    observacao = models.TextField(
        'Observações',
        blank=True
    )

    class Meta:
        verbose_name = 'Histórico de Função'
        verbose_name_plural = 'Históricos de Funções'
        ordering = ['-data_inicio', '-data_fim']
        indexes = [
            models.Index(fields=['data_inicio']),
            models.Index(fields=['data_fim']),
            models.Index(fields=['matricula_sad']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(data_fim__isnull=True) | models.Q(data_fim__gt=models.F('data_inicio')),
                name='data_fim_maior_que_inicio'
            )
        ]

    def __str__(self):
        return f"{self.policial.nome} - {self.funcao.nome} ({self.documento_numero})"

    def clean(self):
        """Validações personalizadas"""
        super().clean()
        
        # Validações existentes
        if self.data_fim and self.data_fim < self.data_inicio:
            raise ValidationError({
                'data_fim': 'A data fim não pode ser anterior à data início'
            })

        # Verificar sobreposição de períodos
        sobreposicao = HistoricoFuncao.objects.filter(
            policial=self.policial,
            data_inicio__lte=self.data_fim or timezone.now(),
            data_fim__gte=self.data_inicio
        ).exclude(pk=self.pk)

        if sobreposicao.exists():
            raise ValidationError(
                'Existe sobreposição com outro período de função para este policial'
            )

        # Validação do arquivo do documento
        if self.documento_arquivo:
            ext = self.documento_arquivo.name.split('.')[-1].lower()
            allowed_extensions = ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']
            if ext not in allowed_extensions:
                raise ValidationError({
                    'documento_arquivo': f'Formato de arquivo não permitido. Use: {", ".join(allowed_extensions)}'
                })

    @property
    def esta_ativo(self):
        """Verifica se é a função atual do policial"""
        return not self.data_fim or self.data_fim >= timezone.now().date()

    def encerrar(self, data_fim=None):
        """Encerra a função na data especificada"""
        self.data_fim = data_fim or timezone.now().date()
        self.save()
