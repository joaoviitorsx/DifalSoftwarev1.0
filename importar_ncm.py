import pandas as pd
import mysql.connector
from database.db_conexao import conectar_banco

def importar_planilha_ncm(caminho_arquivo):
    try:
        df = pd.read_excel(caminho_arquivo)
        df.columns = df.columns.str.strip().str.upper()

        if "NCM 2" not in df.columns or "DESCRIÇÃO" not in df.columns or "TERMINO" not in df.columns:
            print("❌ A planilha não contém as colunas esperadas: 'NCM 2', 'DESCRIÇÃO', 'TERMINO'")
            return

        dados = []
        for _, linha in df.iterrows():
            codigo = str(linha["NCM 2"]).replace(".", "").strip()
            descricao = str(linha["DESCRIÇÃO"]).strip()
            paga_difal = linha["TERMINO"] == 0
            dados.append((codigo, descricao, paga_difal))

        conexao = conectar_banco()
        cursor = conexao.cursor()

        for codigo, descricao, paga_difal in dados:
            try:
                cursor.execute("""
                    INSERT INTO ncm_difal (codigo_ncm, descricao, paga_difal)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        descricao = VALUES(descricao),
                        paga_difal = VALUES(paga_difal)
                """, (codigo, descricao, paga_difal))
            except mysql.connector.Error as err:
                print(f"Erro ao inserir NCM {codigo}: {err}")

        conexao.commit()
        cursor.close()
        conexao.close()

        print("✅ Importação de NCMs concluída com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao importar planilha: {e}")

def ncm_paga_difal(codigo_ncm):
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("SELECT paga_difal FROM ncm_difal WHERE codigo_ncm = %s", (codigo_ncm,))
        resultado = cursor.fetchone()
        cursor.close()
        conexao.close()
        return resultado[0] if resultado else False
    except mysql.connector.Error as err:
        print(f"Erro ao verificar NCM {codigo_ncm}: {err}")
        return False

if __name__ == "__main__":
    importar_planilha_ncm(r"C:\Users\viana\OneDrive\Área de Trabalho\Projetos\DIFAL\planilhas\NCM.xlsx")

    codigo_teste = "85177900"
    if ncm_paga_difal(codigo_teste):
        print(f"✅ esta presente no banco de dados.")
        print(f"✅ O NCM {codigo_teste} paga DIFAL.")
    else:
        print(f"❌ O NCM {codigo_teste} não paga DIFAL.")
