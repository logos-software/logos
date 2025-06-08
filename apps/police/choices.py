from django.db import models

class FuncaoChoices(models.TextChoices):
    """Choices para o campo tipo da função policial"""
    OPM = 'O', 'Operacional'
    GERAL = 'G', 'Geral'
    ADMINISTRATIVO = 'A', 'Administrativo'

class SexoChoices(models.TextChoices):
    MASCULINO = 'M', 'Masculino'
    FEMININO = 'F', 'Feminino'

class TipoSanguineoChoices(models.TextChoices):
    A_POSITIVO = 'A+', 'A+'
    A_NEGATIVO = 'A-', 'A-'
    B_POSITIVO = 'B+', 'B+'
    B_NEGATIVO = 'B-', 'B-'
    AB_POSITIVO = 'AB+', 'AB+'
    AB_NEGATIVO = 'AB-', 'AB-'
    O_POSITIVO = 'O+', 'O+'
    O_NEGATIVO = 'O-', 'O-'

class EstadoCivilChoices(models.TextChoices):
    SOLTEIRO = 'S', 'Solteiro(a)'
    CASADO = 'C', 'Casado(a)'
    DIVORCIADO = 'D', 'Divorciado(a)'
    VIUVO = 'V', 'Viúvo(a)'

class GrauParentescoChoices(models.TextChoices):
    PAI = 'PA', 'Pai'
    MAE = 'MA', 'Mãe'
    FILHO = 'FI', 'Filho(a)'
    CONJUGE = 'CO', 'Cônjuge'
    IRMAO = 'IR', 'Irmão/Irmã'
    AVO = 'AV', 'Avô/Avó'
    NETO = 'NE', 'Neto(a)'
    OUTRO = 'OU', 'Outro'

class EscolaridadeChoices(models.TextChoices):
    """Choices para níveis de escolaridade"""
    FUNDAMENTAL_INCOMPLETO = 'FI', 'Fundamental Incompleto'
    FUNDAMENTAL_COMPLETO = 'FC', 'Fundamental Completo'
    MEDIO_INCOMPLETO = 'MI', 'Médio Incompleto'
    MEDIO_COMPLETO = 'MC', 'Médio Completo'
    SUPERIOR_INCOMPLETO = 'SI', 'Superior Incompleto'
    SUPERIOR_COMPLETO = 'SC', 'Superior Completo'
    POS_GRADUACAO = 'PG', 'Pós-Graduação'
    MESTRADO = 'ME', 'Mestrado'
    DOUTORADO = 'DO', 'Doutorado'
    POS_DOUTORADO = 'PD', 'Pós-Doutorado'