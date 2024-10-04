import sys
import numpy as np
import matplotlib.pyplot as plt
import cirq
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog, QMessageBox,
    QComboBox, QCheckBox, QScrollArea
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class QuantumErrorCorrectionSoftware(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QEC - Simulator")
        self.setGeometry(100, 100, 1400, 1000) 
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Parameters
        self.lattice_size = 5
        self.error_rate = 0.1
        self.error_type = "Depolarizing"
        self.visualization_style = "Coolwarm"
        self.error_correction_algorithm = "None"

        self.selected_visualizations = {}

        self.circuit_manager = None
        self.simulation_manager = None
        self.visualization_manager = None

        # GUI components
        self.create_widgets()
        self.visualization_manager = VisualizationManager(self.display_area)

    def create_widgets(self):
        self.title_label = QLabel("Quantum Error Correction Simulator", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px; color: #34495E;")
        self.layout.addWidget(self.title_label)

        form_layout = QGridLayout()

        # Parameters
        form_layout.addWidget(QLabel("Lattice Size (NxN):"), 0, 0)
        self.lattice_size_input = QLineEdit("5")
        form_layout.addWidget(self.lattice_size_input, 0, 1)

        form_layout.addWidget(QLabel("Error Rate (0 to 1):"), 1, 0)
        self.error_rate_input = QLineEdit("0.1")
        form_layout.addWidget(self.error_rate_input, 1, 1)

        form_layout.addWidget(QLabel("Error Type:"), 2, 0)
        self.error_type_combo = QComboBox()
        self.error_type_combo.addItems(["Bit-flip", "Phase-flip", "Depolarizing"])
        form_layout.addWidget(self.error_type_combo, 2, 1)

        # Error visualization styles
        form_layout.addWidget(QLabel("Visualization Style:"), 3, 0)
        self.visualization_style_combo = QComboBox()
        self.visualization_style_combo.addItems(["Coolwarm", "Viridis", "Plasma"])
        form_layout.addWidget(self.visualization_style_combo, 3, 1)

        # Error correction algorithms
        form_layout.addWidget(QLabel("Error Correction Algorithm:"), 4, 0)
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["None", "Shor Code", "Steane Code"])
        form_layout.addWidget(self.algorithm_combo, 4, 1)

        # Visualizations selection
        form_layout.addWidget(QLabel("Visualizations:"), 6, 0)
        self.visualization_options = {
            'Lattice Before Error Correction': QCheckBox('Lattice Before Error Correction'),
            'Measurement Results': QCheckBox('Measurement Results'),
            'Lattice After Error Correction': QCheckBox('Lattice After Error Correction'),
            'Qubit State Probabilities': QCheckBox('Qubit State Probabilities'),
            'Circuit Diagram': QCheckBox('Circuit Diagram')
        }
        visualizations_layout = QVBoxLayout()
        for checkbox in self.visualization_options.values():
            checkbox.setChecked(True) 
            visualizations_layout.addWidget(checkbox)
        form_layout.addLayout(visualizations_layout, 6, 1)

        self.layout.addLayout(form_layout)

        # Run Simulation Button
        self.run_button = QPushButton("Run Simulation", self)
        self.run_button.clicked.connect(self.run_simulation)
        self.layout.addWidget(self.run_button)

        # Load Simulation 
        self.load_button = QPushButton("Load Simulation", self)
        self.load_button.clicked.connect(self.load_simulation)
        self.layout.addWidget(self.load_button)

        # Save Simulation 
        self.save_button = QPushButton("Save Simulation Results", self)
        self.save_button.clicked.connect(self.save_simulation_results)
        self.layout.addWidget(self.save_button)

        # Display Area 
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.display_area = QWidget()
        self.scroll_area.setWidget(self.display_area)
        self.layout.addWidget(self.scroll_area)

    def run_simulation(self):
        try:
            # Get user input
            self.lattice_size = int(self.lattice_size_input.text())
            self.error_rate = float(self.error_rate_input.text())
            self.error_type = self.error_type_combo.currentText()
            self.visualization_style = self.visualization_style_combo.currentText()
            self.error_correction_algorithm = self.algorithm_combo.currentText()

            if not (0 <= self.error_rate <= 1):
                raise ValueError("Error rate must be between 0 and 1.")
        except ValueError as ve:
            QMessageBox.warning(self, "Input Error", f"Invalid input: {ve}")
            return

        # Get visualization options
        self.selected_visualizations = {name: checkbox.isChecked() for name, checkbox in self.visualization_options.items()}

        # Clear previous display widgets in the display area
        for widget in self.visualization_manager.display_area.findChildren(QWidget):
            widget.deleteLater()

        # Create the quantum circuit with errors injected
        self.circuit_manager = CircuitManager(self.lattice_size, self.error_rate, self.error_type, self.error_correction_algorithm)
        self.circuit_manager.apply_hadamard_and_cnot()
        self.circuit_manager.inject_errors()

        # Add measurements before the first simulation
        self.circuit_manager.measure_stabilizers()

        # Instantiate the simulation manager 
        circuit = self.circuit_manager.get_circuit()
        self.simulation_manager = SimulationManager(circuit)

        # Visualize the lattice before error correction (if selected)
        if self.selected_visualizations.get('Lattice Before Error Correction', False):
            result_before = self.simulation_manager.run_simulation()
            lattice_before_fig = self.simulation_manager.visualize_lattice(self.lattice_size, result_before, self.visualization_style)
            self.visualization_manager.display_figure(lattice_before_fig, title="Lattice Before Error Correction")

        else:
            result_before = self.simulation_manager.run_simulation()

        # Apply chosen error correction algorithm
        self.apply_error_correction()  

        # Add measurements for post-correction visualization
        self.circuit_manager.measure_stabilizers_post_correction() 

        # Run the simulation after correction
        result_after = self.simulation_manager.run_simulation()

        # Visualize the results after error correction
        if self.selected_visualizations.get('Measurement Results', False):
            measurement_fig = self.simulation_manager.visualize_measurement_results(result_after)
            self.visualization_manager.display_figure(measurement_fig, title="Measurement Results")

        if self.selected_visualizations.get('Lattice After Error Correction', False):
            lattice_after_fig = self.simulation_manager.visualize_lattice(self.lattice_size, result_after, self.visualization_style)
            self.visualization_manager.display_figure(lattice_after_fig, title="Lattice After Error Correction")


        # Visualize the circuit diagram
        if self.selected_visualizations.get('Circuit Diagram', False):
            circuit_fig = self.visualize_circuit_graphically(circuit)  # Updated method for graphical visualization
            self.visualization_manager.display_figure(circuit_fig, title="Circuit Diagram")

    def apply_error_correction(self):
        """Apply the selected error correction algorithm."""
        if self.error_correction_algorithm == "Shor Code":
            self.circuit_manager.apply_shor_code()
        elif self.error_correction_algorithm == "Steane Code":
            self.circuit_manager.apply_steane_code()

    def visualize_circuit_graphically(self, circuit):
        """Generate a visualization of the quantum circuit using Matplotlib."""
        fig, ax = plt.subplots(figsize=(15, 6))  
        ax.axis('off')  


        circuit_diagram = circuit.to_text_diagram()  
        ax.text(0.5, 0.5, circuit_diagram, family='monospace', fontsize=10, ha='center', va='center')
        return fig

    def save_simulation_results(self):
        """Save the results of the simulation to a JSON file."""
        if self.simulation_manager and self.simulation_manager.result_data:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "JSON Files (*.json)")
            if file_path:
                results = self.simulation_manager.result_data
                LoggingManager.log_simulation_results(results, file_path)
                QMessageBox.information(self, "Save Success", "Simulation results saved successfully.")
        else:
            QMessageBox.warning(self, "No Results", "No simulation results to save.")

    def load_simulation(self):
        """Load and display results from a previous simulation."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Results", "", "JSON Files (*.json)")
        if file_path:
            try:
                results = LoggingManager.load_simulation_log(file_path)
                QMessageBox.information(self, "Load Success", "Simulation results loaded successfully.")
                circuit_fig = self.visualize_circuit_graphically(cirq.Circuit(cirq.Circuit.from_ops(cirq.read_json(json_text=results['circuit']))))
                self.visualization_manager.display_figure(circuit_fig)
                measurement_fig = self.simulation_manager.visualize_measurement_results_from_data(results['measurements'])
                self.visualization_manager.display_figure(measurement_fig)
                lattice_fig = self.simulation_manager.visualize_lattice_from_data(self.lattice_size, results['lattice'], self.visualization_style)
                self.visualization_manager.display_figure(lattice_fig)
            except Exception as e:
                QMessageBox.warning(self, "Load Error", f"Failed to load simulation: {e}")


class CircuitManager:
    def __init__(self, size, error_rate, error_type, algorithm):
        self.size = size
        self.error_rate = error_rate
        self.error_type = error_type
        self.algorithm = algorithm
        self.qubits = [cirq.GridQubit(i, j) for i in range(size) for j in range(size)]
        self.circuit = cirq.Circuit()

    def apply_hadamard_and_cnot(self):
        """Apply Hadamard and CNOT gates to initialize the lattice."""
        for qubit in self.qubits:
            self.circuit.append(cirq.H(qubit))

        for i in range(self.size):
            for j in range(self.size):
                q = cirq.GridQubit(i, j)
                if i + 1 < self.size:
                    q_right = cirq.GridQubit(i + 1, j)
                    self.circuit.append(cirq.CNOT(q, q_right))
                if j + 1 < self.size:
                    q_down = cirq.GridQubit(i, j + 1)
                    self.circuit.append(cirq.CNOT(q, q_down))

    def apply_shor_code(self):
        """Apply Shor's error correction code to the circuit."""
        # Encode logical qubit using bit-flip repetition (3 qubits)
        if len(self.qubits) < 9:
            raise ValueError("Shor's code requires at least 9 qubits.")

        logical_qubit = self.qubits[0]
        physical_qubits = self.qubits[:9]

        # Bit-flip repetition
        self.circuit.append(cirq.CNOT(logical_qubit, physical_qubits[1]))
        self.circuit.append(cirq.CNOT(logical_qubit, physical_qubits[2]))

        # Phase-flip repetition on each of the three qubits
        for i in range(0, 9, 3):
            self.circuit.append(cirq.H(physical_qubits[i]))
            self.circuit.append(cirq.CNOT(physical_qubits[i], physical_qubits[i + 1]))
            self.circuit.append(cirq.CNOT(physical_qubits[i], physical_qubits[i + 2]))
            self.circuit.append(cirq.H(physical_qubits[i]))

        # Measure stabilizers (error syndromes)
        for i in range(3):
            self.circuit.append(cirq.measure(physical_qubits[i * 3:(i + 1) * 3], key=f'syndrome_{i}'))

        # Simple error correction based on measured syndromes 
        for i in range(3):
            self.circuit.append(cirq.CNOT(physical_qubits[i * 3], physical_qubits[i * 3 + 1]))
            self.circuit.append(cirq.CNOT(physical_qubits[i * 3], physical_qubits[i * 3 + 2]))

    def apply_steane_code(self):
        """Apply Steane's error correction code to the circuit."""
        # Encode 1 qubit into 7 physical qubits
        if len(self.qubits) < 7:
            raise ValueError("Steane's code requires at least 7 qubits.")

        logical_qubit = self.qubits[0]
        physical_qubits = self.qubits[:7]

        # Apply Hadamard and CNOT gates to encode the logical qubit
        for qubit in physical_qubits:
            self.circuit.append(cirq.H(qubit))

        # Apply encoding stabilizers
        for i in range(3):
            self.circuit.append(cirq.CNOT(physical_qubits[i], physical_qubits[i + 3]))

        # Measure stabilizers to detect errors
        for i in range(3):
            self.circuit.append(cirq.measure(physical_qubits[i * 2:(i + 1) * 2], key=f'syndrome_{i}'))

        # Simple error correction based on syndromes 
        for i in range(3):
            self.circuit.append(cirq.CNOT(physical_qubits[i], physical_qubits[i + 3]))

    def inject_errors(self):
        """Inject random errors based on user-selected error type."""
        for qubit in self.qubits:
            rand_val = np.random.rand()
            if self.error_type == "Bit-flip" and rand_val < self.error_rate:
                self.circuit.append(cirq.X(qubit))
            elif self.error_type == "Phase-flip" and rand_val < self.error_rate:
                self.circuit.append(cirq.Z(qubit))
            elif self.error_type == "Depolarizing":
                if rand_val < self.error_rate:
                    self.circuit.append(cirq.X(qubit))
                elif rand_val < 2 * self.error_rate:
                    self.circuit.append(cirq.Z(qubit))
                elif rand_val < 3 * self.error_rate:
                    self.circuit.append(cirq.Y(qubit))

    def measure_stabilizers(self):
        """Measure stabilizers using unique measurement keys."""
        for i, qubit in enumerate(self.qubits):
            self.circuit.append(cirq.measure(qubit, key=f'm{i}_step1'))

    def measure_stabilizers_post_correction(self):
        """Measure stabilizers with unique keys after error correction."""
        for i, qubit in enumerate(self.qubits):
            self.circuit.append(cirq.measure(qubit, key=f'm{i}_step2'))

    def get_circuit(self):
        return self.circuit


