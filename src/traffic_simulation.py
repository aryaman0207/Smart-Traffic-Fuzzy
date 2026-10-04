import os
from collections import deque

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.fuzzy_controller import calculate_green_time


# ==========================================
# SIMULATION SETTINGS
# ==========================================

SIMULATION_TIME = 1800       # 30 minutes
FIXED_GREEN_TIME = 60        # seconds
SERVICE_RATE = 0.5           # vehicles served per second

APPROACHES = [
    "North",
    "East",
    "South",
    "West"
]

# Average vehicle arrival rate per second
ARRIVAL_RATES = {
    "North": 0.12,
    "East": 0.22,
    "South": 0.35,
    "West": 0.18
}


# ==========================================
# FUZZY INPUT CALCULATION
# ==========================================

def calculate_density(queue_length):
    """
    Convert queue length to traffic density percentage.

    40 vehicles or more is treated as 100% density.
    """

    density = (queue_length / 40) * 100

    return min(100, density)


def calculate_waiting_time(queue, current_time):
    """
    Calculate the waiting time of the oldest vehicle.
    """

    if not queue:
        return 0

    oldest_vehicle = queue[0]

    waiting = current_time - oldest_vehicle

    return min(120, waiting)


# ==========================================
# TRAFFIC SIMULATION
# ==========================================

def simulate(controller_type, duration=SIMULATION_TIME, seed=42):

    np.random.seed(seed)

    queues = {
        approach: deque()
        for approach in APPROACHES
    }

    current_phase = 0
    phase_remaining = 0
    service_budget = 0

    served_waiting_times = []

    queue_history = []

    total_arrivals = 0
    total_served = 0

    for current_time in range(duration):

        # --------------------------------------
        # Generate new vehicles
        # --------------------------------------

        for approach in APPROACHES:

            arrivals = np.random.poisson(
                ARRIVAL_RATES[approach]
            )

            total_arrivals += arrivals

            for _ in range(arrivals):
                queues[approach].append(current_time)

        # --------------------------------------
        # Start a new signal phase
        # --------------------------------------

        if phase_remaining <= 0:

            current_approach = APPROACHES[current_phase]

            queue = queues[current_approach]

            density = calculate_density(
                len(queue)
            )

            waiting = calculate_waiting_time(
                queue,
                current_time
            )

            if controller_type == "fuzzy":

                phase_duration = int(
                    round(
                        calculate_green_time(
                            density,
                            waiting
                        )
                    )
                )

            else:

                phase_duration = FIXED_GREEN_TIME

            phase_remaining = phase_duration

            service_budget = 0

        # --------------------------------------
        # Serve vehicles
        # --------------------------------------

        current_approach = APPROACHES[current_phase]

        queue = queues[current_approach]

        service_budget += SERVICE_RATE

        while service_budget >= 1 and queue:

            arrival_time = queue.popleft()

            waiting = current_time - arrival_time

            served_waiting_times.append(waiting)

            total_served += 1

            service_budget -= 1

        # --------------------------------------
        # Record queue length
        # --------------------------------------

        total_queue = sum(
            len(queue)
            for queue in queues.values()
        )

        queue_history.append({
            "time": current_time,
            "controller": controller_type,
            "queue_length": total_queue
        })

        # --------------------------------------
        # Decrease green time
        # --------------------------------------

        phase_remaining -= 1

        # --------------------------------------
        # Change signal
        # --------------------------------------

        if phase_remaining <= 0:

            current_phase = (
                current_phase + 1
            ) % len(APPROACHES)

    # ==========================================
    # CALCULATE FINAL METRICS
    # ==========================================

    if served_waiting_times:

        average_waiting = np.mean(
            served_waiting_times
        )

        maximum_waiting = np.max(
            served_waiting_times
        )

    else:

        average_waiting = 0
        maximum_waiting = 0

    average_queue = np.mean([
        item["queue_length"]
        for item in queue_history
    ])

    metrics = {
        "Controller": controller_type,
        "Total Arrivals": total_arrivals,
        "Vehicles Served": total_served,
        "Average Waiting Time (sec)": round(
            average_waiting,
            2
        ),
        "Maximum Waiting Time (sec)": round(
            maximum_waiting,
            2
        ),
        "Average Queue Length": round(
            average_queue,
            2
        )
    }

    return metrics, queue_history


# ==========================================
# RUN COMPARISON
# ==========================================

if __name__ == "__main__":

    os.makedirs("results", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    print("\nRunning fixed-time simulation...")

    fixed_metrics, fixed_history = simulate(
        "fixed"
    )

    print("Running fuzzy-logic simulation...")

    fuzzy_metrics, fuzzy_history = simulate(
        "fuzzy"
    )

    # --------------------------------------
    # Create comparison table
    # --------------------------------------

    comparison = pd.DataFrame([
        fixed_metrics,
        fuzzy_metrics
    ])

    print("\n==========================================")
    print("TRAFFIC SIGNAL PERFORMANCE COMPARISON")
    print("==========================================")

    print(
        comparison.to_string(index=False)
    )

    comparison.to_csv(
        "data/simulation_results.csv",
        index=False
    )

    # --------------------------------------
    # Queue history
    # --------------------------------------

    history = pd.DataFrame(
        fixed_history + fuzzy_history
    )

    history.to_csv(
        "data/queue_history.csv",
        index=False
    )

    # --------------------------------------
    # Create comparison chart
    # --------------------------------------

    metrics_to_plot = [
        "Average Waiting Time (sec)",
        "Maximum Waiting Time (sec)",
        "Average Queue Length"
    ]

    for metric in metrics_to_plot:

        plt.figure(figsize=(8, 5))

        plt.bar(
            comparison["Controller"],
            comparison[metric]
        )

        plt.title(
            f"Comparison of {metric}"
        )

        plt.xlabel("Controller")
        plt.ylabel(metric)

        plt.tight_layout()

        filename = (
            metric
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )

        plt.savefig(
            f"results/{filename}.png",
            dpi=300
        )

        plt.close()

    # --------------------------------------
    # Queue history graph
    # --------------------------------------

    plt.figure(figsize=(11, 5))

    fixed_data = history[
        history["controller"] == "fixed"
    ]

    fuzzy_data = history[
        history["controller"] == "fuzzy"
    ]

    plt.plot(
        fixed_data["time"],
        fixed_data["queue_length"],
        label="Fixed-Time"
    )

    plt.plot(
        fuzzy_data["time"],
        fuzzy_data["queue_length"],
        label="Fuzzy Logic"
    )

    plt.title(
        "Traffic Queue Length Over Time"
    )

    plt.xlabel("Time (seconds)")
    plt.ylabel("Total Queue Length")

    plt.legend()

    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        "results/queue_comparison.png",
        dpi=300
    )

    plt.close()

    print("\nSimulation completed successfully.")

    print(
        "\nResults saved in:"
    )

    print(
        "data/simulation_results.csv"
    )

    print(
        "data/queue_history.csv"
    )

    print(
        "results/"
    )