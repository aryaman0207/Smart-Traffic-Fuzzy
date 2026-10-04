import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ==========================================
# 1. DEFINE INPUT AND OUTPUT VARIABLES
# ==========================================

# Traffic density: 0 to 100 percent
traffic_density = ctrl.Antecedent(
    np.arange(0, 101, 1),
    'traffic_density'
)

# Waiting time: 0 to 120 seconds
waiting_time = ctrl.Antecedent(
    np.arange(0, 121, 1),
    'waiting_time'
)

# Green signal duration: 20 to 120 seconds
green_time = ctrl.Consequent(
    np.arange(20, 121, 1),
    'green_time'
)


# ==========================================
# 2. DEFINE MEMBERSHIP FUNCTIONS
# ==========================================

# ---------- Traffic Density ----------

traffic_density['low'] = fuzz.trimf(
    traffic_density.universe,
    [0, 0, 40]
)

traffic_density['medium'] = fuzz.trimf(
    traffic_density.universe,
    [20, 50, 80]
)

traffic_density['high'] = fuzz.trimf(
    traffic_density.universe,
    [60, 100, 100]
)


# ---------- Waiting Time ----------

waiting_time['short'] = fuzz.trimf(
    waiting_time.universe,
    [0, 0, 45]
)

waiting_time['medium'] = fuzz.trimf(
    waiting_time.universe,
    [30, 60, 90]
)

waiting_time['long'] = fuzz.trimf(
    waiting_time.universe,
    [75, 120, 120]
)


# ---------- Green Signal Duration ----------

green_time['short'] = fuzz.trimf(
    green_time.universe,
    [20, 20, 55]
)

green_time['medium'] = fuzz.trimf(
    green_time.universe,
    [40, 70, 100]
)

green_time['long'] = fuzz.trimf(
    green_time.universe,
    [85, 120, 120]
)


# ==========================================
# 3. DEFINE FUZZY RULES
# ==========================================

rule1 = ctrl.Rule(
    traffic_density['low'] &
    waiting_time['short'],
    green_time['short']
)

rule2 = ctrl.Rule(
    traffic_density['low'] &
    waiting_time['medium'],
    green_time['short']
)

rule3 = ctrl.Rule(
    traffic_density['low'] &
    waiting_time['long'],
    green_time['medium']
)

rule4 = ctrl.Rule(
    traffic_density['medium'] &
    waiting_time['short'],
    green_time['medium']
)

rule5 = ctrl.Rule(
    traffic_density['medium'] &
    waiting_time['medium'],
    green_time['medium']
)

rule6 = ctrl.Rule(
    traffic_density['medium'] &
    waiting_time['long'],
    green_time['long']
)

rule7 = ctrl.Rule(
    traffic_density['high'] &
    waiting_time['short'],
    green_time['long']
)

rule8 = ctrl.Rule(
    traffic_density['high'] &
    waiting_time['medium'],
    green_time['long']
)

rule9 = ctrl.Rule(
    traffic_density['high'] &
    waiting_time['long'],
    green_time['long']
)


# ==========================================
# 4. CREATE FUZZY CONTROL SYSTEM
# ==========================================

traffic_control_system = ctrl.ControlSystem([
    rule1,
    rule2,
    rule3,
    rule4,
    rule5,
    rule6,
    rule7,
    rule8,
    rule9
])


# ==========================================
# 5. FUNCTION TO CALCULATE GREEN TIME
# ==========================================

def calculate_green_time(density, waiting):
    """
    Calculate recommended green signal duration.

    Parameters:
        density: Traffic density percentage (0-100)
        waiting: Waiting time in seconds (0-120)

    Returns:
        Recommended green signal duration in seconds.
    """

    simulation = ctrl.ControlSystemSimulation(
        traffic_control_system
    )

    simulation.input['traffic_density'] = density
    simulation.input['waiting_time'] = waiting

    simulation.compute()

    return simulation.output['green_time']


# ==========================================
# 6. TEST THE CONTROLLER
# ==========================================

if __name__ == "__main__":

    density = 75
    waiting = 65

    result = calculate_green_time(
        density,
        waiting
    )

    print("=" * 50)
    print("SMART TRAFFIC SIGNAL CONTROL SYSTEM")
    print("=" * 50)

    print(f"Traffic Density : {density}%")
    print(f"Waiting Time    : {waiting} seconds")
    print(f"Green Signal    : {result:.2f} seconds")

    print("=" * 50)