# FIN580 Final Project

## Multi-Agent Narrative-to-Portfolio Trading System (Brent Crude Oil)

---

## Overview

This project builds a multi-agent system that transforms news narratives into executable trading strategies for Brent crude oil.

The system models the decision-making process from raw information to portfolio execution using a structured agent pipeline.

---

## System Architecture

News → Event (A1) → Macro (A2) → Signal (A3) → Backtest

* **A1 (Event Detection)**: Extracts structured events from news data
* **A2 (Macro Interpretation)**: Translates events into macroeconomic implications
* **A3 (Signal Agent)**: Generates trading signals (Long / Short / Flat) with conviction and holding horizon

---

## Key Features

* Multi-agent architecture
* Event-driven trading signals
* Conviction-based position sizing
* Transaction cost modeling (30 bps)
* Latency modeling (prevents look-ahead bias)
* Out-of-sample evaluation
* Baseline comparison (random strategy)
* Ablation study (no conviction, no event)

---

## Project Structure

```
agents/        # trading logic and alternative agents
backtest/      # backtesting engine
utils/         # analysis, plotting, synthetic price
data/          # input data and results
main.py        # main pipeline
dashboard.py   # optional visualization
```

---

## How to Run

### Run main pipeline

```
python main.py
```

### Launch dashboard (optional)

```
streamlit run dashboard.py
```

---

## Results Summary

The strategy generates modest positive returns with low drawdown.

* Demonstrates limited but non-zero predictive power
* Outperforms random baseline
* Conviction-based sizing contributes to performance

---

## Limitations

* Uses synthetic price data
* Limited sample size
* Simplified signal logic
* No real market execution

---

## Future Work

* Integrate real market data (EIA / oil prices)
* Improve signal generation using LLM
* Add risk management agent (A4)
* Expand to multi-asset portfolio

---

## Author

FIN580 – Student B (Trading Signal & Backtesting)
