import mysql.connector
from mysql.connector import Error
from utils.mensagem import mensagem_error, mensagem_info

HOST = "localhost"
USER = "root"
PASSWORD = "assertivus123#"
DATABASE = "empresas_db"

def conectar_banco():
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port="3306"
        )
        criar_banco(conexao)
        conexao.close()

        conexao = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port="3306",
            database=DATABASE
        )
        criar_tabelas(conexao)
        return conexao

    except mysql.connector.Error as err:
        mensagem_error(f"Erro ao conectar ao banco de dados: {err}")


def criar_banco(conexao):
    cursor = conexao.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        conexao.commit()
    except mysql.connector.Error as err:
        mensagem_error(f"Erro ao criar o banco de dados: {err}")
        conexao.rollback()
    finally:
        cursor.close()


def criar_tabelas(conexao):
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empresas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cnpj VARCHAR(20) UNIQUE NOT NULL,
                razao_social VARCHAR(255) NOT NULL,
                aliquota_interna DECIMAL(5,2) NOT NULL,
                is_telecom BOOLEAN NOT NULL,
                estado VARCHAR(2) NOT NULL,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ncm_difal (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo_ncm VARCHAR(10) NOT NULL UNIQUE,
                descricao TEXT,
                paga_difal BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)

        conexao.commit()
    except mysql.connector.Error as err:
        mensagem_error(f"Erro ao criar tabelas: {err}")
        conexao.rollback()
    finally:
        cursor.close()


def cadastrar_empresa(conexao, cnpj, razao_social, aliquota, is_telecom):
    cursor = conexao.cursor()
    try:
        estado = cnpj[:2]  # Pega os 2 primeiros dígitos do CNPJ como código UF
        cursor.execute("""
            INSERT INTO empresas (cnpj, razao_social, aliquota_interna, is_telecom, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (cnpj, razao_social, aliquota, is_telecom == "Sim", estado))
        conexao.commit()
    except mysql.connector.IntegrityError:
        mensagem_error("CNPJ já cadastrado!")
    except mysql.connector.Error as err:
        mensagem_error(f"Erro ao cadastrar empresa: {err}")
    finally:
        cursor.close()


def listar_empresas(conexao):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, cnpj, razao_social, aliquota_interna, is_telecom, estado
        FROM empresas
        ORDER BY razao_social
    """)
    empresas = cursor.fetchall()
    cursor.close()
    return empresas


def fechar_banco(conexao):
    if conexao and conexao.is_connected():
        conexao.close()