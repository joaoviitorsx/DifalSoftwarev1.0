from db_conexao import conectar_banco

if __name__ == "__main__":
    conexao = conectar_banco()
    if conexao:
        print("Banco de dados e tabelas prontos.")
        conexao.close()
