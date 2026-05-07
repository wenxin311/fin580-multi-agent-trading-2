import numpy as np

def generate_fake_prices(n):
    prices = [100]
    for _ in range(n - 1):
        change = np.random.normal(0, 0.01)
        prices.append(prices[-1] * (1 + change))
    return prices