from django.core.exceptions import ValidationError
from django.db import models
from localflavor.br.models import BRStateField

from apps.utils.models import BaseModel


class Documento(BaseModel):
    """Modelo base para documentos"""
    numero = models.CharField('Número', max_length=50)
    data_emissao = models.DateField('Data de Emissão', null=True, blank=True)
    data_validade = models.DateField('Data de Validade', null=True, blank=True)
    arquivo = models.FileField(
        'Arquivo',
        upload_to='documentos/%Y/%m/',
        null=True,
        blank=True
    )
    observacao = models.TextField('Observação', blank=True)

    class Meta:
        abstract = True


class CNH(Documento):
    """CNH do Policial"""
    CATEGORIAS = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'),
        ('D', 'D'), ('E', 'E'),
        ('AB', 'AB'), ('AC', 'AC'), ('AD', 'AE')
    ]

    policial = models.OneToOneField(
        'Policial',
        on_delete=models.CASCADE,
        related_name='cnh'
    )
    categoria = models.CharField(
        'Categoria',
        max_length=2,
        choices=CATEGORIAS
    )

    class Meta:
        verbose_name = 'CNH'
        verbose_name_plural = 'CNHs'


class RG(Documento):
    """RG do Policial"""
    policial = models.ForeignKey(
        'Policial',
        on_delete=models.CASCADE,
        related_name='rgs'
    )
    orgao_emissor = models.CharField('Órgão Emissor', max_length=10)
    tipo = models.CharField(
        max_length=10,
        choices=[('CIVIL', 'Civil'), ('MILITAR', 'Militar')]
    )

    class Meta:
        verbose_name = 'RG'
        verbose_name_plural = 'RGs'


class TituloEleitor(Documento):
    """Título de Eleitor do Policial"""
    policial = models.OneToOneField(
        'Policial',
        on_delete=models.CASCADE,
        related_name='titulo_eleitor'
    )
    zona = models.CharField('Zona Eleitoral', max_length=5)
    secao = models.CharField('Seção Eleitoral', max_length=5)

    class Meta:
        verbose_name = 'Título de Eleitor'
        verbose_name_plural = 'Títulos de Eleitor'


class Reservista(Documento):
    """Certificado de Reservista do Policial"""
    CATEGORIA_CHOICES = [
        ('1', '1ª Categoria'),
        ('2', '2ª Categoria'),
        ('3', '3ª Categoria'),
        ('D', 'Dispensado'),
    ]

    SERIE_CHOICES = [
        ('A', 'Série A'),
        ('B', 'Série B'),
        ('C', 'Série C'),
    ]

    policial = models.OneToOneField(
        'Policial',
        on_delete=models.CASCADE,
        related_name='reservista'
    )
    categoria = models.CharField(
        'Categoria',
        max_length=1,
        choices=CATEGORIA_CHOICES
    )
    serie = models.CharField(
        'Série',
        max_length=1,
        choices=SERIE_CHOICES
    )
    csm = models.CharField(
        'CSM/Região Militar',
        max_length=10
    )
    ra = models.CharField(
        'RA/Unidade Militar',
        max_length=20,
        help_text='Registro de Alistamento'
    )
    situacao_militar = models.CharField(
        'Situação Militar',
        max_length=50,
        blank=True
    )
    data_incorporacao = models.DateField(
        'Data de Incorporação',
        null=True,
        blank=True
    )
    data_desincorporacao = models.DateField(
        'Data de Desincorporação',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Certificado de Reservista'
        verbose_name_plural = 'Certificados de Reservista'
        indexes = [
            models.Index(fields=['categoria']),
            models.Index(fields=['numero']),
        ]

    def __str__(self):
        return f"Reservista {self.numero} - {self.get_categoria_display()}"

    def clean(self):
        """Validações personalizadas"""
        super().clean()
        self.situacao_militar = self.situacao_militar.upper()

        if self.data_incorporacao and self.data_desincorporacao:
            if self.data_desincorporacao < self.data_incorporacao:
                raise ValidationError({
                    'data_desincorporacao': 'A data de desincorporação não pode ser anterior à data de incorporação.'
                })


class CertidaoNascimento(Documento):
    """Certidão de Nascimento do Policial"""
    policial = models.OneToOneField(
        'Policial',
        on_delete=models.CASCADE,
        related_name='certidao_nascimento'
    )
    livro = models.CharField(
        'Livro',
        max_length=10
    )
    folha = models.CharField(
        'Folha',
        max_length=10
    )
    termo = models.CharField(
        'Termo',
        max_length=10
    )
    cartorio = models.CharField(
        'Cartório',
        max_length=100
    )
    cidade = models.CharField(
        'Cidade',
        max_length=100
    )
    uf = BRStateField('UF')
    nacionalidade = models.CharField(
        'Nacionalidade',
        max_length=50,
        default='BRASILEIRA'
    )
    nome_pai = models.CharField(
        'Nome do Pai',
        max_length=100,
        blank=True
    )
    nome_mae = models.CharField(
        'Nome da Mãe',
        max_length=100
    )

    class Meta:
        verbose_name = 'Certidão de Nascimento'
        verbose_name_plural = 'Certidões de Nascimento'
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['nome_mae']),
        ]

    def __str__(self):
        return f"Certidão de Nascimento {self.numero} - {self.policial.nome}"

    def clean(self):
        """Validações personalizadas"""
        super().clean()
        self.cartorio = self.cartorio.upper()
        self.cidade = self.cidade.upper()
        self.nacionalidade = self.nacionalidade.upper()
        self.nome_pai = self.nome_pai.upper()
        self.nome_mae = self.nome_mae.upper()
