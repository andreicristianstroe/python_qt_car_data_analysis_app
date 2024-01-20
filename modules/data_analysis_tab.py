# Third-party imports
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from pandasgui import show


class DataAnalysisTab(QWidget):
    """Class for creating the Data Analysis tab."""

    def __init__(self, dataframe):
        super().__init__()
        self.analysis_result = None
        self.canvas = None
        self.attribute_selection = None
        self.dataframe = dataframe
        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        attribute_label = QLabel("Select your desired car attribute:")
        layout.addWidget(attribute_label)

        self.attribute_selection = QComboBox()
        self.attribute_selection.addItems(list(self.dataframe.columns))
        layout.addWidget(self.attribute_selection)

        analyze_button = QPushButton("Analyze Attribute")
        analyze_button.clicked.connect(self.analyze_data)
        layout.addWidget(analyze_button)

        pandasgui_button = QPushButton("Open in PandasGUI")
        pandasgui_button.clicked.connect(self.open_pandasgui)
        layout.addWidget(pandasgui_button)

        self.analysis_result = QLabel("")
        layout.addWidget(self.analysis_result)

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(8, 6)))
        layout.addWidget(self.canvas)

    def analyze_data(self):
        selected_attribute = self.attribute_selection.currentText()
        if selected_attribute:
            x_values = self.dataframe[[selected_attribute]]
            y_values = self.dataframe["Price"]
            x_train, x_test, y_train, y_test = train_test_split(
                x_values, y_values, test_size=0.2, random_state=0
            )

            model = LinearRegression()
            model.fit(x_train, y_train)
            y_pred = model.predict(x_test)

            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            ax = self.canvas.figure.subplots()
            ax.clear()
            ax.scatter(x_test, y_test, color="blue", label="Actual Prices")
            ax.plot(x_test, y_pred, color="red", linewidth=2, label="Predicted Prices")
            ax.set_xlabel(selected_attribute)
            ax.set_ylabel("Price")
            ax.set_title(f"{selected_attribute} vs. Price")
            ax.legend()
            ax.grid(True)
            self.canvas.figure.canvas.draw()

            self.analysis_result.setText(f"Mean Squared Error: {mse:.2f}\nR-squared: {r2:.2f}")

    def open_pandasgui(self):
        """Function to open the dataframe in pandasgui."""
        show(self.dataframe)
