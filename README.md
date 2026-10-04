
# 🚦 Smart Traffic Signal Control System Using Fuzzy Logic

## 📌 Project Overview

The **Smart Traffic Signal Control System** is a Computational Intelligence mini project that uses **Fuzzy Logic** to dynamically determine the appropriate green signal duration based on traffic density and vehicle waiting time.

Unlike traditional fixed-time traffic signals, the proposed system adapts the green signal duration according to changing traffic conditions.

The project also includes a traffic simulation to compare the performance of a **Fuzzy Logic Controller** with a **Fixed-Time Controller**.

---

## 🎯 Objectives

- Dynamically adjust green signal duration.
- Reduce unnecessary vehicle waiting time.
- Handle uncertain and continuously changing traffic conditions.
- Demonstrate the application of Fuzzy Logic in intelligent transportation.
- Simulate different traffic conditions.
- Compare Fuzzy Logic control with a fixed-time traffic signal.
- Provide an interactive web-based dashboard for demonstration.

---

## 🧠 Computational Intelligence Technique

The project uses **Fuzzy Logic**.

Fuzzy Logic allows traffic conditions to be represented using linguistic values instead of only fixed numerical categories.

For example:

- Traffic Density → Low, Medium, High
- Waiting Time → Short, Medium, Long
- Green Signal Duration → Short, Medium, Long

---

## 📥 Inputs

The Fuzzy Logic Controller uses two input variables:

### 1. Traffic Density

Represents the percentage of road traffic.

Fuzzy sets:

- Low
- Medium
- High

### 2. Waiting Time

Represents how long vehicles have been waiting at the signal.

Fuzzy sets:

- Short
- Medium
- Long

---

## 📤 Output

### Green Signal Duration

The controller determines how long the traffic signal should remain green.

Fuzzy sets:

- Short
- Medium
- Long

---

## 📋 Fuzzy Rule Base

The system uses IF-THEN fuzzy rules to determine the appropriate green signal duration.

| Rule | Traffic Density | Waiting Time | Green Signal |
|------|------------------|--------------|--------------|
| R1 | Low | Short | Short |
| R2 | Low | Medium | Short |
| R3 | Low | Long | Medium |
| R4 | Medium | Short | Medium |
| R5 | Medium | Medium | Medium |
| R6 | Medium | Long | Long |
| R7 | High | Short | Long |
| R8 | High | Medium | Long |
| R9 | High | Long | Long |

### Example Rule

```text
IF traffic density is HIGH
AND waiting time is LONG
THEN green signal duration is LONG.
```

---

## 🔄 System Workflow

```text
Traffic Density + Waiting Time
              ↓
        Fuzzification
              ↓
       Fuzzy Rule Evaluation
              ↓
         Fuzzy Inference
              ↓
        Defuzzification
              ↓
    Green Signal Duration
```

---

## 🧪 Traffic Simulation

The project includes a simulated traffic environment to evaluate the performance of the traffic signal controllers.

Two approaches are compared:

### Fixed-Time Controller

Uses a predefined green signal duration.

### Fuzzy Logic Controller

Dynamically calculates the green signal duration based on:

- Traffic density
- Waiting time

### Performance Metrics

The simulation evaluates:

- Average Waiting Time
- Maximum Waiting Time
- Average Queue Length
- Vehicles Served

Simulation results are stored in the `data` folder.

---

## 💻 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| NumPy | Numerical calculations |
| Pandas | Data processing |
| Matplotlib | Data visualization |
| Scikit-Fuzzy | Fuzzy Logic implementation |
| Streamlit | Interactive web application |

---

## 📁 Project Structure

```text
Smart-Traffic-Fuzzy/
│
├── data/
│   ├── simulation_results.csv
│   └── queue_history.csv
│
├── results/
│   ├── traffic_density_membership.png
│   ├── waiting_time_membership.png
│   ├── green_time_membership.png
│   └── simulation graphs
│
├── src/
│   ├── __init__.py
│   ├── fuzzy_controller.py
│   ├── visualization.py
│   └── traffic_simulation.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation and Setup

## 1. Open the Project

Open the project folder in VS Code:

```text
C:\Smart-Traffic-Fuzzy
```

---

## 2. Activate the Virtual Environment

Open the VS Code terminal and run:

```powershell
.\venv\Scripts\Activate.ps1
```

After successful activation, the terminal should look like:

```text
(venv) PS C:\Smart-Traffic-Fuzzy>
```

---

## 3. Install Required Libraries

Run:

```powershell
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## 1. Test the Fuzzy Controller

