# Quantum Error Correction Simulator

The **Quantum Error Correction Simulator** is a software tool designed to simulate and visualize quantum error correction processes. It integrates various components to allow users to configure, run, and analyze quantum simulations effectively.

## **Functionality**

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

## **Technical Specifications**

- **Programming Language:** Python
- **Libraries and Frameworks:**
  - *Cirq:* For quantum circuit construction and simulation.
  - *PyQt5:* For building the graphical user interface.
  - *Matplotlib:* For creating visualizations.
  - *NumPy:* For numerical operations.
  - *JSON:* For data serialization and storage.

## **Usage Scenarios**

- **Research:** Simulating different quantum error correction algorithms to study their effectiveness.
- **Education:** Teaching quantum computing concepts through interactive simulations and visualizations.
- **Development:** Designing and testing quantum circuits with integrated error correction mechanisms.
