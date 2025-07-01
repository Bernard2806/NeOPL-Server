from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QCheckBox, QLineEdit,
    QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QHeaderView, 
    QGroupBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QIcon, QPixmap
import sys
import os


class LanguageManager:
    """Manejador de idiomas para la interfaz"""
    
    def __init__(self):
        self.current_language = "es"
        self.translations = {
            "es": {
                "title": "NeOPL Server",
                "enable_log": "Activar Log",
                "log_filter": "Filtro de Log",
                "log_autoscroll": "Auto-scroll de Log",
                "clear_log": "Limpiar Log",
                "about": "Acerca de",
                "port": "Puerto",
                "server_stopped": "Servidor detenido (presiona para iniciar)",
                "server_running": "Servidor ejecutándose (presiona para detener)",
                "time": "Hora",
                "event": "Evento",
                "source": "Origen",
                "message": "Mensaje",
                "language": "Idioma"
            },
            "pt": {
                "title": "NeOPL Server",
                "enable_log": "Ativar Log",
                "log_filter": "Filtro de Log",
                "log_autoscroll": "Auto-scroll de Log",
                "clear_log": "Limpar Log",
                "about": "Sobre",
                "port": "Porta",
                "server_stopped": "Servidor parado (pressione para iniciar)",
                "server_running": "Servidor executando (pressione para parar)",
                "time": "Hora",
                "event": "Evento",
                "source": "Origem",
                "message": "Mensagem",
                "language": "Idioma"
            },
            "en": {
                "title": "NeOPL Server",
                "enable_log": "Enable Log",
                "log_filter": "Log Filter",
                "log_autoscroll": "Log Auto-Scroll",
                "clear_log": "Clear Log",
                "about": "About",
                "port": "Port",
                "server_stopped": "Server is stopped (press to start)",
                "server_running": "Server is running (press to stop)",
                "time": "Time",
                "event": "Event",
                "source": "Source",
                "message": "Message",
                "language": "Language"
            }
        }
    
    def get_text(self, key):
        return self.translations[self.current_language].get(key, key)
    
    def set_language(self, language):
        if language in self.translations:
            self.current_language = language


