import matplotlib.pyplot as plt

def plot_cumulative_return(df):
    plt.figure()
    plt.plot(df["cumulative_return"])
    plt.xlabel("Time")
    plt.ylabel("Cumulative Return")
    plt.title("Strategy Performance")
    plt.savefig("data/cumulative_return.png")
    plt.show()