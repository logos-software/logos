from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django_cpf_cnpj.validators import validate_cpf
from localflavor.br.models import BRCPFField, BRStateField

from apps.police.choices import (CorCabeloChoices, CorOlhosChoices,
                                 CorPeleChoices, EscolaridadeChoices,
                                 EstadoCivilChoices, GrauParentescoChoices,
                                 SexoChoices, TipoCabeloChoices,
                                 TipoSanguineoChoices)
from apps.utils.models import BaseModel


class Policial(BaseModel):
    """Modelo para representar dados do Policial"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='policial',
        verbose_name='Usuário',
        help_text='Usuário do sistema associado ao policial'
    )
    matricula = models.CharField(
        'Matrícula',
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(5)]
    )
    nome = models.CharField(
        'Nome Completo',
        max_length=100
    )
    nome_guerra = models.CharField(
        'Nome de Guerra',
        max_length=20
    )
    cpf = BRCPFField(
        'CPF',
        unique=True,
        validators=[validate_cpf]
    )
    rg = models.CharField(
        'RG',
        max_length=20,
        unique=True
    )
    data_nascimento = models.DateField(
        'Data de Nascimento'
    )
    data_inclusao = models.DateField(
        'Data de Inclusão'
    )
    sexo = models.CharField(
        max_length=1,
        choices=SexoChoices.choices
    )
    tipo_sanguineo = models.CharField(
        'Tipo Sanguíneo',
        max_length=3,
        choices=TipoSanguineoChoices.choices,
        null=True,
        blank=True
    )
    estado_civil = models.CharField(
        'Estado Civil',
        max_length=1,
        choices=EstadoCivilChoices.choices
    )

    # Contato
    email = models.EmailField(
        'E-mail Corporativo',
        unique=True
    )
    email_pessoal = models.EmailField(
        'E-mail Pessoal',
        blank=True,
        null=True
    )
    telefone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True
    )
    celular = models.CharField(
        'Celular',
        max_length=20
    )

    # Endereço
    cep = models.CharField(
        'CEP',
        max_length=9
    )
    endereco = models.CharField(
        'Endereço',
        max_length=100
    )
    numero = models.CharField(
        'Número',
        max_length=10
    )
    complemento = models.CharField(
        'Complemento',
        max_length=100,
        blank=True
    )
    bairro = models.CharField(
        'Bairro',
        max_length=50
    )
    cidade = models.CharField(
        'Cidade',
        max_length=50
    )
    uf = BRStateField('UF')

    # Dados Bancários
    banco = models.CharField(
        max_length=3,
        blank=True
    )
    agencia = models.CharField(
        max_length=10,
        blank=True
    )
    conta = models.CharField(
        max_length=20,
        blank=True
    )

    data_falecimento = models.DateField(
        'Data de Falecimento',
        null=True,
        blank=True
    )

    # posto = models.ForeignKey(
    #     'Posto',
    #     on_delete=models.PROTECT,
    #     related_name='policiais'
    # )
    # quadro = models.ForeignKey(
    #     'Quadro',
    #     on_delete=models.PROTECT,
    #     related_name='policiais'
    # )
    # lotacao = models.ForeignKey(
    #     'Lotacao',
    #     on_delete=models.PROTECT,
    #     related_name='policiais'
    # )

    foto = models.ImageField(
        'Foto',
        upload_to='fotos_policiais/%Y/%m/',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Policial'
        verbose_name_plural = 'Policiais'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['matricula']),
            models.Index(fields=['cpf']),
            models.Index(fields=['nome']),
        ]

    def __str__(self):
        return f"{self.matricula} - {self.nome}"

    def clean(self):
        """Validação do modelo"""
        super().clean()

        # Validação do CPF
        if self.cpf:
            self.cpf = ''.join(filter(str.isdigit, self.cpf))

            if len(self.cpf) != 11:
                raise ValidationError({
                    'cpf': 'CPF deve conter 11 dígitos.'
                })

        self.nome = self.nome.upper()
        self.nome_guerra = self.nome_guerra.upper()

    def get_idade(self):
        """Calcula a idade do policial"""
        from datetime import date
        today = date.today()
        return today.year - self.data_nascimento.year - (
            (today.month, today.day) <
            (self.data_nascimento.month, self.data_nascimento.day)
        )

    def save(self, *args, **kwargs):
        """Sobrescrevendo save para garantir sincronização com User"""
        if not self.pk and not hasattr(self, 'user'):
            from django.contrib.auth import get_user_model

            from apps.users.models.auth.choices import (UserStatusChoices,
                                                        UserTypeChoices)

            User = get_user_model()
            user = User.objects.create_user(
                username=self.matricula,
                email=self.email,
                password=None,  # Senha deve ser definida posteriormente
                first_name=self.nome.split()[0],
                last_name=' '.join(self.nome.split()[1:]),
                user_type=UserTypeChoices.POLICE,
                status=UserStatusChoices.ACTIVE
            )
            self.user = user

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Sobrescrevendo delete para inativar o usuário"""
        if self.user:
            from apps.users.models.auth.choices import UserStatusChoices
            self.user.status = UserStatusChoices.INACTIVE
            self.user.save()
        super().delete(*args, **kwargs)