class IconManager:
    """Manejador de iconos para la aplicación"""
    
    @staticmethod
    def create_icon_from_text(text, size=16, color="white"):
        """Crea un icono simple a partir de texto (para cuando no hay archivos de icono)"""
        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(58, 134, 255))  # Color de fondo azul
        
        from PyQt6.QtGui import QPainter, QFont
        painter = QPainter(pixmap)
        painter.setPen(QColor(color))
        
        font = QFont()
        font.setPointSize(size // 2)
        font.setBold(True)
        painter.setFont(font)
        
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
        painter.end()
        
        return QIcon(pixmap)
    
    @staticmethod
    def load_icon(icon_path, fallback_text="?"):
        """Carga un icono desde archivo o crea uno de respaldo"""
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        else:
            return IconManager.create_icon_from_text(fallback_text)
    
    @staticmethod
    def get_system_icon(icon_name):
        """Obtiene iconos del sistema si están disponibles"""
        # Mapeo de nombres a iconos del sistema
        system_icons = {
            "play": "media-playback-start",
            "stop": "media-playback-stop",
            "clear": "edit-clear",
            "about": "help-about",
            "log": "text-x-generic",
            "filter": "view-filter",
            "autoscroll": "go-down",
            "language": "preferences-desktop-locale"
        }
        
        system_name = system_icons.get(icon_name)
        if system_name:
            icon = QIcon.fromTheme(system_name)
            if not icon.isNull():
                return icon
        
        # Si no se encuentra el icono del sistema, crear uno de texto
        fallback_texts = {
            "play": "▶",
            "stop": "⏹",
            "clear": "🗑",
            "about": "?",
            "log": "📝",
            "filter": "🔍",
            "autoscroll": "↓",
            "language": "🌐"
        }
        
        return IconManager.create_icon_from_text(fallback_texts.get(icon_name, "?"))


class OPLServerGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.lang_manager = LanguageManager()
        self.server_running = False
        
        self.setWindowTitle(self.lang_manager.get_text("title"))
        self.resize(800, 500)
        
        # Establecer icono de la aplicación
        self.set_window_icon()
        
        self.init_ui()
        self.apply_modern_theme()

    def set_window_icon(self):
        """Establece el icono de la ventana de la aplicación"""
        # Intentar cargar el icono desde archivo
        icon_path = "app_icon.png"  # o "app_icon.ico"
        
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            # Crear un icono de respaldo
            app_icon = IconManager.create_icon_from_text("N", size=32, color="white")
            self.setWindowIcon(app_icon)

    def apply_modern_theme(self):
        """Aplica una paleta de colores moderna y elegante"""
        modern_palette = QPalette()
        
        # Colores base más modernos y suaves
        # Fondo principal - gris azulado oscuro
        modern_palette.setColor(QPalette.ColorRole.Window, QColor(24, 26, 31))
        modern_palette.setColor(QPalette.ColorRole.WindowText, QColor(225, 228, 232))
        
        # Campos de entrada - negro suave con tinte azul
        modern_palette.setColor(QPalette.ColorRole.Base, QColor(16, 18, 22))
        modern_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(32, 35, 42))
        
        # Texto
        modern_palette.setColor(QPalette.ColorRole.Text, QColor(225, 228, 232))
        modern_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
        
        # Botones - gris medio con tinte azul
        modern_palette.setColor(QPalette.ColorRole.Button, QColor(48, 52, 62))
        modern_palette.setColor(QPalette.ColorRole.ButtonText, QColor(225, 228, 232))
        
        # Destacados - azul moderno y vibrante
        modern_palette.setColor(QPalette.ColorRole.Highlight, QColor(58, 134, 255))
        modern_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        # Tooltips
        modern_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(32, 35, 42))
        modern_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(225, 228, 232))
        
        # Estados deshabilitados
        modern_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(120, 125, 135))
        modern_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(120, 125, 135))
        modern_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(120, 125, 135))
        
        self.setPalette(modern_palette)
        
        # Estilos CSS adicionales para elementos específicos
        self.setStyleSheet("""
            QTableWidget {
                gridline-color: #404448;
                selection-background-color: #3A86FF;
                alternate-background-color: #2A2D35;
            }
            
            QTableWidget::item:selected {
                background-color: #3A86FF;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #30343E;
                padding: 8px;
                border: 1px solid #404448;
                font-weight: bold;
            }
            
            QPushButton {
                padding: 8px 16px;
                border: 1px solid #404448;
                border-radius: 4px;
                background-color: #30343E;
                text-align: left;
            }
            
            QPushButton:hover {
                background-color: #3A86FF;
                border-color: #3A86FF;
            }
            
            QPushButton:pressed {
                background-color: #2C75E6;
            }
            
            QLineEdit {
                padding: 4px 8px;
                border: 1px solid #404448;
                border-radius: 3px;
                background-color: #101216;
            }
            
            QLineEdit:focus {
                border-color: #3A86FF;
            }
            
            QComboBox {
                padding: 4px 8px;
                border: 1px solid #404448;
                border-radius: 3px;
                background-color: #30343E;
            }
            
            QComboBox:hover {
                border-color: #3A86FF;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #E1E4E8;
                width: 0;
                height: 0;
                border-top: 4px solid #E1E4E8;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: none;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #404448;
                border-radius: 3px;
                background-color: #101216;
            }
            
            QCheckBox::indicator:checked {
                background-color: #3A86FF;
                border-color: #3A86FF;
            }
            
            QCheckBox::indicator:checked:after {
                content: "✓";
                color: white;
                font-weight: bold;
            }
        """)

    def init_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.connect_signals()

    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Selector de idioma
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Español", "Português", "English"])
        self.language_combo.setCurrentText("Español")
        
        self.language_label = QLabel(self.lang_manager.get_text("language"))
        
        # Botones de log con iconos
        self.enable_log = QPushButton(self.lang_manager.get_text("enable_log"))
        self.enable_log.setIcon(IconManager.get_system_icon("log"))
        
        self.log_filter = QCheckBox(self.lang_manager.get_text("log_filter"))
        # Los checkboxes no suelen tener iconos, pero se puede añadir si se desea
        
        self.log_autoscroll = QCheckBox(self.lang_manager.get_text("log_autoscroll"))
        self.log_autoscroll.setChecked(True)
        
        self.clear_log = QPushButton(self.lang_manager.get_text("clear_log"))
        self.clear_log.setIcon(IconManager.get_system_icon("clear"))
        
        self.about = QPushButton(self.lang_manager.get_text("about"))
        self.about.setIcon(IconManager.get_system_icon("about"))

        # Puerto y servidor
        self.port_label = QLabel(self.lang_manager.get_text("port"))
        self.port_input = QLineEdit("1024")
        self.port_input.setFixedWidth(80)

        self.server_button = QPushButton(self.lang_manager.get_text("server_stopped"))
        self.server_button.setIcon(IconManager.get_system_icon("play"))
        self.server_button.setMinimumWidth(250)

        # Tabla de logs
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.update_table_headers()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)

    def create_layouts(self):
        """Crea y organiza los layouts"""
        # Layout del selector de idioma
        language_layout = QHBoxLayout()
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch()

        # Layout de controles de log
        log_controls_layout = QHBoxLayout()
        log_controls_layout.addWidget(self.enable_log)
        log_controls_layout.addWidget(self.log_filter)
        log_controls_layout.addWidget(self.log_autoscroll)
        log_controls_layout.addWidget(self.clear_log)
        log_controls_layout.addWidget(self.about)
        log_controls_layout.addStretch()

        # Layout de servidor
        server_layout = QHBoxLayout()
        server_layout.addWidget(self.port_label)
        server_layout.addWidget(self.port_input)
        server_layout.addWidget(self.server_button)

        # Layout superior combinado
        top_layout = QVBoxLayout()
        top_layout.addLayout(language_layout)
        
        controls_layout = QHBoxLayout()
        controls_layout.addLayout(log_controls_layout)
        controls_layout.addLayout(server_layout)
        top_layout.addLayout(controls_layout)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        self.setLayout(main_layout)

    def connect_signals(self):
        """Conecta las señales de los widgets"""
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.server_button.clicked.connect(self.toggle_server)

    def change_language(self, language_text):
        """Cambia el idioma de la interfaz"""
        language_map = {
            "Español": "es",
            "Português": "pt", 
            "English": "en"
        }
        
        lang_code = language_map.get(language_text, "es")
        self.lang_manager.set_language(lang_code)
        self.update_interface_text()

    def update_interface_text(self):
        """Actualiza todos los textos de la interfaz"""
        self.setWindowTitle(self.lang_manager.get_text("title"))
        
        self.language_label.setText(self.lang_manager.get_text("language"))
        self.enable_log.setText(self.lang_manager.get_text("enable_log"))
        self.log_filter.setText(self.lang_manager.get_text("log_filter"))
        self.log_autoscroll.setText(self.lang_manager.get_text("log_autoscroll"))
        self.clear_log.setText(self.lang_manager.get_text("clear_log"))
        self.about.setText(self.lang_manager.get_text("about"))
        self.port_label.setText(self.lang_manager.get_text("port"))
        
        # Actualiza el texto del botón del servidor
        server_text = "server_running" if self.server_running else "server_stopped"
        self.server_button.setText(self.lang_manager.get_text(server_text))
        
        self.update_table_headers()

    def update_table_headers(self):
        """Actualiza los encabezados de la tabla"""
        headers = [
            self.lang_manager.get_text("time"),
            self.lang_manager.get_text("event"),
            self.lang_manager.get_text("source"),
            self.lang_manager.get_text("message")
        ]
        self.table.setHorizontalHeaderLabels(headers)

    def toggle_server(self):
        """Alterna el estado del servidor"""
        self.server_running = not self.server_running
        server_text = "server_running" if self.server_running else "server_stopped"
        self.server_button.setText(self.lang_manager.get_text(server_text))
        
        # Cambiar el icono del botón según el estado
        icon_name = "stop" if self.server_running else "play"
        self.server_button.setIcon(IconManager.get_system_icon(icon_name))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configura el estilo de la aplicación
    app.setStyle('Fusion')  # Estilo más moderno

    window = OPLServerGUI()
    window.show()

    sys.exit(app.exec())