import sys  # Import the sys module to interact with the system
import os  # Import the os module for interacting with the operating system
import logging  # Import the logging module for logging errors and messages
import pymysql  # Import pymysql for MySQL database connectivity
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QSpacerItem, QSizePolicy, QMessageBox, QFileDialog, QStackedWidget, QDesktopWidget
)  # Import necessary PyQt5 widgets
from PyQt5.QtGui import QFont, QColor  # Import QFont for setting fonts and QColor for colors
from PyQt5.QtCore import Qt  # Import Qt for alignment and other constants
from PyQt5.QtWidgets import QGraphicsDropShadowEffect  # Import QGraphicsDropShadowEffect for shadow effects
import sqlalchemy as sal  # Import SQLAlchemy for database interactions
import pandas as pd  # Import pandas for data manipulation
import qtawesome as qta  # Import QtAwesome for icons

# Setup logging
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


class DatabaseApp(QWidget):
    def __init__(self):
        """
        Constructor method that initializes the DatabaseApp class.
        """
        super().__init__()
        self.initUI()
        self.conn = None  # Initialize the database connection as None
        self.table_name = None  # Initialize the table name as None

    def initUI(self):
        """
        Method to initialize the user interface.
        """
        self.setWindowTitle('SQL Manager 📊')  # Set the window title
        self.setGeometry(0, 0, 600, 750)  # Set the window size
        self.center_window()  # Center the window
        self.setStyleSheet("background-color: #e0f7fa;")  # Set the background color

        # Create a QStackedWidget to hold multiple pages
        self.stacked_widget = QStackedWidget(self)

        # Create the first and second pages
        self.page1 = QWidget()
        self.page2 = QWidget()
        self.create_page1()  # Create the UI for the first page
        self.create_page2()  # Create the UI for the second page

        # Add the pages to the stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        # Set the first page as the initial page
        self.stacked_widget.setCurrentIndex(0)

        # Set the layout for the main widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        self.show()  # Explicitly show the window

    def center_window(self):
        """
        Center the application window on the screen.
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_shadow_effect(self, blur_radius=10, color=QColor(0, 0, 0, 160), offset=(2, 2)):
        """
        Create a drop shadow effect with the specified parameters.
        """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setColor(color)
        shadow.setOffset(*offset)
        return shadow

    def create_styled_button(self, text, click_handler, icon_name=None):
        """
        Create a QPushButton with the specified text and click handler, applying a common style and shadow effect.
        """
        button_style = """
            QPushButton {
                background-color: #1E88E5;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 12px;
                font-family: Verdana;
                min-width: 10px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: 2px solid #1E88E5;
            }
        """
        button = QPushButton(text)
        button.clicked.connect(click_handler)
        button.setStyleSheet(button_style)
        button.setGraphicsEffect(self.create_shadow_effect(blur_radius=15, offset=(3, 3)))
        if icon_name:
            button.setIcon(qta.icon(icon_name, color='white'))
        return button

    def create_page1(self):
        """
        Create the first page for database connection.
        """
        # Create input fields for database connection details
        self.dialect_edit = self.create_input_field('Enter SQL Dialect (e.g., mysql)')
        self.driver_edit = self.create_input_field('Enter SQL Driver (e.g., pymysql)')
        self.username_edit = self.create_input_field('Enter Username')
        self.password_edit = self.create_input_field('Enter Password', password=True)
        self.host_edit = self.create_input_field('Enter Host Address (e.g., localhost)')
        self.port_edit = self.create_input_field('Enter Port Number (e.g., 3306)')
        self.database_edit = self.create_input_field('Enter Database Name')
        self.table_edit = self.create_input_field('Enter Table Name (optional)')

        # Create the "Connect to Database" button
        self.connect_button = self.create_styled_button('Connect to Database', self.connect_to_database, 'fa5s.database')

        # Create the title label for the app
        app_title_label = QLabel('SQL Manager 📊')
        app_title_label.setFont(QFont('Arial', 24, QFont.Bold))
        app_title_label.setStyleSheet("color: #1E88E5;")
        app_title_label.setAlignment(Qt.AlignCenter)

        # Create section labels
        section_font = QFont('Verdana', 16, QFont.Bold)
        section_style = "color: #1565C0;"

        db_connection_label = QLabel('Database Connection 🛠️')
        db_connection_label.setFont(section_font)
        db_connection_label.setStyleSheet(section_style)

        # Create a status label
        self.status_label = QLabel('Status: Ready')
        self.status_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.status_label.setStyleSheet("color: #1565C0;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Set up the layout for the first page
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(app_title_label)
        main_layout.addSpacing(20)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        form_layout.addWidget(db_connection_label)
        form_layout.addWidget(self.dialect_edit)
        form_layout.addWidget(self.driver_edit)
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.host_edit)
        form_layout.addWidget(self.port_edit)
        form_layout.addWidget(self.database_edit)
        form_layout.addWidget(self.table_edit)
        form_layout.addWidget(self.connect_button)
        form_layout.addWidget(self.status_label)

        center_layout = QHBoxLayout()
        center_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        center_layout.addLayout(form_layout)
        center_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(center_layout)

        self.page1.setLayout(main_layout)

    def create_page2(self):
        """
        Create the second page for other database interactions.
        """
        # Create buttons for various database operations
        self.import_button = self.create_styled_button('Import Excel File', self.import_excel, 'fa5s.file-excel')
        self.lowercase_button = self.create_styled_button('Lowercase Headers', self.lowercase_headers, 'fa5s.text-height')
        self.replace_spaces_button = self.create_styled_button('Replace Spaces in Headers', self.replace_spaces_in_headers, 'fa5s.text-width')
        self.drop_na_button = self.create_styled_button('Drop NA', self.drop_na_values, 'fa5s.times-circle')
        self.remove_duplicates_button = self.create_styled_button('Remove Duplicates', self.remove_duplicates, 'fa5s.clone')
        self.disconnect_button = self.create_styled_button('Disconnect from Database', self.disconnect_from_database, 'fa5s.sign-out-alt')

        # Create section labels
        section_font = QFont('Verdana', 16, QFont.Bold)
        section_style = "color: #1565C0;"

        import_data_label = QLabel('Import Data 📥')
        import_data_label.setFont(section_font)
        import_data_label.setStyleSheet(section_style)

        data_preparation_label = QLabel('Data Preparation 📝')
        data_preparation_label.setFont(section_font)
        data_preparation_label.setStyleSheet(section_style)

        data_cleaning_label = QLabel('Data Cleaning 🧹')
        data_cleaning_label.setFont(section_font)
        data_cleaning_label.setStyleSheet(section_style)

        # Create a status label
        self.status_label = QLabel('Status: Ready')
        self.status_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.status_label.setStyleSheet("color: #1565C0;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Set up the layout for the second page
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        form_layout.addWidget(import_data_label)
        form_layout.addWidget(self.import_button)

        form_layout.addSpacing(10)

        form_layout.addWidget(data_preparation_label)
        form_layout.addWidget(self.lowercase_button)
        form_layout.addWidget(self.replace_spaces_button)

        form_layout.addSpacing(10)

        form_layout.addWidget(data_cleaning_label)
        form_layout.addWidget(self.drop_na_button)
        form_layout.addWidget(self.remove_duplicates_button)

        form_layout.addWidget(self.disconnect_button)
        form_layout.addWidget(self.status_label)

        center_layout = QHBoxLayout()
        center_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        center_layout.addLayout(form_layout)
        center_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(center_layout)

        self.page2.setLayout(main_layout)

    def create_input_field(self, placeholder_text, password=False):
        """
        Create a QLineEdit with shadow effect and border.
        """
        input_field = QLineEdit()  # Create a QLineEdit widget
        input_field.setPlaceholderText(placeholder_text)  # Set the placeholder text
        input_field.setFont(QFont('Arial', 14))  # Set the font of the text

        if password:
            input_field.setEchoMode(QLineEdit.Password)  # If password is True, set the echo mode to Password

        # Set the style sheet for the input field
        input_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #1E88E5;
                border-radius: 10px;
                padding: 10px;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #1E88E5;
            }
        """)

        # Create and set a drop shadow effect for the input field
        shadow = self.create_shadow_effect()
        input_field.setGraphicsEffect(shadow)

        return input_field  # Return the created input field

    def connect_to_database(self):
        """
        Connect to the database using the provided connection parameters.
        """
        # Construct the connection URL from input fields
        connection_url = (
            f"{self.dialect_edit.text()}+{self.driver_edit.text()}://"
            f"{self.username_edit.text()}:{self.password_edit.text()}@"
            f"{self.host_edit.text()}:{self.port_edit.text()}/"
            f"{self.database_edit.text()}"
        )

        try:
            # Create the SQLAlchemy engine and connect to the database
            engine = sal.create_engine(connection_url)
            self.conn = engine.connect()
            self.status_label.setText('Status: Connected to Database')

            # Handle table connection
            self.table_name = self.table_edit.text().strip()
            if self.table_name:
                try:
                    pd.read_sql_table(self.table_name, self.conn)
                    self.status_label.setText(f'Status: Connected to Table "{self.table_name}"')
                    self.show_message_box('Connection Successful', f'Connected to the table "{self.table_name}" successfully.', QMessageBox.Information)
                except Exception as e:
                    self.table_name = None
                    self.show_message_box('Table Connection Error', f'Table "{self.table_name}" does not exist. Error: {e}', QMessageBox.Critical)
            else:
                self.show_message_box('Connection Successful', 'Connected to the database successfully. You can create a new table by importing an Excel file.', QMessageBox.Information)

            self.stacked_widget.setCurrentIndex(1)  # Switch to the second page
        except Exception as e:
            self.conn = None
            self.status_label.setText('Status: Connection Failed')
            logging.error(f'Error connecting to database: {e}')
            self.show_message_box('Connection Error', f'Error connecting to database: {e}', QMessageBox.Critical)

    def disconnect_from_database(self):
        """
        Disconnect from the database.
        """
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                self.table_name = None
                self.status_label.setText('Status: Disconnected from Database')
                self.show_message_box('Disconnection Successful', 'Disconnected from the database successfully.', QMessageBox.Information)
                # Switch back to the first page after disconnection
                self.stacked_widget.setCurrentIndex(0)
            except Exception as e:
                logging.error(f'Error disconnecting from database: {e}')
                self.show_message_box('Disconnection Error', f'Error disconnecting from database: {e}', QMessageBox.Critical)
        else:
            self.show_message_box('Disconnection Error', 'No database connection to disconnect.', QMessageBox.Warning)

    def import_excel(self):
        """
        Import data from an Excel file into the database.
        """
        if not self.conn:
            self.show_message_box('Import Error', 'No database connection established.', QMessageBox.Warning)
            return

        try:
            # Open a file dialog to select the Excel file
            file_path, _ = QFileDialog.getOpenFileName(self, 'Open Excel File', os.getenv('HOME'), 'Excel Files (*.xlsx *.xls)')
            if not file_path:
                return

            df = pd.read_excel(file_path)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            self.table_name = file_name

            # Import the Excel data into the database table
            df.to_sql(self.table_name, con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Import Successful', f'Excel file imported successfully as table "{self.table_name}".', QMessageBox.Information)
        except Exception as e:
            logging.error(f'Error importing Excel file: {e}')
            self.show_message_box('Import Error', f'Error importing Excel file: {e}', QMessageBox.Critical)

    def lowercase_headers(self):
        """
        Lowercase the headers of a selected table in the database.
        """
        try:
            if not self.table_name:
                self.show_message_box('Error', 'No table name provided.', QMessageBox.Warning)
                return

            df = pd.read_sql_table(self.table_name, self.conn)
            df.columns = [col.lower() for col in df.columns]
            df.to_sql(self.table_name, con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Lowercase Headers', 'Table headers lowercased successfully.', QMessageBox.Information)
        except Exception as e:
            logging.error(f'Error lowercasing headers: {e}')
            self.show_message_box('Lowercase Headers Error', f'Error lowercasing headers: {e}', QMessageBox.Critical)

    def replace_spaces_in_headers(self):
        """
        Replace spaces in the headers of a selected table in the database with underscores.
        """
        try:
            if not self.table_name:
                self.show_message_box('Error', 'No table name provided.', QMessageBox.Warning)
                return

            df = pd.read_sql_table(self.table_name, self.conn)
            df.columns = [col.replace(' ', '_') for col in df.columns]
            df.to_sql(self.table_name, con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Replace Spaces in Headers', 'Spaces in headers replaced successfully.', QMessageBox.Information)
        except Exception as e:
            logging.error(f'Error replacing spaces in headers: {e}')
            self.show_message_box('Replace Spaces in Headers Error', f'Error replacing spaces in headers: {e}', QMessageBox.Critical)

    def drop_na_values(self):
        """
        Drop rows with NA values from a selected table in the database.
        """
        try:
            if not self.table_name:
                self.show_message_box('Error', 'No table name provided.', QMessageBox.Warning)
                return

            df = pd.read_sql_table(self.table_name, self.conn)
            df = df.dropna()
            df.to_sql(self.table_name, con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Drop NA Values', 'NA values dropped successfully.', QMessageBox.Information)
        except Exception as e:
            logging.error(f'Error dropping NA values: {e}')
            self.show_message_box('Drop NA Values Error', f'Error dropping NA values: {e}', QMessageBox.Critical)

    def remove_duplicates(self):
        """
        Remove duplicate rows from a selected table in the database.
        """
        try:
            if not self.table_name:
                self.show_message_box('Error', 'No table name provided.', QMessageBox.Warning)
                return

            df = pd.read_sql_table(self.table_name, self.conn)
            df = df.drop_duplicates()
            df.to_sql(self.table_name, con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Remove Duplicates', 'Duplicate rows removed successfully.', QMessageBox.Information)
        except Exception as e:
            logging.error(f'Error removing duplicates: {e}')
            self.show_message_box('Remove Duplicates Error', f'Error removing duplicates: {e}', QMessageBox.Critical)

    def show_message_box(self, title, message, icon):
        """
        Show a message box with the given title, message, and icon.
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()  # Explicitly show the window
    window.raise_()  # Brings the window to the front
    window.activateWindow()  # Activates the window
    sys.exit(app.exec_())