class DadosFisicos(BaseModel):
    """Características físicas do Policial"""
    policial = models.OneToOneField(
        'Policial',
        on_delete=models.CASCADE,
        related_name='dados_fisicos'
    )
    altura = models.DecimalField(
        'Altura (m)',
        max_digits=3,
        decimal_places=2
    )
    peso = models.DecimalField(
        'Peso (kg)',
        max_digits=5,
        decimal_places=2
    )
    tipo_sanguineo = models.CharField(
        'Tipo Sanguíneo',
        max_length=3,
        choices=TipoSanguineoChoices.choices
    )
    cor_olhos = models.CharField(
        'Cor dos Olhos',
        max_length=2,
        choices=CorOlhosChoices.choices
    )
    cor_cabelos = models.CharField(
        'Cor do Cabelo',
        max_length=2,
        choices=CorCabeloChoices.choices
    )
    tipo_cabelos = models.CharField(
        'Tipo do Cabelo',
        max_length=2,
        choices=TipoCabeloChoices.choices
    )
    cor_pele = models.CharField(
        'Cor da Pele',
        max_length=2,
        choices=CorPeleChoices.choices
    )

    class Meta:
        verbose_name = 'Dados Físicos'
        verbose_name_plural = 'Dados Físicos'

    def __str__(self):
        return f"Dados Físicos - {self.policial}"


class Fardamento(BaseModel):
    """Dados de fardamento do Policial"""
    policial = models.OneToOneField(
        'Policial',
        on_delete=models.CASCADE,
        related_name='fardamento'
    )
    manequim = models.CharField(max_length=5, blank=True)
    calcado = models.CharField('Calçado', max_length=2, blank=True)

    class Meta:
        verbose_name = 'Fardamento'
        verbose_name_plural = 'Fardamentos'


class DadosFamiliares(BaseModel):
    """Dados dos familiares do Policial"""
    policial = models.ForeignKey(
        'Policial',
        on_delete=models.CASCADE,
        related_name='familiares'
    )
    nome = models.CharField('Nome Completo', max_length=100)
    grau_parentesco = models.CharField(
        'Grau de Parentesco',
        max_length=2,
        choices=GrauParentescoChoices.choices
    )
    data_nascimento = models.DateField(
        'Data de Nascimento',
        null=True,
        blank=True
    )
    cpf = BRCPFField(
        'CPF',
        null=True,
        blank=True
    )
    rg = models.CharField(
        'RG',
        max_length=20,
        blank=True
    )
    dependente = models.BooleanField(
        'É dependente?',
        default=False
    )
    contato = models.CharField(
        'Telefone/Celular',
        max_length=20,
        blank=True
    )
    observacao = models.TextField(
        'Observações',
        blank=True
    )

    class Meta:
        verbose_name = 'Familiar'
        verbose_name_plural = 'Familiares'
        ordering = ['nome']
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['cpf']),
        ]

    def __str__(self):
        return f"{self.nome} - {self.get_grau_parentesco_display()}"

    def clean(self):
        self.nome = self.nome.upper()


class Escolaridade(BaseModel):
    """Formação acadêmica do Policial"""
    policial = models.ForeignKey(
        'Policial',
        on_delete=models.CASCADE,
        related_name='escolaridades'
    )
    nivel = models.CharField(
        'Nível',
        max_length=2,
        choices=EscolaridadeChoices.choices
    )
    curso = models.CharField(
        'Curso',
        max_length=100,
        blank=True
    )
    instituicao = models.CharField(
        'Instituição',
        max_length=100
    )
    ano_conclusao = models.PositiveIntegerField(
        'Ano de Conclusão',
        null=True,
        blank=True
    )
    data_colacao = models.DateField(
        'Data da Colação',
        null=True,
        blank=True
    )
    registro = models.CharField(
        'Número do Registro',
        max_length=50,
        blank=True
    )
    arquivo_diploma = models.FileField(
        'Diploma/Certificado',
        upload_to='documentos/diplomas/%Y/%m/',
        null=True,
        blank=True
    )
    observacao = models.TextField(
        'Observações',
        blank=True
    )

    class Meta:
        verbose_name = 'Escolaridade'
        verbose_name_plural = 'Escolaridades'
        ordering = ['-ano_conclusao', 'nivel']
        indexes = [
            models.Index(fields=['nivel']),
            models.Index(fields=['ano_conclusao']),
        ]

    def __str__(self):
        return f"{self.get_nivel_display()} - {self.curso}"

    def clean(self):
        self.curso = self.curso.upper()
        self.instituicao = self.instituicao.upper()
