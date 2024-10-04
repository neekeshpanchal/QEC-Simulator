# Quantum Error Correction Simulator

The **Quantum Error Correction Simulator** is a software tool designed to simulate and visualize quantum error correction processes. It integrates various components to allow users to configure, run, and analyze quantum simulations effectively.
![image](https://github.com/user-attachments/assets/9ee62d52-ac5e-40d1-afea-328a0093ee68)

## **Functionality**

- **Parameter Configuration**
  - **Lattice Size (NxN):** User inputs the size of the quantum lattice.
  - **Error Rate:** User specifies the probability of errors occurring.
![image](https://github.com/user-attachments/assets/dc56d827-3d09-4ca6-a7fd-2e053ba11080)

  - **Error Type:** Options include Bit-flip, Phase-flip, and Depolarizing errors.
![image](https://github.com/user-attachments/assets/b16acf09-7e06-4ff8-aad5-019812258af2)

  - **Visualization Style:** Choices include Coolwarm, Viridis, and Plasma colormaps.
  - **Error Correction Algorithm:** Options are None, Shor Code, and Steane Code.
![image](https://github.com/user-attachments/assets/13d43dfc-b3b9-4f28-8d60-242d6d6ad465)


- **Simulation Execution**
  - Constructs the quantum circuit based on input parameters.
  - Applies Hadamard and CNOT gates to initialize the lattice.
  - Injects errors according to the specified error rate and type.
  - Applies selected error correction algorithms.
  - Measures stabilizers before and after error correction.
  - Runs the simulation and collects results.

![3x3](https://github.com/user-attachments/assets/4d290597-dcdb-49f6-8bee-d74ef2995b6d)


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