class SimulationManager:
    def __init__(self, circuit, repetitions=1000):
        self.circuit = circuit
        self.repetitions = repetitions
        self.simulator = cirq.Simulator()
        self.result_data = None

    def run_simulation(self):
        """Run the quantum circuit simulation."""
        result = self.simulator.run(self.circuit, repetitions=self.repetitions)
        self.result_data = {
            'circuit': cirq.to_json(self.circuit),
            'measurements': result.data.to_dict(),
        }
        return result

    def visualize_measurement_results(self, result):
        """Plot the measurement results."""
        data = result.data
        bitstring_series = data.apply(lambda row: ''.join(row.astype(str)), axis=1)
        counts = bitstring_series.value_counts()

        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot.bar(ax=ax)
        ax.set_xlabel('Measurement Outcome')
        ax.set_ylabel('Counts')
        ax.set_title('Measurement Results')
        return fig

    def visualize_lattice(self, size, result, style="coolwarm"):
        """Visualize the surface code lattice with measurement results."""
        data = result.data
        measurement = data.iloc[0]  
        lattice = np.zeros((size, size))

        for i in range(size):
            for j in range(size):
                index = i * size + j
                key = f'm{index}_step1'  
                if key in measurement:
                    lattice[i, j] = measurement[key]

        fig, ax = plt.subplots()
        cax = ax.matshow(lattice, cmap=style.lower()) 
        fig.colorbar(cax)
        ax.set_title('Surface Code Lattice Measurement')
        return fig

    def show_qubit_states(self, result):
        """Display the qubit states and probabilities."""
        qubit_probs = result.data.describe().transpose()['mean']  
        fig, ax = plt.subplots(figsize=(12, 6))
        qubit_probs.plot.bar(ax=ax)
        ax.set_xlabel('Qubits')
        ax.set_ylabel('Probability')
        ax.set_title('Qubit State Probabilities')
        return fig

    def visualize_measurement_results_from_data(self, measurements):
        """Visualize measurement results from saved data."""
        data = pd.DataFrame(measurements)
        bitstring_series = data.apply(lambda row: ''.join(row.astype(str)), axis=1)
        counts = bitstring_series.value_counts()

        fig, ax = plt.subplots(figsize=(12, 6))
        counts.plot.bar(ax=ax)
        ax.set_xlabel('Measurement Outcome')
        ax.set_ylabel('Counts')
        ax.set_title('Measurement Results')
        return fig

    def visualize_lattice_from_data(self, size, lattice_data, style="coolwarm"):
        """Visualize lattice from saved data."""
        lattice = np.array(lattice_data)
        fig, ax = plt.subplots()
        cax = ax.matshow(lattice, cmap=style.lower())
        fig.colorbar(cax)
        ax.set_title('Surface Code Lattice Measurement')
        return fig


