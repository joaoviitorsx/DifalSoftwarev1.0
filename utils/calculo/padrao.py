from utils.calculo.base import obter_aliquota_interestadual

def calcular(valor_operacao, uf_origem, uf_empresa, aliquota_interna):
    """Calcula o DIFAL padrão, sem regras específicas por estado."""
    if uf_origem == uf_empresa:
        return 0.0

    aliquota_interestadual = obter_aliquota_interestadual(uf_origem)
    icms_origem = valor_operacao * aliquota_interestadual
    base_calculo = (valor_operacao - icms_origem) / (1 - aliquota_interna)
    icms_destino = base_calculo * aliquota_interna

    return icms_destino - icms_or