"""
Performance Metrics

Purpose:
Calculate quantitative strategy metrics.
"""

import numpy as np


class PerformanceMetrics:

    @staticmethod
    def sharpe_ratio(returns):

        returns = np.array(returns)

        if returns.std() == 0:
            return 0

        return (
            returns.mean() / returns.std()
        ) * np.sqrt(252)

    @staticmethod
    def max_drawdown(capital_curve):

        peak = capital_curve[0]
        max_dd = 0

        for value in capital_curve:

            if value > peak:
                peak = value

            drawdown = (peak - value) / peak

            if drawdown > max_dd:
                max_dd = drawdown

        return max_dd

    @staticmethod
    def win_rate(returns):

        wins = [r for r in returns if r > 0]

        return len(wins) / len(returns)