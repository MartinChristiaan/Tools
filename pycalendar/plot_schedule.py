def plot_schedule(events):
    import matplotlib.pyplot as plt
    import numpy as np

    plt.style.use("seaborn")

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(events))
    width = [event.duration / 60 for event in events]
    left = [event.start_time.minute / 60 + event.start_time.hour for event in events]
    ax.barh(
        x,
        np.array(width),
        left=left,
    )

    # Add text annotations
    for i, event in enumerate(events):
        ax.text(
            left[i] + width[i] / 2,
            x[i],
            event.title,
            ha="center",
            va="center",
            color="white",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title("Schedule")
    ax.set_xlabel("Hour")
    fig.autofmt_xdate()
    plt.show()
