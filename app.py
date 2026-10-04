import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from pathlib import Path

from src.fuzzy_controller import (
    traffic_density,
    waiting_time,
    green_time,
    calculate_green_time
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Traffic Signal Control",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .project-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .project-subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .result-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(128,128,128,0.3);
        margin: 10px 0 20px 0;
    }

    .result-number {
        font-size: 42px;
        font-weight: 700;
    }

    .result-label {
        font-size: 18px;
    }

    .traffic-light {
        width: 100px;
        margin: auto;
        padding: 15px;
        border-radius: 25px;
        border: 3px solid #555;
        text-align: center;
        background-color: #222;
    }

    .light {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin: 10px auto;
        border: 2px solid #555;
    }

    .light-red {
        background-color: #ff4b4b;
    }

    .light-yellow {
        background-color: #ffd43b;
    }

    .light-green {
        background-color: #2ecc71;
    }

    .info-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.3);
        margin-bottom: 10px;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="project-title">🚦 Smart Traffic Signal Control System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="project-subtitle">'
    'Intelligent Traffic Management Using Fuzzy Logic'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚦 Traffic Control")

st.sidebar.markdown(
    "Select a traffic scenario or create your own custom condition."
)


scenario = st.sidebar.radio(
    "Traffic Scenario",
    [
        "Custom",
        "Low Traffic",
        "Moderate Traffic",
        "Heavy Traffic"
    ]
)


# ============================================================
# SCENARIO VALUES
# ============================================================

if scenario == "Low Traffic":

    default_density = 15
    default_waiting = 10

elif scenario == "Moderate Traffic":

    default_density = 50
    default_waiting = 50

elif scenario == "Heavy Traffic":

    default_density = 90
    default_waiting = 100

else:

    default_density = 50
    default_waiting = 30


density = st.sidebar.slider(
    "Traffic Density (%)",
    min_value=0,
    max_value=100,
    value=default_density,
    step=1
)


waiting = st.sidebar.slider(
    "Waiting Time (seconds)",
    min_value=0,
    max_value=120,
    value=default_waiting,
    step=1
)


st.sidebar.divider()

st.sidebar.info(
    """
    **Input Variables**

    • Traffic Density  
    • Waiting Time

    **Output**

    • Green Signal Duration
    """
)


# ============================================================
# FUZZY CALCULATION
# ============================================================

result = calculate_green_time(
    density,
    waiting
)


# ============================================================
# MEMBERSHIP VALUES
# ============================================================

density_memberships = {}

for name, term in traffic_density.terms.items():

    density_memberships[name] = fuzz.interp_membership(
        traffic_density.universe,
        term.mf,
        density
    )


waiting_memberships = {}

for name, term in waiting_time.terms.items():

    waiting_memberships[name] = fuzz.interp_membership(
        waiting_time.universe,
        term.mf,
        waiting
    )


dominant_density = max(
    density_memberships,
    key=density_memberships.get
)


dominant_waiting = max(
    waiting_memberships,
    key=waiting_memberships.get
)


# ============================================================
# GREEN TIME CATEGORY
# ============================================================

if result < 55:

    signal_category = "SHORT GREEN"
    signal_icon = "🟢"

elif result < 85:

    signal_category = "MEDIUM GREEN"
    signal_icon = "🟢"

else:

    signal_category = "LONG GREEN"
    signal_icon = "🟢"


# ============================================================
# INPUT METRICS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Current Traffic Conditions</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Traffic Density",
        f"{density}%"
    )


with col2:

    st.metric(
        "Waiting Time",
        f"{waiting} sec"
    )


with col3:

    st.metric(
        "Recommended Green Time",
        f"{result:.2f} sec"
    )


# ============================================================
# MAIN RESULT + TRAFFIC LIGHT
# ============================================================

st.divider()

left, right = st.columns([2, 1])


with left:

    st.markdown(
        '<div class="section-title">🎯 Fuzzy Controller Recommendation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-box">

        <div class="result-label">
        Recommended Green Signal Duration
        </div>

        <div class="result-number">
        {result:.2f} seconds
        </div>

        <div style="font-size:22px;">
        {signal_icon} {signal_category}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with right:

    st.markdown(
        '<div class="section-title">🚦 Signal Status</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="traffic-light">

        <div class="light light-red"></div>

        <div class="light light-yellow"></div>

        <div class="light light-green"></div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FUZZY ANALYSIS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🧠 Fuzzy Analysis</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    st.markdown("### Traffic Density")

    st.write(
        f"Dominant Level: **{dominant_density.upper()}**"
    )

    for name, value in density_memberships.items():

        st.progress(
            float(value),
            text=f"{name.capitalize()}: {value:.2f}"
        )


with col2:

    st.markdown("### Waiting Time")

    st.write(
        f"Dominant Level: **{dominant_waiting.upper()}**"
    )

    for name, value in waiting_memberships.items():

        st.progress(
            float(value),
            text=f"{name.capitalize()}: {value:.2f}"
        )


# ============================================================
# MEMBERSHIP FUNCTION GRAPHS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📈 Membership Functions</div>',
    unsafe_allow_html=True
)


tab1, tab2, tab3 = st.tabs(
    [
        "Traffic Density",
        "Waiting Time",
        "Green Signal"
    ]
)


def create_membership_plot(variable, title, current_value=None):

    fig, ax = plt.subplots(
        figsize=(9, 4)
    )

    for name, term in variable.terms.items():

        ax.plot(
            variable.universe,
            term.mf,
            linewidth=2,
            label=name.capitalize()
        )

    if current_value is not None:

        ax.axvline(
            current_value,
            linestyle="--",
            linewidth=2,
            label=f"Current = {current_value}"
        )

    ax.set_title(title)

    ax.set_ylabel(
        "Membership Degree"
    )

    ax.set_ylim(
        -0.05,
        1.05
    )

    ax.grid(
        True,
        alpha=0.3
    )

    ax.legend()

    plt.tight_layout()

    return fig


with tab1:

    fig = create_membership_plot(
        traffic_density,
        "Traffic Density Membership Functions",
        density
    )

    st.pyplot(fig)

    plt.close(fig)


with tab2:

    fig = create_membership_plot(
        waiting_time,
        "Waiting Time Membership Functions",
        waiting
    )

    st.pyplot(fig)

    plt.close(fig)


with tab3:

    fig = create_membership_plot(
        green_time,
        "Green Signal Duration Membership Functions"
    )

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# FUZZY RULE BASE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📋 Fuzzy Rule Base</div>',
    unsafe_allow_html=True
)


