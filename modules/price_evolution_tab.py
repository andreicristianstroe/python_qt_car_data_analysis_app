# Third-party imports
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class PriceEvolutionTab(QWidget):
    """Class for creating the Price Evolution tab."""

    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe
        self.model_var = ""
        self.engine_var = ""
        self.canvas = None
        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        unique_models = [model.strip() for model in self.dataframe["Model"].unique()]
        unique_engines = [engine.strip() for engine in self.dataframe["Engine"].unique()]
        labels = ["Select your desired car model:", "Select your desired engine:"]
        values = [unique_models, unique_engines]

        for label, value in zip(labels, values):
            model_label = QLabel(label)
            layout.addWidget(model_label)
            model_dropdown = QComboBox()
            model_dropdown.addItems(value)
            layout.addWidget(model_dropdown)
            model_dropdown.currentTextChanged.connect(lambda text, var=label: self.update_var(text, var))

        plot_price_evolution_button = QPushButton("Generate Price Evolution")
        plot_price_evolution_button.clicked.connect(self.plot_price_evolution)
        layout.addWidget(plot_price_evolution_button)

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(10, 6)))
        layout.addWidget(self.canvas)

    def update_var(self, text, var):
        if "model" in var.lower():
            self.model_var = text
        elif "engine" in var.lower():
            self.engine_var = text

    def plot_price_evolution(self):
        selected_car_model, engine = self.model_var, self.engine_var
        filtered_data = self.dataframe[
            (self.dataframe["Model"] == selected_car_model) & (self.dataframe["Engine"] == engine)]

        plt.clf()
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_data["Year"], filtered_data["Price"], marker="o", linestyle="-")
        plt.title(f"Price Evolution for {selected_car_model} - {engine}")
        plt.xlabel("Year")
        plt.ylabel("Price")
        plt.grid(True)

        self.canvas.figure.clf()
        ax = self.canvas.figure.subplots()
        ax.plot(filtered_data["Year"], filtered_data["Price"], marker="o", linestyle="-")
        ax.set_title(f"Price Evolution for {selected_car_model} - {engine}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Price")
        ax.grid(True)
        self.canvas.draw()
