import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk


def run_simulation(returns, last_price, n_simulations=10000, n_days=365):
    simulated_prices = np.zeros((n_days, n_simulations))
    simulated_prices[0] = last_price

    for t in range(1, n_days):
        random_shocks = np.random.choice(returns, size=n_simulations, replace=True)
        simulated_prices[t] = simulated_prices[t-1] * (1 + random_shocks)

    return simulated_prices


def create_chart(simulated_prices, percentiles, percentile_values):
    plt.style.use("cyberpunk")
    plt.figure(figsize=(12, 6))

    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#FF4500', '#00FF00']

    for i in range(10000):
        plt.plot(simulated_prices[:, i], alpha=0.3, color=colors[i % len(colors)])

    for percentile, value in zip(percentiles, percentile_values):
        plt.axhline(value, linestyle='dashed', linewidth=2, label=f'{percentile}th Percentile')

    plt.title('Monte Carlo Simulation of BTC Price', fontsize=16)
    plt.xlabel('Days')
    plt.legend(loc='upper left', frameon=True, edgecolor='white')
    plt.ylabel('Price')
    plt.show()


data = pd.read_csv('btc2.csv')
data = data[['Close']]
data['Daily_Return'] = data['Close'].pct_change()
data = data.dropna()
returns = data['Daily_Return'].values


n_simulations = 10000
n_days = 365
last_price = data['Close'].iloc[-1]

simulated_prices = run_simulation(returns, last_price, n_simulations, n_days)

percentiles = [1, 25, 50, 75, 99]
percentile_values = np.percentile(simulated_prices[-1, :], percentiles)


create_chart(simulated_prices, percentiles, percentile_values)


df_points = pd.DataFrame({
    'Day': np.repeat(np.arange(n_days), n_simulations),
    'Simulation': np.tile(np.arange(n_simulations), n_days),
    'Price': simulated_prices.flatten()
})

df_points.to_csv('btc_monte_carlo.csv', index=False)
