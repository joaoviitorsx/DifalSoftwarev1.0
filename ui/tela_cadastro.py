from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QCheckBox, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QPixmap
from database.db_conexao import conectar_banco, cadastrar_empresa

class TelaCadastro(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.conexao = conectar_banco()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Logo
        self.logo = QLabel(self)
        pixmap = QPixmap("images/logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(250, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        # Container principal
        self.container = QFrame()
        self.container.setObjectName("cardContainer")
        self.container.setFixedWidth(450)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignCenter)

        # Título e descrição
        self.label_titulo = QLabel("Cadastro de Empresa")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_titulo)

        self.label_descricao = QLabel("Preencha os campos abaixo para cadastrar uma nova empresa")
        self.label_descricao.setObjectName("descricao")
        self.label_descricao.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_descricao)

        self.container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Campo CNPJ
        self.label_cnpj = QLabel("CNPJ")
        self.label_cnpj.setObjectName("campoLabel")
        self.container_layout.addWidget(self.label_cnpj)

        self.input_cnpj = QLineEdit()
        self.input_cnpj.setPlaceholderText("00.000.000/0000-00")
        self.input_cnpj.setObjectName("campoInput")
        self.input_cnpj.setAlignment(Qt.AlignCenter)
        self.input_cnpj.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}/[0-9]{4}-[0-9]{2}")))
        self.container_layout.addWidget(self.input_cnpj)

        # Campo Razão Social
        self.label_razao_social = QLabel("Razão Social")
        self.label_razao_social.setObjectName("campoLabel")
        self.container_layout.addWidget(self.label_razao_social)

        self.input_razao_social = QLineEdit()
        self.input_razao_social.setPlaceholderText("Nome da Empresa")
        self.input_razao_social.setObjectName("campoInput")
        self.input_razao_social.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.input_razao_social)

        # Campo Alíquota Interna
        self.label_aliquota = QLabel("Alíquota Interna (%)")
        self.label_aliquota.setObjectName("campoLabel")
        self.container_layout.addWidget(self.label_aliquota)

        self.input_aliquota = QLineEdit()
        self.input_aliquota.setPlaceholderText("Ex: 18.00")
        self.input_aliquota.setObjectName("campoInput")
        self.input_aliquota.setAlignment(Qt.AlignCenter)
        self.input_aliquota.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]+(\\.[0-9]{1,2})?$")))
        self.container_layout.addWidget(self.input_aliquota)

        # Checkbox Telecom
        self.checkbox_telecom = QCheckBox("Empresa de Telecom")
        self.checkbox_telecom.setObjectName("checkboxTelecom")
        self.checkbox_telecom.setCursor(Qt.PointingHandCursor)
        self.container_layout.addWidget(self.checkbox_telecom)

        self.container_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Botões
        self.botoes_container = QFrame()
        self.botoes_layout = QVBoxLayout(self.botoes_container)

        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar.setObjectName("botaoPrincipal")
        self.botao_salvar.setCursor(Qt.PointingHandCursor)
        self.botao_salvar.clicked.connect(self.confirmar_salvar)
        self.botoes_layout.addWidget(self.botao_salvar)

        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setObjectName("botaoSecundario")
        self.botao_voltar.setCursor(Qt.PointingHandCursor)
        self.botao_voltar.clicked.connect(self.voltar_para_tela_inicial)
        self.botoes_layout.addWidget(self.botao_voltar)

        self.container_layout.addWidget(self.botoes_container)
        self.layout.addWidget(self.container)

    def confirmar_salvar(self):
        cnpj = self.input_cnpj.text().strip()
        razao_social = self.input_razao_social.text().strip()
        aliquota_texto = self.input_aliquota.text().strip()
        setor_telecom = "Sim" if self.checkbox_telecom.isChecked() else "Não"

        if not cnpj or not razao_social or not aliquota_texto:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos corretamente.")
            return

        try:
            aliquota = float(aliquota_texto)
            if aliquota <= 0 or aliquota > 100:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Erro", "Alíquota inválida.")
            return

        resposta = QMessageBox.question(
            self, "Confirmação",
            f"Confirmar cadastro?\n\nCNPJ: {cnpj}\nRazão: {razao_social}\nAlíquota: {aliquota}%\nTelecom: {setor_telecom}",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            self.salvar_empresa(cnpj, razao_social, aliquota, setor_telecom)

    def salvar_empresa(self, cnpj, razao_social, aliquota, setor_telecom):
        cadastrar_empresa(self.conexao, cnpj, razao_social, aliquota, setor_telecom)
        QMessageBox.information(self, "Sucesso", "Empresa cadastrada com sucesso!")
        self.voltar_para_tela_inicial()

    def voltar_para_tela_inicial(self):
        self.main_window.mostrar_tela_inicial()
        self.input_cnpj.clear()
        self.input_razao_social.clear()
        self.input_aliquota.clear()
        self.checkbox_telecom.setChecked(False)
