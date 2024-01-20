# Standard library imports
import sys

# Third-party imports
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

# Local imports
from modules.car_model_hierarchy_tab import CarModelHierarchyTab
from modules.data_analysis_tab import DataAnalysisTab
from modules.display_data_tab import DisplayDataTab
from modules.price_estimation_tab import PriceEstimationTab
from modules.price_evolution_tab import PriceEvolutionTab


def clean_data(data_frame):
    """Clean the data frame columns."""
    data_frame["Price"] = data_frame["Price"].str.replace(",", "").astype(int)
    for col in ["Model", "Engine"]:
        data_frame[col] = data_frame[col].str.strip("[]")


def load_data(file_path):
    """Load data from a file path."""
    try:
        df = pd.read_csv(file_path)
        clean_data(df)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


class MainApplication(QMainWindow):
    """Main application class."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Data Analysis App")
        self.resize(1280, 720)

        # Creating Tab Widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Loading data
        data = load_data("data/database.csv")

        # Adding tabs
        self.add_tab(DisplayDataTab, "Display Data", data)
        self.add_tab(DataAnalysisTab, "Data Analysis", data)
        self.add_tab(CarModelHierarchyTab, "Car Model Hierarchy", data)
        self.add_tab(PriceEvolutionTab, "Price Evolution", data)
        self.add_tab(PriceEstimationTab, "Price Estimation", data)

    def add_tab(self, tab_class, title, dataframe):
        tab = tab_class(dataframe)
        self.tab_widget.addTab(tab, title)


# Main Function
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec())
