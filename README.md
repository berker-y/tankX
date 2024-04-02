# Arbitrage Bot

This project contains a Python script that connects to the Binance WebSocket API to monitor real-time price data across various currency pairs for arbitrage opportunities.

## Features

- Connects to Binance WebSocket API.
- Monitors real-time price data for a predefined list of currency pairs.
- Calculates potential arbitrage opportunities based on current market prices.
- Allows resetting of the highest profit calculation through user input.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- `websocket-client` package
- An understanding of currency trading and arbitrage

### Installation

1. Clone the repository:

git clone https://github.com/berker-y/tankX.git

### Usage

Run the script with Python:

python main.py

When the script is running, it will connect to the Binance WebSocket API and start monitoring the price data for the specified currency pairs. You can interact with the running script through the command line interface to reset `r` the profit calculation also to quit `q`.

### Configuration

You can modify the `required_pairs` list in `main.py` to monitor different currency pairs according to your needs.