Run:

```powershell
python -m src.fuzzy_controller
```

This runs the Fuzzy Logic Controller independently and can be used to test sample input values.

---

## 2. Generate Membership Function Graphs

Run:

```powershell
python -m src.visualization
```

This generates the membership function graphs inside the `results` folder.

You do **not** need to run this every time you open the application.

Run it again only if the membership functions or visualization code are changed.

---

## 3. Run the Traffic Simulation

Run:

```powershell
python -m src.traffic_simulation
```

This generates the traffic simulation results and stores the generated data inside the `data` folder.

You do **not** need to run this every time you open the application.

Run it again when you want to generate a new simulation or update the simulation results.

---

# 🚀 Running the Web Application

Once the project has been set up and the required files have been generated, activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Then run:

```powershell
streamlit run app.py
```

Streamlit will provide a local address such as:

```text
http://localhost:8501
```

Open that address in your web browser.

---

# 🔁 Normal Daily Usage

If the project has already been set up, you do **not** need to regenerate all files every time.

Simply run:

```powershell
.\venv\Scripts\Activate.ps1
```

Then:

```powershell
streamlit run app.py
```

The existing data and result files remain in the project folders.

---

# 📊 Web Application Features

The Streamlit application provides:

- Traffic scenario selection
- Custom traffic conditions
- Traffic density input
- Waiting time input
- Recommended green signal duration
- Traffic signal visualization
- Fuzzy membership analysis
- Membership function graphs
- Fuzzy rule table
- Fixed-Time vs Fuzzy comparison
- Traffic simulation results
- System workflow
- Technology stack
- Project information

---

# 📱 Local Mobile Access

The Streamlit application can also be accessed from a mobile phone when the phone and computer are connected to the same Wi-Fi network.

Streamlit may display a Network URL such as:

```text
http://192.168.x.x:8501
```

Open that Network URL on the mobile phone.

The computer must remain:

- Switched on
- Connected to the same network
- Running the Streamlit application

This is useful for local demonstrations.

---

# 🌐 Online Deployment

For permanent access from a phone, another computer, or without having the laptop with you, the application should be deployed online.

The recommended deployment option is **Streamlit Community Cloud**.

After deployment, the application will have a public URL similar to:

```text
https://your-project-name.streamlit.app
```

Anyone with the link can then open the application from a supported web browser.

The laptop does not need to remain switched on for the deployed application.

---

# ⚠️ Project Limitations

The current project is a simulation and prototype.

Limitations include:

- Traffic data is simulated.
- Real-time CCTV cameras are not connected.
- Real traffic signal hardware is not connected.
- Vehicle behavior is simplified.
- Pedestrian traffic is not currently considered.
- Emergency vehicle priority is not currently implemented.
- Weather conditions are not considered.
- Road accidents and road blockages are not considered.

---

# 🚀 Future Scope

The project can be extended with:

- Real-time CCTV vehicle detection
- OpenCV
- YOLO-based vehicle detection
- IoT traffic sensors
- Emergency vehicle priority
- Pedestrian detection
- Accident detection
- Multi-intersection traffic coordination
- Reinforcement Learning
- Real-time traffic APIs
- Hardware-based traffic signal control

---

# 🎓 Academic Significance

This project demonstrates the application of **Computational Intelligence** to a real-world transportation problem.

The system combines:

```text
Fuzzy Logic
     +
Traffic Simulation
     +
Data Analysis
     +
Visualization
     +
Interactive Web Application
```

---

# 👨‍💻 Project Information

**Project Title:** Smart Traffic Signal Control System Using Fuzzy Logic

**Domain:** Computational Intelligence

**Programming Language:** Python

**Fuzzy Logic Library:** Scikit-Fuzzy

**Web Framework:** Streamlit

**Project Type:** Mini Project