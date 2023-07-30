"""
GUI containing all the panels ordered on a grid.
"""

# Imports
from typing import List, Optional
from PySide6.QtWidgets import QGroupBox, QGridLayout, QWidget
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt

# GUI toolbox imports
from guitoolbox.panel import Panel
from guitoolbox.panels.button_bar import ButtonBarPanel
from guitoolbox.panels.track import TrackPanel

class PanelsGUI(QWidget):
    def __init__(self, width: int = 800, height: int = 600, title: str = "Panels GUI"):
        """
        Parameters
        ----------
        width : int, optional
            Width of the GUI in pixels
        height : int, optional
            Height of the GUI in pixels
        title : str, optional
            Title of the GUI

        Returns
        -------
        None
        """
        
        # Init widget
        QWidget.__init__(self)
        self._panels: List[Panel] = []

        # Resize GUI and set title
        self.resize(width, height)
        self.setWindowTitle(title)

        # Basic layout
        self._layout = QGridLayout()
        self.setLayout(self._layout)
        self.setFocus()
        self.button_bar_panel = None
        self.track_view = None
        self.showFullScreen()

        # Show GUI
        self.show()

    def _update_panels(self, data: dict, source_name: str, dest_name: str = '') -> None:
        """
        Updates the panels in the GUI. When no panel name is supplied, all the
        panels will be updated, else only the panel with the given name.

        Parameters
        ----------
        data : dict, required
            Data dict to send
        source_name : str, required
            Name of the panel who send the update
        dest_name : str, optional
            Name of the panel to be updated

        Returns
        -------
        None
        """

        # Update each panel
        for panel in self._panels:
            if not dest_name or dest_name == panel.name:
                panel.update_panel(source_name, data)

    def add_panel(
            self,
            panel: Panel,
            row: int,
            col: int,
            row_span: int = 1,
            col_span: int = 1,
            title: Optional[str] = None
        ) -> None:
        """
        Parameters
        ----------
        widget : QWidget, required
            Widget object to be added
        row : int, required
            Zero indexed row of the grid layout where the widget is placed
        col : int, required
            Zero indexed column of the grid layout where the widget is placed
        row_span : int, optional
            Amount of rows the widget is spanning the grid layout
        col_span : int, optional
            Amount of columns the widget is spanning the grid layout
        title : str, optional
            Title of the groupbox

        Returns
        -------
        None
        """
        
        # Add panel to list of panels and connect update function to signal
        self._panels.append(panel)
        panel.signal.connect(self._update_panels)
        
        # Create a group box
        groupbox = QGroupBox()
        # Add panel widget to the groupbox
        layout = QGridLayout()
        layout.addWidget(panel, 0, 0)
        groupbox.setLayout(layout)

        # Add groupbox to layout
        self._layout.addWidget(groupbox, row, col, row_span, col_span)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Override QWidget keyPressEvent
        """

        key = event.key()
        if self.button_bar_panel is None:
            self.button_bar_panel = [x for x in self._panels if isinstance(x,ButtonBarPanel)][0]
            self.track_view = [x for x in self._panels if isinstance(x,TrackPanel)][0].track_view
        button_bar = self.button_bar_panel
        action_lut = {
            Qt.Key.Key_H:button_bar.decrease_large,
            Qt.Key.Key_J:button_bar.decrease_small,
            Qt.Key.Key_K:button_bar.increase_small,
            Qt.Key.Key_L:button_bar.increase_large,
            Qt.Key.Key_Q:self.close,
            Qt.Key.Key_A:self.track_view.zoom_out,
            Qt.Key.Key_S:self.track_view.zoom_in,
            Qt.Key.Key_Y:self.track_view.toggle_ylabel,
        }
        if key in action_lut:
            action_lut[key]()

        return super().keyPressEvent(event)
