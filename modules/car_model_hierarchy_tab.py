# Third-party imports
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QTreeView, QVBoxLayout


class CarModelHierarchyTab(QWidget):
    """Class for creating the Car Model Hierarchy tab."""

    def __init__(self, dataframe):
        super().__init__()
        self.model = None
        self.dataframe = dataframe
        self.tree = None
        self.create_widgets()
        self.populate_tree()

    def create_widgets(self):
        """Create widgets for the Car Model Hierarchy tab."""
        layout = QVBoxLayout(self)
        self.tree = QTreeView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Car Model", "Price/Quality Ratio", "Price"])
        self.tree.setModel(self.model)
        layout.addWidget(self.tree)

    def populate_tree(self):
        """Populate the tree view with car data."""
        for _, car_row in self.dataframe.iterrows():
            price_quality_ratio = self.calculate_price_quality_ratio(car_row)
            if price_quality_ratio is not None:
                car_model = f"{car_row['Make']} {car_row['Model']} ({car_row['Year']})"
                price = float(car_row['Price'])
                items = [
                    QStandardItem(car_model),
                    QStandardItem(f"{price_quality_ratio:.4f}"),
                    QStandardItem(f"${price:.2f}")
                ]
                self.model.appendRow(items)

    @staticmethod
    def calculate_price_quality_ratio(row):
        """Calculate the price/quality ratio for a given car row."""
        power_weight = 0.4
        features_weight = 0.3
        fuel_consumption_weight = 0.3
        try:
            power_score = float(row["Horsepower"])
            features_score = float(row["Torque"])
            fuel_consumption_score = float(row["Consumption"])
            row_price = float(row["Price"])
        except ValueError:
            return None
        if power_score == 0 or features_score == 0 or fuel_consumption_score == 0:
            return None
        price_quality_ratio = (
                (power_score * power_weight
                 + features_score * features_weight
                 + fuel_consumption_score * fuel_consumption_weight)
                / row_price
        )
        return price_quality_ratio
