import os
import xmltodict
import pandas as pd
from PySide6.QtWidgets import QMessageBox, QFileDialog, QLineEdit, QLabel
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from utils.calculo import calcular_difal
from utils.calculo.base import formatar_numero, extrair_info_chave_nfe
from database.db_conexao import conectar_banco

def ncm_tributavel(ncm, conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM ncm_difal WHERE codigo_ncm = %s", (ncm,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado is not None

def processar_nfes(pasta_xmls, empresa, progresso, janela):
    if not os.path.isdir(pasta_xmls):
        QMessageBox.warning(janela, "Erro", "A pasta selecionada não é válida.")
        return

    arquivos_xml = [os.path.join(pasta_xmls, f) for f in os.listdir(pasta_xmls) if f.endswith(".xml")]
    if not arquivos_xml:
        QMessageBox.warning(janela, "Erro", "Nenhum arquivo XML encontrado na pasta.")
        return

    resultados = []
    conexao = conectar_banco()
    total = len(arquivos_xml)

    for i, caminho in enumerate(arquivos_xml):
        try:
            with open(caminho, "rb") as f:
                dic_arquivo = xmltodict.parse(f, process_namespaces=False)
                infos_nf = dic_arquivo.get('nfeProc', {}).get('NFe', {}).get('infNFe', {})
                if not infos_nf:
                    raise ValueError("XML inválido ou estrutura não suportada.")

                produtos = infos_nf.get('det', [])
                if not isinstance(produtos, list):
                    produtos = [produtos]

                for produto in produtos:
                    prod = produto.get('prod', {})
                    imposto = produto.get('imposto', {})

                    ncm = prod.get('NCM', '00000000')
                    ncm = ncm.replace(".", "")
                    if not ncm_tributavel(ncm, conexao):
                        difal_status = "NÃO"
                        vr_difal = 0.0
                    else:
                        valor_item = formatar_numero(prod.get('vProd', '0'))
                        uf_origem, ano, mes = extrair_info_chave_nfe(infos_nf.get('@Id', ''))
                        vr_difal = calcular_difal(empresa['estado'], valor_item, uf_origem, empresa['estado'], empresa['aliquota_interna'] / 100)
                        difal_status = "SIM" if vr_difal > 0 else "NÃO"

                    resultados.append({
                        "ANO": ano,
                        "MÊS": mes,
                        "PARTIC": infos_nf.get('dest', {}).get('xNome', ''),
                        "CNPJ": infos_nf.get('dest', {}).get('CNPJ', ''),
                        "IND_OP": infos_nf.get('ide', {}).get('indFinal', ''),
                        "CFOP": prod.get('CFOP', ''),
                        "NF": infos_nf.get('ide', {}).get('nNF', ''),
                        "UF": uf_origem,
                        "% ORIGEM": '',
                        "% DESTINO": '',
                        "CHAVE NFE": infos_nf.get('@Id', ''),
                        "CODIGO": prod.get('cProd', ''),
                        "DESCRICAO": prod.get('xProd', ''),
                        "NCM": ncm,
                        "DIFAL": difal_status,
                        "VR ITEM": prod.get('vProd', ''),
                        "VR DESC": prod.get('vDesc', '0'),
                        "ICMS ORIGEM": '',
                        "ICMS DESTINO": '',
                        "VR DIFAL": vr_difal
                    })

        except Exception as e:
            print(f"Erro ao processar {caminho}: {e}")

        progresso.setValue(int((i + 1) / total * 100))

    df_resultado = pd.DataFrame(resultados)
    caminho_saida, _ = QFileDialog.getSaveFileName(janela, "Salvar Planilha de Cálculos", "", "Planilhas Excel (*.xlsx)")
    if caminho_saida:
        df_resultado.to_excel(caminho_saida, index=False)
        QMessageBox.information(janela, "Concluído", "Planilha gerada com sucesso!")
        abrir = QMessageBox.question(janela, "Abrir Arquivo", "Deseja abrir a planilha?", QMessageBox.Yes | QMessageBox.No)
        if abrir == QMessageBox.Yes:
            os.startfile(caminho_saida)

    progresso.setValue(0)