rules_data = {

    "Rule": [
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
        "R7",
        "R8",
        "R9"
    ],

    "Traffic Density": [
        "Low",
        "Low",
        "Low",
        "Medium",
        "Medium",
        "Medium",
        "High",
        "High",
        "High"
    ],

    "Waiting Time": [
        "Short",
        "Medium",
        "Long",
        "Short",
        "Medium",
        "Long",
        "Short",
        "Medium",
        "Long"
    ],

    "Green Signal": [
        "Short",
        "Short",
        "Medium",
        "Medium",
        "Medium",
        "Long",
        "Long",
        "Long",
        "Long"
    ]
}


rules_df = pd.DataFrame(
    rules_data
)

st.dataframe(
    rules_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SIMULATION RESULTS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Fixed-Time vs Fuzzy Control</div>',
    unsafe_allow_html=True
)


simulation_file = DATA_DIR / "simulation_results.csv"


if simulation_file.exists():

    simulation_df = pd.read_csv(
        simulation_file
    )

    st.dataframe(
        simulation_df,
        use_container_width=True,
        hide_index=True
    )

    metric_columns = [
        "Average Waiting Time (sec)",
        "Maximum Waiting Time (sec)",
        "Average Queue Length"
    ]

    available_metrics = [
        column
        for column in metric_columns
        if column in simulation_df.columns
    ]

    if available_metrics:

        selected_metric = st.selectbox(
            "Select Performance Metric",
            available_metrics
        )

        chart_df = simulation_df[
            ["Controller", selected_metric]
        ].set_index("Controller")

        st.bar_chart(
            chart_df
        )

else:

    st.warning(
        "Simulation results are not available yet. "
        "Run the traffic simulation first."
    )


# ============================================================
# PROJECT METHODOLOGY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">⚙️ How the System Works</div>',
    unsafe_allow_html=True
)


flow_col1, flow_col2, flow_col3, flow_col4, flow_col5 = st.columns(5)


with flow_col1:

    st.info(
        "1️⃣\n\n"
        "**Input**\n\n"
        "Traffic Density\n"
        "Waiting Time"
    )


with flow_col2:

    st.info(
        "2️⃣\n\n"
        "**Fuzzification**\n\n"
        "Convert inputs into fuzzy values"
    )


with flow_col3:

    st.info(
        "3️⃣\n\n"
        "**Rule Evaluation**\n\n"
        "Apply IF-THEN rules"
    )


with flow_col4:

    st.info(
        "4️⃣\n\n"
        "**Inference**\n\n"
        "Combine fuzzy outputs"
    )


with flow_col5:

    st.info(
        "5️⃣\n\n"
        "**Defuzzification**\n\n"
        "Calculate green time"
    )


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">💻 Technology Stack</div>',
    unsafe_allow_html=True
)


tech1, tech2, tech3, tech4, tech5 = st.columns(5)


with tech1:
    st.metric("Language", "Python")


with tech2:
    st.metric("Fuzzy Logic", "Scikit-Fuzzy")


with tech3:
    st.metric("Data", "Pandas")


with tech4:
    st.metric("Visualization", "Matplotlib")


with tech5:
    st.metric("Interface", "Streamlit")


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">ℹ️ About the Project</div>',
    unsafe_allow_html=True
)


st.write(
    """
    The Smart Traffic Signal Control System uses Fuzzy Logic to
    dynamically determine the appropriate green signal duration
    based on traffic density and vehicle waiting time.

    Unlike a traditional fixed-time traffic signal, the proposed
    system adapts its output according to changing traffic
    conditions.

    The project demonstrates the application of Computational
    Intelligence techniques to intelligent transportation systems.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🚦 Smart Traffic Signal Control System Using Fuzzy Logic

    <br>

    Computational Intelligence Mini Project

    <br>

    Developed using Python, Scikit-Fuzzy and Streamlit

    </div>
    """,
    unsafe_allow_html=True
)