class VisualizationManager:
    def __init__(self, display_area):
        self.display_area = display_area
        self.ensure_layout()
        self.pop_out_windows = []

    def ensure_layout(self):
        """Ensure the display area has a layout."""
        if self.display_area.layout() is None:
            self.display_area.setLayout(QVBoxLayout())

    def display_figure(self, fig, title="Figure"):
        """Display a matplotlib figure in the PyQt5 window."""
        self.ensure_layout()  
        canvas = FigureCanvas(fig)
        canvas.draw()


        container_widget = QWidget()
        container_layout = QVBoxLayout()
        container_widget.setLayout(container_layout)
        container_layout.addWidget(canvas)

        pop_out_button = QPushButton("Pop Out")
        container_layout.addWidget(pop_out_button)
        pop_out_button.clicked.connect(lambda: self.pop_out_figure(fig, title))


        self.display_area.layout().addWidget(container_widget)
        plt.close(fig)

    def pop_out_figure(self, fig, title="Figure"):
        """Create a new window to display the figure."""
        pop_out_window = FigureWindow(fig, title)
        pop_out_window.show()
        self.pop_out_windows.append(pop_out_window)


class FigureWindow(QWidget):
    def __init__(self, fig, title="Figure"):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        canvas = FigureCanvas(fig)
        canvas.draw()
        self.layout.addWidget(canvas)


class LoggingManager:
    @staticmethod
    def log_simulation_results(results, filepath):
        with open(filepath, 'w') as file:
            json.dump(results, file)

    @staticmethod
    def load_simulation_log(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuantumErrorCorrectionSoftware()
    window.show()
    sys.exit(app.exec_())
