from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils.ler_arquivos import processar_nfes
import re

class TelaPrincipal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.empresa = None
        self.pasta_xmls = None

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
        self.container.setFixedWidth(550)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignCenter)

        # Título
        self.label_titulo = QLabel("Processamento de XMLs")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_titulo)

        # Descrição
        self.label_descricao = QLabel("Selecione a pasta contendo os arquivos XML de NF-e")
        self.label_descricao.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_descricao)

        self.container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Informações da empresa
        self.info_empresa_container = QFrame()
        self.info_empresa_container.setObjectName("infoEmpresaContainer")
        self.info_empresa_container.setFrameShape(QFrame.StyledPanel)
        self.info_empresa_layout = QHBoxLayout(self.info_empresa_container)

        self.info_empresa_text_layout = QVBoxLayout()
        self.label_empresa = QLabel("Empresa")
        self.label_empresa.setObjectName("empresaNome")
        self.label_empresa.setAlignment(Qt.AlignLeft)
        self.info_empresa_text_layout.addWidget(self.label_empresa)

        self.label_cnpj = QLabel("CNPJ: --.--")
        self.label_cnpj.setObjectName("empresaCNPJ")
        self.label_cnpj.setAlignment(Qt.AlignLeft)
        self.info_empresa_text_layout.addWidget(self.label_cnpj)

        self.info_empresa_layout.addLayout(self.info_empresa_text_layout)

        self.label_aliquota = QLabel("Alíquota: --%")
        self.label_aliquota.setObjectName("aliquotaDestaque")
        self.label_aliquota.setAlignment(Qt.AlignRight)
        self.info_empresa_layout.addWidget(self.label_aliquota)

        self.container_layout.addWidget(self.info_empresa_container)

        # Upload da pasta com XMLs
        self.upload_container = self.criar_card_upload(
            "Pasta de XMLs", "Clique para selecionar a pasta com os arquivos XML",
            self.selecionar_pasta_xmls
        )
        self.container_layout.addWidget(self.upload_container)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(20)
        self.container_layout.addWidget(self.progress_bar)

        # Botão de processar
        self.botao_processar = QPushButton("Processar XMLs")
        self.botao_processar.setObjectName("botaoProcessar")
        self.botao_processar.setCursor(Qt.PointingHandCursor)
        self.botao_processar.clicked.connect(self.processar)
        self.container_layout.addWidget(self.botao_processar)

        # Botão voltar
        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setObjectName("botaoVoltar")
        self.botao_voltar.setCursor(Qt.PointingHandCursor)
        self.botao_voltar.clicked.connect(self.voltar_para_tela_inicial)
        self.container_layout.addWidget(self.botao_voltar)

        self.layout.addWidget(self.container)

    def criar_card_upload(self, titulo, descricao, funcao_click):
        card = QFrame()
        card.setObjectName("uploadCard")
        card_layout = QVBoxLayout(card)

        label_titulo = QLabel(titulo)
        label_titulo.setObjectName("uploadTitulo")
        label_titulo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(label_titulo)

        label_descricao = QLabel(descricao)
        label_descricao.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(label_descricao)

        botao = QPushButton("📂 Selecionar pasta")
        botao.setCursor(Qt.PointingHandCursor)
        botao.setObjectName("botaoUpload")
        botao.clicked.connect(funcao_click)
        card_layout.addWidget(botao)

        return card

    def formatar_cnpj(self, cnpj):
        cnpj_limpo = re.sub(r'\D', '', cnpj)
        if len(cnpj_limpo) == 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj

    def definir_dados(self, empresa):
        self.empresa = empresa
        self.label_empresa.setText(empresa['razao_social'])
        self.label_cnpj.setText(f"CNPJ: {self.formatar_cnpj(empresa['cnpj'])}")
        self.label_aliquota.setText(f"Alíquota: {empresa['aliquota_interna']}%")

    def selecionar_pasta_xmls(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta com XMLs")
        if pasta:
            self.pasta_xmls = pasta
            QMessageBox.information(self, "Pasta Selecionada", f"Pasta com XMLs: {pasta}")

    def processar(self):
        if not self.pasta_xmls:
            QMessageBox.warning(self, "Erro", "Selecione a pasta com os arquivos XML.")
            return
        processar_nfes(self.pasta_xmls, self.empresa, self.progress_bar, self)

    def voltar_para_tela_inicial(self):
        self.main_window.mostrar_tela_inicial()
