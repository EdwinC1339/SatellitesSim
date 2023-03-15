import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import *
import random as r


def bernoulli(p):
    return r.random() < p


def geometric(p):
    failures = 0

    while not bernoulli(p):
        failures += 1

    return failures


def main():
    n = 10000
    p = [0.00045, 0.0005, 0.00055]

    df = pd.DataFrame(columns=p)
    for prob in p:
        with ProcessPoolExecutor() as executor:
            futures = []

            for _ in range(n):
                future = executor.submit(geometric, prob)
                futures.append(future)

            executor.shutdown()
            results = pd.Series(map(lambda x: x.result(), futures))
            df[prob] = results

    print(df)

    fig1, ax1 = plt.subplots()
    ax1 = df.plot.hist(bins=40, alpha=0.2, ax=ax1)
    ax1.set_xlabel("Orbits before battery failure")
    ax1.legend().set_title("Probability of battery failure")
    ax1.set_title("Satellite lifetime histogram")

    fig2, ax2 = plt.subplots()
    ax2 = df.boxplot(ax=ax2, grid=False)
    ax2.set_ylabel("Orbits before battery failure")
    ax2.set_xlabel("Probability of battery failure")
    ax2.set_title("Satellite lifetime boxplot")

    plt.show()


if __name__ == '__main__':
    main()

