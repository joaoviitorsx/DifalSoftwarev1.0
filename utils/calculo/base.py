ALIQUOTAS_INTERESTADUAIS = {
    "11": 7,  "12": 12, "13": 7,  "14": 12, "15": 7,
    "16": 12, "17": 7,  "21": 12, "22": 7,  "23": 12,
    "24": 12, "25": 12, "26": 12, "27": 12, "28": 12,
    "29": 12, "31": 7,  "32": 12, "33": 7,  "35": 7,
    "41": 7,  "42": 7,  "43": 7,  "50": 7,  "51": 12,
    "52": 12, "53": 12
}

CODIGO_UF = {
    "12": "AC",  "27": "AL",  "13": "AM",  "16": "AP",  "29": "BA",
    "23": "CE",  "53": "DF",  "32": "ES",  "52": "GO",  "21": "MA",
    "51": "MT",  "50": "MS",  "31": "MG",  "15": "PA",  "25": "PB",
    "26": "PE",  "22": "PI",  "41": "PR",  "33": "RJ",  "24": "RN",
    "43": "RS",  "11": "RO",  "14": "RR",  "42": "SC",  "35": "SP",
    "28": "SE",  "17": "TO"
}

def obter_aliquota_interestadual(codigo_uf_origem):
    """Retorna a alíquota interestadual com base no código da UF de origem."""
    return ALIQUOTAS_INTERESTADUAIS.get(codigo_uf_origem, 12) / 100

def obter_codigo_uf(sigla_uf):
    """Retorna o código da UF com base na sigla do estado."""
    for codigo, sigla in CODIGO_UF.items():
        if sigla == sigla_uf:
            return codigo
    return None

def formatar_numero(valor):
    """Converte strings numéricas para float, tratando valores inválidos."""
    if not valor or isinstance(valor, float) or isinstance(valor, int):
        return float(valor) if valor else 0.0
    if isinstance(valor, str):
        valor = valor.strip()
        if valor.lower() in ["não informado", "-", "", "null"]:
            return 0.0
        return float(valor.replace(".", "").replace(",", "."))
    return 0.0

def extrair_info_chave_nfe(chave_nfe):
    """Extrai UF e Ano/Mês da chave de acesso da NF-e."""
    if chave_nfe.startswith("NFe"):
        chave_nfe = chave_nfe[3:] 

    if len(chave_nfe) == 44:  
        uf_codigo = chave_nfe[:2] 
        aa_mm = chave_nfe[2:6] 
        ano = "20" + aa_mm[:2] 
        mes = aa_mm[2:] 
        return uf_codigo, ano, mes

    return "Desconhecido", "", ""