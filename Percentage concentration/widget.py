from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGridLayout, QMessageBox, QFormLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QPoint
import usefull_functions as uf
import algorithms as alg
import os

class Settings_window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("images/title_icon.png"))
        self.setFixedSize(725, 350)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Flags:
        self.pallete_changed = False
        self.preview_active = False
        self.setting_window_layout_option = 0

        self.default_layout()
        self.setLayout(self.whole_window)
        self.load_colors()
        self.fill_color_lines()
    
    # When program start creat all fully setted layout: 
    def default_layout(self):

        # Title bar settings:
        self.title_bar =  QHBoxLayout()
        self.title_bar.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setSpacing(0)
        self.minimize_button = QPushButton("_")
        self.minimize_button.setFixedWidth(50)
        self.exit_button = QPushButton("X")
        self.exit_button.setFixedWidth(50)
        self.title = QLabel("Settings", objectName="title_bar_title")
        self.title_bar.addWidget(self.title)
        self.title_bar.addWidget(self.minimize_button)
        self.title_bar.addWidget(self.exit_button)

        # Layouts:
        self.gather_data = QVBoxLayout()
        self.lines = QFormLayout()
        self.button_lines = QHBoxLayout()
        self.whole_window = QGridLayout()

        # Buttons:
        self.load_default_pallete_button = QPushButton("Load default pallete", objectName="color_option")
        self.preview_button = QPushButton("Preview", objectName="color_option")
        self.load_previous_pallete_button = QPushButton("Back changes", objectName="color_option")
        self.save_pallete_button = QPushButton("Save pallete", objectName="color_option")

        # Signals:
        self.load_default_pallete_button.clicked.connect(self.load_default_pallete)
        self.preview_button.clicked.connect(self.preview_pallete)
        self.save_pallete_button.clicked.connect(self.save_pallet)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.exit_button.clicked.connect(self.quit_application)

        # QLabels:
        self.title = QLabel("Change pallete:", objectName="title")
        self.first_label = QLabel("Background color of window:")
        self.second_label = QLabel("Font color for window:")
        self.third_label = QLabel("Background color for buttons:")
        self.fourth_label = QLabel("Font color for buttons:")
        self.fifth_label = QLabel("Background color for line edit fields:")
        self.sixth_label = QLabel("Font color for line edit fields:")

        # QLineEdit:
        self.first_data = QLineEdit()
        self.second_data = QLineEdit()
        self.third_data = QLineEdit()
        self.fourth_data = QLineEdit()
        self.fifth_data = QLineEdit()
        self.sixth_data = QLineEdit()

        # Set Layouts:
        self.gather_data.addWidget(self.title)

        self.lines.addRow(self.first_label, self.first_data)
        self.lines.addRow(self.second_label, self.second_data)
        self.lines.addRow(self.third_label, self.third_data)
        self.lines.addRow(self.fourth_label, self.fourth_data)
        self.lines.addRow(self.fifth_label, self.fifth_data)
        self.lines.addRow(self.sixth_label, self.sixth_data)
        self.button_lines.addWidget(self.load_default_pallete_button)
        self.button_lines.addWidget(self.preview_button)
        self.button_lines.addWidget(self.load_previous_pallete_button)
        self.button_lines.addWidget(self.save_pallete_button)

        self.gather_data.addLayout(self.lines)
        self.gather_data.addLayout(self.button_lines)
        self.gather_data.setContentsMargins(5, 5, 5, 5)
        self.whole_window.addLayout(self.title_bar, 0, 0)
        self.whole_window.addLayout(self.gather_data, 1, 0)
        self.whole_window.setContentsMargins(0, 0, 0, 0)

    # Load pallete from setted file.
    def load_colors(self):

        path = "files\selected pallete.txt"
        exist = os.path.exists(path)

        # Protection:
        if exist is True:
            with open(path, "r") as file:
                path = file.readline()
                exist = os.path.exists(path)
        else:
            wrong_data = QMessageBox().critical(self, "Warning", "Source file doesn't exist. Program load default pallet.", QMessageBox.Ok)
            path = "files\default color settings.txt"
        
            with open("files\selected pallete.txt", "w") as file:
                file.write(path)
        
        # Window: background-color; font-color; Button: background-color; font-color; LineEdit: background-color; font-color;
        self.colors = []

        if exist is True:
            with open(path, "r") as file:
                for number, line in enumerate(file):
                    if number != 5:
                        self.colors.append(line[:-1])
                    else:
                        self.colors.append(line)

        else:
            wrong_data = QMessageBox().critical(self, "Warning", "Source file doesn't exist. Reinstalation is needed.", QMessageBox.Ok)
            exit(1)
 
        styles = """
            QWidget {
            background-color: """ + self.colors[0] + """;
            color: """ + self.colors[1] + """;
            }

            QPushButton#color_option {
            color: black;
            font-size: 18px;
            font-style: bold;
            width: 400px;
            height: 40px;
            background-color: """ + self.colors[2] + """;
            color: """ + self.colors[3] + """;
            }

            QPushButton {
            background-color: #005bc5;
            color: black;
            font-size: 18px;
            font-style: bold;
            height: 40px;
            background-color: """ + self.colors[2] + """;
            color: """ + self.colors[3] + """;
            }

            QLabel {
            font-size: 18px;
            font-family: Consolas;
            margin: 2px;
            }

            QLabel#title {
            font-weight: bold;
            padding-bottom: 10px;
            }

            QLabel#title_bar_title {
            font-weight: bold;
            font-size: 20px;
            }

            QLineEdit {
            background-color: """ + self.colors[4] + """;
            color: """ + self.colors[5] + """;
            font-size: 18px;
            }

            QRadioButton {
            font-size: 18px;
            }
            """
        
        self.setStyleSheet(styles)

    # Fill QEditLines objects with RGB colors in hexadecimal number format.
    def fill_color_lines(self):
        self.first_data.setText(self.colors[0])
        self.second_data.setText(self.colors[1])
        self.third_data.setText(self.colors[2])
        self.fourth_data.setText(self.colors[3])
        self.fifth_data.setText(self.colors[4])
        self.sixth_data.setText(self.colors[5])

    # Slots:
    # Save pallete
    def save_pallet(self):
        self.colors.clear()
        self.colors.append(uf.is_a_hexadecimal_color(self.first_data.text()))
        self.colors.append(uf.is_a_hexadecimal_color(self.second_data.text()))
        self.colors.append(uf.is_a_hexadecimal_color(self.third_data.text()))
        self.colors.append(uf.is_a_hexadecimal_color(self.fourth_data.text()))
        self.colors.append(uf.is_a_hexadecimal_color(self.fifth_data.text()))
        self.colors.append(uf.is_a_hexadecimal_color(self.sixth_data.text()))

        # Protection
        if False in self.colors:
            wrong_data = QMessageBox.warning(self, "Warning", "Wrong data was given as color", QMessageBox.Ok)
            self.colors.clear()
            return 1

        with open("files\custom pallete.txt", "w") as file:
            for number, color in enumerate(self.colors):
                if number < 5:
                    file.write(color + "\n")
                else:
                    file.write(color)
        
        with open("files\selected pallete.txt", "w") as file:
            file.write("files\custom pallete.txt")
            
        self.load_colors()
        self.fill_color_lines()
    
    def clear_pallete_changed_flag(self):
        self.pallete_changed = False
    
    # Load defoult pallete from file.
    def load_default_pallete(self):
        with open("files\selected pallete.txt", "w") as file:
            file.write("files\default color settings.txt")
        self.pallete_changed = True
        self.load_colors()
        self.fill_color_lines()
    
    # Showing at main window appereance of preview pattern.
    def preview_pallete(self):
        self.preview_active = False
        self.preview_colors = []
        self.preview_colors.append(uf.is_a_hexadecimal_color(self.first_data.text()))
        self.preview_colors.append(uf.is_a_hexadecimal_color(self.second_data.text()))
        self.preview_colors.append(uf.is_a_hexadecimal_color(self.third_data.text()))
        self.preview_colors.append(uf.is_a_hexadecimal_color(self.fourth_data.text()))
        self.preview_colors.append(uf.is_a_hexadecimal_color(self.fifth_data.text()))
        self.preview_colors.append(uf.is_a_hexadecimal_color(self.sixth_data.text()))
        self.pallete_changed = True

        # Protection:
        if False in self.preview_colors:
            wrong_data = QMessageBox.warning(self, "Warning", "Wrong data was given as color!", QMessageBox.Ok)
            self.preview_colors.clear()
            return 1
        
        self.preview_active = True
    def return_pallete_from_preview(self):
        return self.preview_colors

    def minimize_window(self):
        self.showMinimized()

    # Quit application.
    def quit_application(self):
        sure = QMessageBox(self, objectName="quit_window")
        sure.setIcon(QMessageBox.Warning)
        sure.setWindowTitle("Quit")
        sure.setText("Are you sure, you want to close setting window?")
        sure.setFixedWidth(100)
        
        sure.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        answer = sure.exec()
        
        if answer == QMessageBox.Yes:
            self.close()

    # Get position of mouse at pressing.
    def mousePressEvent(self, event):
        self.old_position = event.globalPos()
    
    # Move window with pressed mouse
    def mouseMoveEvent(self, event):
        self.delta = QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + self.delta.x(), self.y() + self.delta.y())
        self.old_position = event.globalPos()

class Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Flags:
        self.option_number = 0
        self.active_layout_number = 0
        self.settings_window_exist = False

        self.setWindowIcon(QIcon("images/title_icon.png"))
        self.setFixedSize(1100, 325)
        self.load_colors()
        self.set_default_layout()
        self.setLayout(self.whole_window)

    # Slots:
    def get_pc(self):

        if self.active_layout_number == 1:
            self.set_first_layout()
            self.active_layout_number = 0

        if self.option_number != 0:
            self.option_number = 0
            self.first_data.setText("")
            self.second_data.setText("")
            self.result.setText("")
            # Change label's text.
            self.what_calculate.setText("Percentage concentration")
            self.first_label.setText("Mass of solut:")
            self.first_unit.setText("g")
            self.second_label.setText("Mass of solution:")
            self.second_unit.setText("g")
            self.result_label.setText("Percentage concentration:")
            self.result_unit.setText("%")

    def get_mass_of_solut(self):

        if self.active_layout_number == 1:
            self.set_first_layout()
            self.active_layout_number = 0

        if self.option_number != 1:
            self.option_number = 1
            self.first_data.setText("")
            self.second_data.setText("")
            self.result.setText("")
            # Change label's text.
            self.what_calculate.setText("Mass of solut")
            self.first_label.setText("Percentage concentration:")
            self.first_unit.setText("%")
            self.second_label.setText("Mass of solution:")
            self.second_unit.setText("g")
            self.result_label.setText("Mass of solut:")
            self.result_unit.setText("g")

    def get_mass_of_solution(self):

        if self.active_layout_number == 1:
            self.set_first_layout()
            self.active_layout_number = 0

        if self.option_number != 2:
            self.option_number = 2
            self.first_data.setText("")
            self.second_data.setText("")
            self.result.setText("")
            # Change label's text.
            self.what_calculate.setText("Mass of solution")
            self.first_label.setText("Mass of solut:")
            self.first_unit.setText("g")
            self.second_label.setText("Percentage concentration:")
            self.second_unit.setText("%")
            self.result_label.setText("Mass of solution result:")
            self.result_unit.setText("g")
    
    # Protections, getting result and show them in application.  
    def calculate_result(self):
        
        # For calculate percentage concentration:
        if self.option_number == 0:
            mass_of_solut = uf.isNumber(self.first_data.text())
            if mass_of_solut is False:  
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as mass of solut.", QMessageBox.Ok)
                return 1
            
            mass_of_solution = uf.isNumber(self.second_data.text())
            if mass_of_solution is False:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as mass of solution.", QMessageBox.Ok)
                return 1
            
            if mass_of_solut < 0:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass positive number as mass of solution.", QMessageBox.Ok)
                return 1

            if mass_of_solution <= 0:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number greather than 0 as mass of solution.", QMessageBox.Ok)
                return 1
            
            if mass_of_solution < mass_of_solut:
                wrong_data = QMessageBox().warning(self, "Warning", "Mass of solution can't be lesser than mass of solut.", QMessageBox.Ok)
                return 1

            self.result.setText(str(alg.calculate_percentage_concentration(mass_of_solut, mass_of_solution)))

        # For calculate mass of solut:
        if self.option_number == 1:
            percentage_concentration = uf.isNumber(self.first_data.text())
            if percentage_concentration is False:  
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as mass of solut.", QMessageBox.Ok)
                return 1
            
            mass_of_solution = uf.isNumber(self.second_data.text())
            if mass_of_solution is False:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as mass of solution.", QMessageBox.Ok)
                return 1
            
            if percentage_concentration < 0 or percentage_concentration > 100:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number in range from 0 to 100, as percentage concentration.", QMessageBox.Ok)
                return 1

            if mass_of_solution <= 0:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number greather than 0 as mass of solution.", QMessageBox.Ok)
                return 1

            self.result.setText(str(alg.calculate_mass_of_solut(percentage_concentration, mass_of_solution)))

        # For calculate mass of solution:
        if self.option_number == 2:        
            mass_of_solut = uf.isNumber(self.first_data.text())
            if mass_of_solut is False:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as mass of solut.", QMessageBox.Ok)
                return 1
            
            percentage_concentration = uf.isNumber(self.second_data.text())
            if percentage_concentration is False:  
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number in range from 0 to 100, as percentage concentration.", QMessageBox.Ok)
                return 1
            
            if percentage_concentration < 0 or percentage_concentration > 100:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass number in range from 0 to 100, as percentage concentration.", QMessageBox.Ok)
                return 1

            if mass_of_solut < 0:
                wrong_data = QMessageBox().warning(self, "Warning", "You should pass positive number as mass of solution.", QMessageBox.Ok)
                return 1

            self.result.setText(str(alg.calculate_mass_of_solution(mass_of_solut, percentage_concentration)))
        
        if self.option_number == 3:
            self.cross_rule()

    def copy_result(self):

        self.result.selectAll()
        self.result.copy()
    
    def minimize_window(self):
        self.showMinimized()

    def quit_application(self):
        sure = QMessageBox(self, objectName="quit_window")
        sure.setIcon(QMessageBox.Warning)
        sure.setWindowTitle("Quit")
        sure.setText("Are you sure, you want to quit?")
        sure.setFixedWidth(100)
        
        sure.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        answer = sure.exec()
        
        # Protection:
        if answer == QMessageBox.Yes:
            if self.settings_window_exist is True:
                self.settings_window.close()
            self.close()

    # Load default layout at start application.
    def set_default_layout(self):
        
        # Title bar settings:
        self.title_bar =  QHBoxLayout()
        self.title_bar.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setSpacing(0)
        self.minimize_button = QPushButton("_")
        self.minimize_button.setFixedWidth(50)
        self.exit_button = QPushButton("X")
        self.exit_button.setFixedWidth(50)
        self.title = QLabel("Percentage concentration calculator", objectName="title_bar_title")
        self.title_bar.addWidget(self.title)
        self.title_bar.addWidget(self.minimize_button)
        self.title_bar.addWidget(self.exit_button)

        self.active_layout_number = 0

        # Labels:
        self.what_calculate = QLabel("Percentage concentration:", objectName="title")
        self.first_label = QLabel("Mass of solut:")
        self.first_unit = QLabel("g")
        self.second_label = QLabel("Mass of solution:")
        self.second_unit = QLabel("g")
        self.result_label = QLabel("Percentage concentration:")
        self.result_unit = QLabel("%")

        # LineEdits:
        self.first_data = QLineEdit()
        self.second_data = QLineEdit()
        self.result = QLineEdit()

        # Buttons:
        self.pc_button = QPushButton("Calculate percentage concentration", objectName="side_menu")
        self.mass_of_solut_button = QPushButton("Calculate mass of solut", objectName="side_menu")
        self.mass_of_solution_button = QPushButton("Calculate mass of solution", objectName="side_menu")
        self.cross_rule_button = QPushButton("Cross rule", objectName="side_menu")
        self.settigs_button = QPushButton("Settings", objectName="side_menu")
        self.quit_button = QPushButton("Quit", objectName="side_menu")
        self.calculate_button = QPushButton("Calculate", objectName="side_menu")
        self.copy_result_button = QPushButton("Copy", objectName="copy_button")
        
        # Signals:
        self.pc_button.clicked.connect(self.get_pc)
        self.mass_of_solut_button.clicked.connect(self.get_mass_of_solut)
        self.mass_of_solution_button.clicked.connect(self.get_mass_of_solution)
        self.cross_rule_button.clicked.connect(self.set_second_layout)
        self.settigs_button.clicked.connect(self.show_settings_window)
        self.quit_button.clicked.connect(self.quit_application)
        self.calculate_button.clicked.connect(self.calculate_result)
        self.calculate_button.pressed.connect(self.calculate_result)
        self.copy_result_button.clicked.connect(self.copy_result)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.exit_button.clicked.connect(self.quit_application)
        
        # Layouts:
        self.whole_window = QGridLayout()
        self.side_menu = QVBoxLayout()
        self.gather_data = QVBoxLayout()
        self.lines = QFormLayout()
        self.first_line = QHBoxLayout()
        self.second_line = QHBoxLayout()
        self.result_line = QHBoxLayout()
        self.full_result_line = QFormLayout()

        # Fill layouts:
        self.side_menu.addWidget(self.pc_button)
        self.side_menu.addWidget(self.mass_of_solut_button)
        self.side_menu.addWidget(self.mass_of_solution_button)
        self.side_menu.addWidget(self.cross_rule_button)
        self.side_menu.addWidget(self.settigs_button)
        self.side_menu.addWidget(self.quit_button)

        self.lines.addRow(self.what_calculate)

        self.first_line.addWidget(self.first_data)
        self.first_line.addWidget(self.first_unit)
        self.lines.addRow(self.first_label, self.first_line)
        
        self.second_line.addWidget(self.second_data)
        self.second_line.addWidget(self.second_unit)
        self.lines.addRow(self.second_label, self.second_line)

        self.lines.setVerticalSpacing(20)

        self.result_line.addWidget(self.result)
        self.result_line.addWidget(self.result_unit)
        self.result_line.addWidget(self.copy_result_button)
        self.result_line.setContentsMargins(0, 0, 0, 10)
        self.full_result_line.addRow(self.result_label, self.result_line)

        self.gather_data.addLayout(self.lines)
        self.gather_data.addWidget(self.calculate_button)

        self.gather_data.addLayout(self.full_result_line)
        self.gather_data.setSpacing(20)

        self.whole_window.setContentsMargins(0, 0, 0, 0)

        self.whole_window.addLayout(self.title_bar, 0, 0, 1, 2)

        self.whole_window.addLayout(self.side_menu, 1, 0)
        self.whole_window.setRowMinimumHeight(1,15)
        self.whole_window.addLayout(self.gather_data, 1, 1)
    
    # If layout is setted at "cross rule" option, change layout for other options.
    def set_first_layout(self):
        if self.active_layout_number == 1:
            
            button = self.gather_data.takeAt(2)
            self.lines.removeRow(3)
            self.gather_data.addItem(button)
            self.lines.setVerticalSpacing(20)
    
    # If layout is setted at other options than "cross rule" option, change layout for "cross rule".
    def set_second_layout(self):
        if self.active_layout_number == 0:
            # Set flags:
            self.active_layout_number = 1
            self.option_number = 3

            # Set label's texts:
            self.first_data.setText("")
            self.first_unit.setText("%")
            self.second_data.setText("")
            self.second_unit.setText("%")
            self.result.setText("")
            self.what_calculate.setText("Cross rule")
            self.first_label.setText("Percentage concentration of first solution:")
            self.second_label.setText("Percentage concentration of second solution:")

            button_buffor = self.gather_data.takeAt(2)
            self.third_data = QLineEdit()

            self.third_line = QHBoxLayout()

            self.third_line.addWidget(self.third_data)
            self.third_unit = QLabel("%")
            self.third_line.addWidget(self.third_unit)
            self.third_label = QLabel("Expected percentage concentration of solution:")
            self.lines.addRow(self.third_label, self.third_line)

            self.gather_data.addLayout(button_buffor)
            self.result_label.setText("Proportion (first solution:second_solution):")
            self.result_unit.setText("")
            self.lines.setVerticalSpacing(10)

    # Protection, getting result from cross rule option and show it in application.
    def cross_rule(self):

        # Check if user pass numbers:
        first_concentration = uf.isNumber(self.first_data.text())
        if first_concentration is False:  
            wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as concentration of first solution.", QMessageBox.Ok)
            return 1
            
        second_concentration = uf.isNumber(self.second_data.text())
        if second_concentration is False:  
            wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as concentration of second solution.", QMessageBox.Ok)
            return 1

        expected_concentration = uf.isNumber(self.third_data.text())
        if expected_concentration is False:  
            wrong_data = QMessageBox().warning(self, "Warning", "You should pass number as expected concentration.", QMessageBox.Ok)
            return 1
        
        # Check if user pass only intiger numbers:
        if first_concentration is float or second_concentration is float or expected_concentration is float:
            wrong_data = QMessageBox().warning(self, "Warning", "You should pass possitive intiger numbers.", QMessageBox.Ok)
            return 1

        # Check if user's data meet the conditions:

        if first_concentration < 0 or first_concentration > 100 or second_concentration < 0 or second_concentration > 100:
            wrong_data = QMessageBox().warning(self, "Warning", "Percentage concentration can be from 0 to 100.", QMessageBox.Ok)
            return 1
        
        if first_concentration == second_concentration:
            wrong_data = QMessageBox().warning(self, "Warning", "Percentage concentration can't be the same.", QMessageBox.Ok)
            return 1
        

        if first_concentration < second_concentration:
            greather_concentration = second_concentration
            lesser_concentration = first_concentration
        else:
            greather_concentration = first_concentration
            lesser_concentration = second_concentration

        if expected_concentration > greather_concentration or expected_concentration < lesser_concentration:
            wrong_data = QMessageBox().warning(self, "Warning", "Expected precentage of solution must be greather than a concentration one of mixed solution, and lesser than concentration of another one.", QMessageBox.Ok)
            return 1

        self.proportion = alg.cross_rule(first_concentration, second_concentration, expected_concentration)
        self.result.setText(str(self.proportion[0]) + ":" + str(self.proportion[1]))

    # Load pallete before preview optio.
    def load_preview_pallete(self):
        
        self.preview_pallete = self.settings_window.return_pallete_from_preview()
        if len(self.preview_pallete) != 6:
            return 1

        styles = """
            QWidget {
            background-color: """ + self.preview_pallete[0] + """;
            color: """ + self.preview_pallete[1] + """;
            }

            QPushButton {
            background-color: #005bc5;
            color: black;
            font-size: 18px;
            font-style: bold;
            width: 400px;
            height: 40px;
            background-color: """ + self.preview_pallete[2] + """;
            color: """ + self.preview_pallete[3] + """;
            }

            QPushButton#copy_button {
            width: 20px;
            height: 20px;
            }

            QLabel {
            font-size: 18px;
            font-family: Consolas;
            margin: 2px;
            }

            QLabel#title {
            font-weight: bold;
            }

            QLineEdit {
            background-color: """ + self.preview_pallete[4] + """;
            color: """ + self.preview_pallete[5] + """;
            font-size: 18px;
            }

            """

        self.setStyleSheet(styles)

    # Function creating separated setting window.
    def show_settings_window(self):

        self.settings_window = Settings_window()
        self.settings_window_exist = True

        self.settings_window.show()

        #Signals from side window:
        self.settings_window.save_pallete_button.clicked.connect(self.load_colors)
        self.settings_window.load_default_pallete_button.clicked.connect(self.load_colors)
        self.settings_window.preview_button.clicked.connect(self.load_preview_pallete)
        self.settings_window.load_previous_pallete_button.clicked.connect(self.load_colors)
        self.settings_window.load_previous_pallete_button.clicked.connect(self.settings_window.fill_color_lines)
        
        if self.settings_window.pallete_changed:
            self.load_colors()
            self.settings_window.clear_pallete_changed_flag()
        
        if self.settings_window.preview_active:
            self.settings_window.fill_color_lines()

    # Load colors from files and set them as pallete of window.
    def load_colors(self):

        path = "files\selected pallete.txt"
        exist = os.path.exists(path)

        if exist is True:
            with open(path, "r") as file:
                path = file.readline()
            exist = os.path.exists(path)
        else:
            wrong_data = QMessageBox().critical(self, "Warning", "Source file doesn't exist. Program load default pallet.", QMessageBox.Ok)
            path = "files/default color settings.txt"
        
        # Window: background-color; font-color; Button: background-color; font-color; LineEdit: background-color; font-color;
        colors = []

        if exist is True:
            with open(path, "r") as file:
                for number, line in enumerate(file):
                    if number != 5:
                        colors.append(line[:-1])
                    else:
                        colors.append(line)

        else:
            wrong_data = QMessageBox().critical(self, "Warning", "Source file doesn't exist. Reinstalation is needed.", QMessageBox.Ok)
            exit(1)

        styles = """
            QWidget{
            background-color: """ + colors[0] + """;
            color: """ + colors[1] + """;
            }

            QPushButton#side_menu {
            background-color: #005bc5;
            color: black;
            font-size: 18px;
            font-style: bold;
            margin: 0;
            width: 400px;
            height: 40px;
            background-color: """ + colors[2] + """;
            color: """ + colors[3] + """;
            }

            QPushButton {
            background-color: #005bc5;
            color: black;
            font-size: 18px;
            font-style: bold;
            height: 40px;
            background-color: """ + colors[2] + """;
            color: """ + colors[3] + """;
            }

            QPushButton#copy_button {
            width: 20px;
            height: 20px;
            }

            QLabel {
            font-size: 18px;
            font-family: Consolas;
            margin: 2px;
            }

            QLabel#title_bar_title {
            font-weight: bold;
            font-size: 20px;
            }
            
            QLabel#title {
            font-weight: bold;
            }

            QLineEdit {
            background-color: """ + colors[4] + """;
            border-color: """ + colors[4] + """;
            color: """ + colors[5] + """;
            font-size: 18px;
            }
            """
        self.setStyleSheet(styles)

    # Get possition of pressed mouse.
    def mousePressEvent(self, event):
        self.old_position = event.globalPos()
    
    # Move window with mouse.
    def mouseMoveEvent(self, event):
        self.old_position = QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + self.old_position.x(), self.y() + self.old_position.y())
        self.old_position = event.globalPos()
