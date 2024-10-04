# Quantum Error Correction Simulator

The **Quantum Error Correction Simulator** is a software tool designed to simulate and visualize quantum error correction processes. It integrates various components to allow users to configure, run, and analyze quantum simulations effectively.

## **Key Components**

- **Graphical User Interface (GUI)**
  - Built using PyQt5.
  - Provides input fields, dropdown menus, checkboxes, and buttons for user interaction.
  - Includes a display area for visualizations.

- **Quantum Circuit Management**
  - Utilizes the Cirq library to construct quantum circuits.
  - Supports applying quantum gates such as Hadamard and CNOT.
  - Allows injection of errors based on user-defined parameters.

- **Simulation Engine**
  - Executes quantum circuits using Cirq's simulator.
  - Configurable number of repetitions for simulations.
  - Collects measurement results and qubit state probabilities.

- **Visualization Tools**
  - Employs Matplotlib for generating plots and diagrams.
  - Visualizes lattice structures before and after error correction.
  - Displays measurement results and qubit state probabilities.
  - Generates circuit diagrams for quantum circuits.

- **Data Management**
  - Enables saving simulation results to JSON files.
  - Allows loading of previous simulation data for review.
  - Logs simulation details for future reference.

## **Functionalities**

- **Parameter Configuration**
  - **Lattice Size (NxN):** User inputs the size of the quantum lattice.
  - **Error Rate:** User specifies the probability of errors occurring.
  - **Error Type:** Options include Bit-flip, Phase-flip, and Depolarizing errors.
  - **Visualization Style:** Choices include Coolwarm, Viridis, and Plasma colormaps.
  - **Error Correction Algorithm:** Options are None, Shor Code, and Steane Code.
  - **Detailed Qubit Information:** Option to display detailed qubit state probabilities.

- **Simulation Execution**
  - Constructs the quantum circuit based on input parameters.
  - Applies Hadamard and CNOT gates to initialize the lattice.
  - Injects errors according to the specified error rate and type.
  - Applies selected error correction algorithms.
  - Measures stabilizers before and after error correction.
  - Runs the simulation and collects results.

- **Visualization Options**
  - **Lattice Before Error Correction:** Displays the initial state of the lattice.
  - **Measurement Results:** Shows the outcomes of quantum measurements.
  - **Lattice After Error Correction:** Displays the state of the lattice post-correction.
  - **Qubit State Probabilities:** Visualizes the probabilities of qubit states.
  - **Circuit Diagram:** Generates a diagram of the quantum circuit used.

- **Data Operations**
  - **Run Simulation:** Executes the simulation with current parameters.
  - **Save Simulation Results:** Saves the current simulation data to a JSON file.
  - **Load Previous Simulation:** Loads simulation data from a JSON file.
  - **Display Visualizations:** Shows generated plots and diagrams within the GUI.
  - **Pop Out Visualizations:** Allows visualizations to be viewed in separate windows.

## **User Workflow**

1. **Configure Parameters:**
   - Input lattice size, error rate, and select error type.
   - Choose visualization style and error correction algorithm.
   - Optionally enable detailed qubit state information.
   - Select desired visualizations to display.

2. **Run Simulation:**
   - Click the "Run Simulation" button.
   - The application constructs the quantum circuit, injects errors, applies error correction, and performs measurements.
   - Simulation results are generated and visualizations are displayed based on selections.

3. **Analyze Results:**
   - View visualizations such as lattice states, measurement outcomes, qubit probabilities, and circuit diagrams.
   - Use pop-out buttons to view visualizations in separate windows if needed.

4. **Manage Data:**
   - Save simulation results for future reference.
   - Load previously saved simulations to compare or review past data.

## **Technical Specifications**

- **Programming Language:** Python
- **Libraries and Frameworks:**
  - *Cirq:* For quantum circuit construction and simulation.
  - *PyQt5:* For building the graphical user interface.
  - *Matplotlib:* For creating visualizations.
  - *NumPy:* For numerical operations.
  - *JSON:* For data serialization and storage.

- **Classes and Modules:**
  - `QuantumErrorCorrectionSoftware`: Main application class handling the GUI and user interactions.
  - `CircuitManager`: Manages the construction and modification of quantum circuits.
  - `SimulationManager`: Handles the execution of simulations and processing of results.
  - `VisualizationManager`: Manages the generation and display of visualizations.
  - `FigureWindow`: Handles pop-out windows for visualizations.
  - `LoggingManager`: Manages saving and loading of simulation data.

## **Usage Scenarios**

- **Research:** Simulating different quantum error correction algorithms to study their effectiveness.
- **Education:** Teaching quantum computing concepts through interactive simulations and visualizations.
- **Development:** Designing and testing quantum circuits with integrated error correction mechanisms.
