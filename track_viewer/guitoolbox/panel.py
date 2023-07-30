"""
Panel widget, which can be used as a base class.
The update_panel function has t0 be reimplemented in order to process received data
"""

# Imports
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, Signal

class Communicate(QObject):
    def __init__(self) -> None:
        # Init object
        QObject.__init__(self)

        # Variables
        self._signal = Signal(dict, str, str)

    @property
    def signal(self) -> Signal:
        return self._signal

class Panel(QWidget):
    def __init__(self, name: str) -> None:
        """
        Panel constructor

        Parameters
        ----------
        name : str, required
            Name of the panel

        Returns
        -------
        None
        """
        
        # Init widget
        QWidget.__init__(self)

        # Variables
        self._name = name

        # Create signal
        self._signal = Communicate().signal

    @property
    def name(self) -> str:
        return self._name
        
    @property
    def signal(self) -> Signal:
        return self._signal

    def update_panel(self, source_name: str, data: dict) -> None:
        """
        Function which is called when the panel receives an update. User needs to
        reimplement this function

        Parameters
        ----------
        source_name : str, required
            Name of the panel who send the update
        data : dict, required
            Data dict being received

        Returns
        -------
        None
        """

        raise NotImplementedError

    def publish(self, data: dict, dest_name: str = '') -> None:
        """
        Publishes the data. When no panel name is supplied, all the
        panels will be updated, else only the panel with the given name.

        Parameters
        ----------
        data : dict, required
            Data dict to send
        dest_name : str, optional
            Name of the panel to be updated

        Returns
        -------
        None
        """

        # Send data
        self._signal.emit(data, self.name, dest_name)
