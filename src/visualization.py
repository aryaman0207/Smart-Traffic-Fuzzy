import matplotlib.pyplot as plt

from src.fuzzy_controller import (
    traffic_density,
    waiting_time,
    green_time
)


def plot_membership_functions(variable, title, filename):
    """
    Plot and save membership functions for a fuzzy variable.
    """

    fig, ax = plt.subplots(figsize=(9, 5))

    for name, term in variable.terms.items():
        ax.plot(
            variable.universe,
            term.mf,
            linewidth=2,
            label=name.capitalize()
        )

    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Membership Degree")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()

    output_path = f"results/{filename}"

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {output_path}")


if __name__ == "__main__":

    plot_membership_functions(
        traffic_density,
        "Traffic Density Membership Functions",
        "traffic_density_membership.png"
    )

    plot_membership_functions(
        waiting_time,
        "Waiting Time Membership Functions",
        "waiting_time_membership.png"
    )

    plot_membership_functions(
        green_time,
        "Green Signal Duration Membership Functions",
        "green_time_membership.png"
    )

    print("\nAll membership-function graphs created successfully.")