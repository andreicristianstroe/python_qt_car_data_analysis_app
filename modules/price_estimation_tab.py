# Third-party imports
import pandas as pd
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QVBoxLayout, QHBoxLayout
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder


class PriceEstimationTab(QWidget):
    """Class for creating the Price Estimation tab."""

    def __init__(self, dataframe):
        super().__init__()
        self.estimated_price_label = None
        self.year_entry = None
        self.make_combobox = None
        self.dataframe = dataframe
        self.preprocessor = None
        self.model = None
        self.create_widgets()
        self.prepare_data()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        # Make selection
        make_layout = QHBoxLayout()
        make_label = QLabel("Select the manufacturer:")
        make_layout.addWidget(make_label)

        unique_makes = [str(make) for make in self.dataframe["Make"].unique()]
        self.make_combobox = QComboBox()
        self.make_combobox.addItems(unique_makes)
        make_layout.addWidget(self.make_combobox)

        # Year input
        year_layout = QHBoxLayout()
        year_label = QLabel("Type a future year:")
        year_layout.addWidget(year_label)
        self.year_entry = QLineEdit()
        year_layout.addWidget(self.year_entry)

        # Combine layouts
        layout.addLayout(make_layout)
        layout.addLayout(year_layout)

        # Estimate button
        estimate_button = QPushButton("Estimate Price")
        estimate_button.clicked.connect(self.estimate_price)
        layout.addWidget(estimate_button)

        # Estimated price label
        self.estimated_price_label = QLabel("")
        layout.addWidget(self.estimated_price_label)

    def prepare_data(self):
        """Prepare the data for modeling."""
        x = self.dataframe[["Make", "Year", "Horsepower", "Torque"]]
        y = self.dataframe["Price"]
        categorical_columns = ["Make"]
        self.preprocessor = ColumnTransformer(
            transformers=[("cat", OneHotEncoder(), categorical_columns)],
            remainder="passthrough",
        )
        x_encoded = self.preprocessor.fit_transform(x)
        self.model = LinearRegression()
        self.model.fit(x_encoded, y)

    def estimate_price(self):
        """Estimate the price based on user inputs."""
        user_make = self.make_combobox.currentText()
        user_year = self.year_entry.text()
        if not user_make or not user_year:
            self.estimated_price_label.setText("Please fill in both input fields.")
            return
        try:
            user_year = int(user_year)
        except ValueError:
            self.estimated_price_label.setText("Please enter a valid numeric year.")
            return
        future_data = pd.DataFrame(
            {"Make": [user_make], "Year": [user_year], "Horsepower": [200], "Torque": [200]}
        )
        x_input = future_data[["Make", "Year", "Horsepower", "Torque"]]
        x_input_encoded = self.preprocessor.transform(x_input)
        estimated_price = self.model.predict(x_input_encoded)
        self.estimated_price_label.setText(f"Estimated Price: ${estimated_price[0]:.2f}")
