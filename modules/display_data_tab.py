# Third-party imports
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractItemView


class DisplayDataTab(QWidget):
    """Class for creating the Display Data tab."""

    def __init__(self, dataframe):
        """Initialize the tab with the parent widget and the data."""
        super().__init__()
        self.dataframe = dataframe
        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the Display Data tab."""
        layout = QVBoxLayout(self)

        data_label = QLabel("Car Data Overview:")
        layout.addWidget(data_label)

        table = QTableWidget()
        table.setRowCount(self.dataframe.shape[0])
        table.setColumnCount(self.dataframe.shape[1])
        table.setHorizontalHeaderLabels(self.dataframe.columns)

        for row in range(self.dataframe.shape[0]):
            for col in range(self.dataframe.shape[1]):
                item = QTableWidgetItem(str(self.dataframe.iat[row, col]))
                table.setItem(row, col, item)

        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(table)

        self.setLayout(layout)
