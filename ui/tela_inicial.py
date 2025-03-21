from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from database.db_conexao import conectar_banco, listar_empresas

class TelaInicial(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.conexao = conectar_banco()

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
        self.label_titulo = QLabel("Selecione uma empresa")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_titulo)

        self.label_descricao = QLabel("Escolha uma empresa cadastrada ou cadastre uma nova")
        self.label_descricao.setObjectName("descricao")
        self.label_descricao.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_descricao)

        # ComboBox de empresas
        self.combo_empresas = QComboBox()
        self.combo_empresas.setObjectName("comboEmpresas")
        self.combo_empresas.setMinimumHeight(40)
        self.container_layout.addWidget(self.combo_empresas)

        # Linha separadora
        self.linha = QFrame()
        self.linha.setFrameShape(QFrame.HLine)
        self.linha.setFrameShadow(QFrame.Sunken)
        self.container_layout.addWidget(self.linha)

        # Botão prosseguir
        self.botao_prosseguir = QPushButton("Prosseguir")
        self.botao_prosseguir.setObjectName("botaoPrincipal")
        self.botao_prosseguir.setEnabled(False)
        self.botao_prosseguir.setCursor(Qt.PointingHandCursor)
        self.botao_prosseguir.clicked.connect(self.prosseguir_para_tela_principal)
        self.container_layout.addWidget(self.botao_prosseguir)

        self.container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Botão cadastrar nova empresa
        self.botao_cadastrar = QPushButton("➕ Cadastrar nova empresa")
        self.botao_cadastrar.setObjectName("botaoPrimario")
        self.botao_cadastrar.setCursor(Qt.PointingHandCursor)
        self.botao_cadastrar.clicked.connect(self.abrir_tela_cadastro)
        self.container_layout.addWidget(self.botao_cadastrar)

        self.layout.addWidget(self.container)
        self.carregar_empresas()

    def carregar_empresas(self):
        empresas = listar_empresas(self.conexao)
        self.combo_empresas.clear()
        self.combo_empresas.addItem("Selecionar empresa...", None)

        for empresa in empresas:
            self.combo_empresas.addItem(f"{empresa['razao_social']} - {empresa['cnpj']}", empresa)

        self.combo_empresas.currentIndexChanged.connect(self.habilitar_botao_prosseguir)

    def habilitar_botao_prosseguir(self, index):
        self.botao_prosseguir.setEnabled(index > 0)

    def prosseguir_para_tela_principal(self):
        index = self.combo_empresas.currentIndex()
        if index > 0:
            empresa = self.combo_empresas.itemData(index)
            self.main_window.mostrar_tela_principal(empresa)

    def abrir_tela_cadastro(self):
        self.main_window.mostrar_tela_cadastro()

    def showEvent(self, event):
        self.carregar_empresas()
        super().showEvent(event)
