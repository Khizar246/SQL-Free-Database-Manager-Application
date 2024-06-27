import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QSpacerItem, QSizePolicy, QMessageBox, QFileDialog
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
import sqlalchemy as sal
import pandas as pd

class DatabaseApp(QWidget):
    def __init__(self):
        """
        Constructor method that initializes the DatabaseApp class.
        """
        super().__init__()  # Initialize the parent class
        self.initUI()  # Initialize the UI components
        self.conn = None  # Initialize connection variable to None

    def initUI(self):
        """
        Method to initialize the user interface.
        """
        # Set the title and size of the main window
        self.setWindowTitle('Database Interaction App 📊')
        self.setGeometry(100, 100, 600, 700)

        # Set the overall background color
        self.setStyleSheet("background-color: #e0f7fa;")

        # Create QLineEdit widgets for database connection setup with placeholders
        self.dialect_edit = self.create_input_field('Enter SQL Dialect (e.g., mysql)')
        self.driver_edit = self.create_input_field('Enter SQL Driver (e.g., pymysql)')
        self.username_edit = self.create_input_field('Enter Username')
        self.password_edit = self.create_input_field('Enter Password', password=True)
        self.host_edit = self.create_input_field('Enter Host Address (e.g., localhost)')
        self.port_edit = self.create_input_field('Enter Port Number (e.g., 3306)')
        self.database_edit = self.create_input_field('Enter Database Name')

        # Style the buttons and add shadow effect
        button_style = """
            QPushButton {
                background-color: #4CAF50;
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
                border: 2px solid #4CAF50;
            }
        """

        # Create and style QPushButton widgets
        self.connect_button = QPushButton('Connect to Database')  # Button to connect to the database
        self.connect_button.clicked.connect(self.connect_to_database)  # Connect button to its handler method
        self.connect_button.setStyleSheet(button_style)
        self.add_shadow_effect(self.connect_button)

        self.disconnect_button = QPushButton('Disconnect from Database')  # Button to disconnect from the database
        self.disconnect_button.clicked.connect(self.disconnect_from_database)  # Connect button to its handler method
        self.disconnect_button.setStyleSheet(button_style)
        self.add_shadow_effect(self.disconnect_button)

        self.import_button = QPushButton('Import Excel File')  # Button to import an Excel file
        self.import_button.clicked.connect(self.import_excel)  # Connect button to its handler method
        self.import_button.setStyleSheet(button_style)
        self.add_shadow_effect(self.import_button)

        self.lowercase_button = QPushButton('Lowercase Headers')  # Button to lowercase headers
        self.lowercase_button.clicked.connect(self.lowercase_headers)  # Connect button to its handler method
        self.lowercase_button.setStyleSheet(button_style)
        self.add_shadow_effect(self.lowercase_button)

        self.replace_spaces_button = QPushButton('Replace Spaces in Headers')  # Button to replace spaces in headers
        self.replace_spaces_button.clicked.connect(self.replace_spaces_in_headers)  # Connect button to its handler method
        self.replace_spaces_button.setStyleSheet(button_style)
        self.add_shadow_effect(self.replace_spaces_button)

        self.drop_na_button = QPushButton('Drop NA')  # Button to drop NA values
        self.drop_na_button.clicked.connect(self.drop_na_values)  # Connect button to its handler method
        self.drop_na_button.setStyleSheet(button_style)
        self.add_shadow_effect(self.drop_na_button)

        # Create and style QLabel widgets
        app_title_label = QLabel('Database Interaction App 📊')  # Application title
        app_title_label.setFont(QFont('Arial', 24, QFont.Bold))
        app_title_label.setStyleSheet("color: #00695c;")
        app_title_label.setAlignment(Qt.AlignCenter)

        section_font = QFont('Verdana', 16, QFont.Bold)
        section_style = "color: #004d40;"

        db_connection_label = QLabel('Database Connection 🛠️')  # Label for database connection section
        db_connection_label.setFont(section_font)
        db_connection_label.setStyleSheet(section_style)

        import_data_label = QLabel('Import Data 📥')  # Label for import data section
        import_data_label.setFont(section_font)
        import_data_label.setStyleSheet(section_style)

        data_preparation_label = QLabel('Data Preparation 📝')  # Label for data preparation section
        data_preparation_label.setFont(section_font)
        data_preparation_label.setStyleSheet(section_style)

        data_cleaning_label = QLabel('Data Cleaning 🧹')  # Label for data cleaning section
        data_cleaning_label.setFont(section_font)
        data_cleaning_label.setStyleSheet(section_style)

        # Create and style the status label
        self.status_label = QLabel('Status: Ready')  # Label to display the current status
        self.status_label.setFont(QFont('Arial', 16, QFont.Bold))
        self.status_label.setStyleSheet("color: #004d40;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Layout setup
        main_layout = QVBoxLayout()  # Main vertical layout
        main_layout.setAlignment(Qt.AlignTop)

        # Add the application title label to the main layout
        main_layout.addWidget(app_title_label)

        # Add spacing between the application title and the main content
        main_layout.addSpacing(20)

        form_layout = QVBoxLayout()  # Form vertical layout
        form_layout.setSpacing(10)

        # Add widgets to the form layout
        form_layout.addWidget(db_connection_label)
        form_layout.addWidget(self.dialect_edit)
        form_layout.addWidget(self.driver_edit)
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.host_edit)
        form_layout.addWidget(self.port_edit)
        form_layout.addWidget(self.database_edit)
        form_layout.addWidget(self.connect_button)
        form_layout.addWidget(self.disconnect_button)

        # Add spacing between sections
        form_layout.addSpacing(10)

        form_layout.addWidget(import_data_label)
        form_layout.addWidget(self.import_button)

        # Add spacing between sections
        form_layout.addSpacing(10)

        form_layout.addWidget(data_preparation_label)
        form_layout.addWidget(self.lowercase_button)
        form_layout.addWidget(self.replace_spaces_button)

        # Add spacing between sections
        form_layout.addSpacing(10)

        form_layout.addWidget(data_cleaning_label)
        form_layout.addWidget(self.drop_na_button)
        form_layout.addWidget(self.status_label)

        # Center the form layout
        center_layout = QHBoxLayout()  # Horizontal layout to center the form
        center_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        center_layout.addLayout(form_layout)
        center_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(center_layout)  # Add the centered layout to the main layout

        self.setLayout(main_layout)  # Set the main layout
        self.show()  # Show the main window

    def create_input_field(self, placeholder_text, password=False):
        """
        Create a QLineEdit with shadow effect and border.
        """
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setFont(QFont('Arial', 14))
        if (password):
            input_field.setEchoMode(QLineEdit.Password)

        # Style the input field
        input_field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #4CAF50;
                border-radius: 10px;
                padding: 10px;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)

        # Add shadow effect to the input field
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(2, 2)
        input_field.setGraphicsEffect(shadow)

        return input_field

    def add_shadow_effect(self, button):
        """
        Add a shadow effect to a given button.
        """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(3, 3)
        button.setGraphicsEffect(shadow)

    def connect_to_database(self):
        """
        Connect to the database using the provided connection parameters.
        """
        connection_url = (
            f"{self.dialect_edit.text()}+{self.driver_edit.text()}://"
            f"{self.username_edit.text()}:{self.password_edit.text()}@"
            f"{self.host_edit.text()}:{self.port_edit.text()}/"
            f"{self.database_edit.text()}"
        )

        try:
            engine = sal.create_engine(connection_url)
            self.conn = engine.connect()
            self.status_label.setText('Status: Connected to Database')
            self.show_message_box('Connection Successful', 'Connected to the database successfully.', QMessageBox.Information)
        except Exception as e:
            self.conn = None
            self.status_label.setText('Status: Connection Failed')
            self.show_message_box('Connection Error', f'Error connecting to database: {e}', QMessageBox.Critical)

    def disconnect_from_database(self):
        """
        Disconnect from the currently connected database.
        """
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                self.status_label.setText('Status: Disconnected from Database')
                self.show_message_box('Disconnection Successful', 'Disconnected from the database successfully.', QMessageBox.Information)
            except Exception as e:
                self.show_message_box('Disconnection Error', f'Error disconnecting from database: {e}', QMessageBox.Critical)
        else:
            self.show_message_box('Disconnection Error', 'No active database connection to disconnect.', QMessageBox.Warning)

    def import_excel(self):
        """
        Import data from an Excel file into the database.
        """
        if not self.conn:
            self.show_message_box('Connection Error', 'Database connection not established.', QMessageBox.Warning)
            return

        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Excel File', '', 'Excel Files (*.xls *.xlsx)')
        if file_path:
            try:
                df = pd.read_excel(file_path)
                df.to_sql(name='orders', con=self.conn, if_exists='replace', index=False)
                self.show_message_box('Import Successful', f'Successfully imported data from {file_path} into table orders.', QMessageBox.Information)
            except Exception as e:
                self.show_message_box('Import Error', f'Error importing Excel file: {e}', QMessageBox.Critical)

    def lowercase_headers(self):
        """
        Convert column headers of the 'orders' table to lowercase.
        """
        if not self.conn:
            self.show_message_box('Connection Error', 'Database connection not established.', QMessageBox.Warning)
            return

        try:
            df = pd.read_sql_table('orders', self.conn)
            df.columns = df.columns.str.lower()
            df.to_sql(name='orders', con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Lowercase Headers', 'Successfully converted column headers to lowercase.', QMessageBox.Information)
        except Exception as e:
            self.show_message_box('Lowercase Headers Error', f'Error converting column headers to lowercase: {e}', QMessageBox.Critical)

    def replace_spaces_in_headers(self):
        """
        Replace spaces in column headers of the 'orders' table with underscores.
        """
        if not self.conn:
            self.show_message_box('Connection Error', 'Database connection not established.', QMessageBox.Warning)
            return

        try:
            df = pd.read_sql_table('orders', self.conn)
            df.columns = df.columns.str.replace(' ', '_')
            df.to_sql(name='orders', con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Replace Spaces in Headers', 'Successfully replaced spaces with underscores in column headers.', QMessageBox.Information)
        except Exception as e:
            self.show_message_box('Replace Spaces in Headers Error', f'Error replacing spaces in column headers: {e}', QMessageBox.Critical)

    def drop_na_values(self):
        """
        Drop rows with 'NA' values from the 'orders' table.
        """
        if not self.conn:
            self.show_message_box('Connection Error', 'Database connection not established.', QMessageBox.Warning)
            return

        try:
            df = pd.read_sql_table('orders', self.conn)
            cleaned_df = df.replace('NA', pd.NA).dropna()
            cleaned_df.to_sql(name='orders', con=self.conn, if_exists='replace', index=False)
            self.show_message_box('Drop NA', 'Successfully dropped rows with "NA" values.', QMessageBox.Information)
        except Exception as e:
            self.show_message_box('Drop NA Error', f'Error dropping rows with "NA" values: {e}', QMessageBox.Critical)

    def show_message_box(self, title, message, icon):
        """
        Show a message box with the specified title, message, and icon.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
        
if __name__ == "__main__":
    app = QApplication([])
    ex = DatabaseApp()
    app.exec_()