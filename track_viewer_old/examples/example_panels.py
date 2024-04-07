"""
Example for use with panels, both created by code or designed with Qt designer, and update functions
"""

# Imports
import sys

from guitoolbox.panel import Panel

# GUI toolbox imports
from guitoolbox.panels_gui import PanelsGUI
from guitoolbox.ui.example import Ui_Form
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton

"""
Panel with labels
"""


class Panel1(Panel):
    def __init__(self) -> None:
        # Call super class function
        super().__init__("panel_1")

        # Create layout with labels
        self.hbox_layout = QHBoxLayout()
        self.label1 = QLabel("Test 1")
        self.label2 = QLabel("Test 2")
        self.hbox_layout.addWidget(self.label1)
        self.hbox_layout.addWidget(self.label2)
        self.setLayout(self.hbox_layout)

    # Override
    def update_panel(self, source_name: str, data: dict):
        # Print data
        print(f"name: {self.name}, source: {source_name} data: {data}")

        # Set label
        self.label1.setText(str(source_name))
        self.label2.setText(str(data))

        # Call super class function
        return super().update_panel(source_name, data)


"""
Panel with buttons
"""


class Panel2(Panel):
    def __init__(self) -> None:
        # Call super class function
        super().__init__("panel_2")

        # Create layout with buttons
        self.hbox_layout = QHBoxLayout()
        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.hbox_layout.addWidget(self.button1)
        self.hbox_layout.addWidget(self.button2)
        self.setLayout(self.hbox_layout)

        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)

    # Override
    def update_panel(self, source_name: str, data: dict):
        # Print data
        print(f"name: {self.name}, source: {source_name} data: {data}")

        # Set button text
        if source_name == "panel_3" and "combobox" in data:
            self.button2.setText(data["combobox"])

        # Call super class function
        return super().update_panel(source_name, data)

    def button1_clicked(self):
        # Send data to panel 1
        self.publish({"name": self.name, "button": 1}, "panel_1")

    def button2_clicked(self):
        # Send data to all panels
        self.publish({"name": self.name, "button": 2})


"""
Panel based on UI file generated with the Qt designer
"""


class Panel3(Panel, Ui_Form):
    def __init__(self):
        super(Panel3, self).__init__("panel_3")

        # Init widget
        self.setupUi(self)

        self.checkbox.clicked.connect(self.checkbox_clicked)
        self.combobox.currentIndexChanged.connect(self.combobox_changed)

    # Override
    def update_panel(self, source_name: str, data: dict):
        # Print data
        print(f"name: {self.name}, source: {source_name} data: {data}")

        # Call super class function
        return super().update_panel(source_name, data)

    def checkbox_clicked(self):
        # Send data to all panels
        self.publish({"name": self.name, "checkbox": self.checkbox.isChecked()})

    def combobox_changed(self):
        # Send data to to panel 2
        self.publish(
            {"name": self.name, "combobox": self.combobox.currentText()}, "panel_2"
        )


if __name__ == "__main__":
    # Init application
    app = QApplication(sys.argv)

    # Create panels GUI
    panels_gui = PanelsGUI()

    # Add panel 1
    panel_1 = Panel1()
    panels_gui.add_panel(panel_1, 0, 0, title="Panel 1")

    # Add example widget 2
    panel_2 = Panel2()
    panels_gui.add_panel(panel_2, 1, 0, col_span=3, title="Panel 2")

    # Add example widget 2
    panel_3 = Panel3()
    panels_gui.add_panel(panel_3, 0, 2, title="Panel 3")

    # Run application
    sys.exit(app.exec())
