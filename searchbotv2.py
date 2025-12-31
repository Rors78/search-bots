import requests
import time
import datetime
import os
from collections import deque

# ========== CONFIG ==========
CYCLE_DELAY = 30  # seconds between cycles
HISTORY_LENGTH = 30  # how many prices to track for ASCII sparklines
GRID_COUNT = 5

COINS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]  # Top 3 monitored coins

# API endpoints
BINANCE_URL = "https://api.binance.us/api/v3/ticker/price"
KRAKEN_URL = "https://api.kraken.com/0/public/Ticker?pair="
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

# Colors
RESET = "\033[0m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
WHITE = "\033[97m"

# Track last price for momentum calculation
last_prices = {coin: None for coin in COINS}
price_history = {coin: deque(maxlen=HISTORY_LENGTH) for coin in COINS}

# Persistent whale banner
current_whale = None

def fetch_price_binance(symbol):
    try:
        r = requests.get(BINANCE_URL, timeout=5)
        data = r.json()
        for item in data:
            if item['symbol'] == symbol:
                return float(item['price'])
    except:
        return None

def fetch_price_kraken(symbol):
    kraken_map = {
        "BTCUSDT": "XBTUSDT",
        "ETHUSDT": "ETHUSDT",
        "SOLUSDT": "SOLUSDT"
    }
    try:
        kraken_symbol = kraken_map.get(symbol, symbol)
        r = requests.get(KRAKEN_URL + kraken_symbol, timeout=5)
        data = r.json()
        key = list(data['result'].keys())[0]
        return float(data['result'][key]['c'][0])
    except:
        return None

def fetch_price_coingecko(symbol):
    cg_map = {
        "BTCUSDT": "bitcoin",
        "ETHUSDT": "ethereum",
        "SOLUSDT": "solana"
    }
    try:
        r = requests.get(COINGECKO_URL + f"?ids={cg_map[symbol]}&vs_currencies=usd", timeout=5)
        return float(r.json()[cg_map[symbol]]['usd'])
    except:
        return None

def get_live_price(symbol):
    for fetcher in [fetch_price_binance, fetch_price_kraken, fetch_price_coingecko]:
        price = fetcher(symbol)
        if price:
            return price
    return None

def generate_grid_settings(price):
    # Example grid: +/-0.2% spread around current price
    spread = price * 0.002
    low = round(price - spread, 4)
    high = round(price + spread, 4)
    return low, high, GRID_COUNT

def momentum_symbol(momentum):
    if momentum > 0:
        return GREEN + "▲" + RESET
    elif momentum < 0:
        return RED + "▼" + RESET
    else:
        return WHITE + "•" + RESET

def generate_sparkline(prices):
    if not prices:
        return ""
    min_p, max_p = min(prices), max(prices)
    span = max_p - min_p if max_p != min_p else 1
    blocks = "▁▂▃▄▅▆▇█"
    return "".join(blocks[int((p - min_p) / span * (len(blocks)-1))] for p in prices)

def print_cycle_header(cycle_num):
    os.system('cls' if os.name == 'nt' else 'clear')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(CYAN + f"\n╔════════════════════════════════════════════╗" + RESET)
    print(CYAN + f"   GRID BOT PICKS CYCLE #{cycle_num} [{now}]   " + RESET)
    print(CYAN + f"╚════════════════════════════════════════════╝\n" + RESET)

    if current_whale:
        print(MAGENTA + f"🐋 WHALE ALERT: {current_whale} is moving fast!" + RESET)
        print(CYAN + "─────────────────────────────────────────────\n" + RESET)

def run_cycle(cycle_num):
    global current_whale

    prices = {}
    momentum = {}

    # Fetch live data and compute momentum
    for coin in COINS:
        price = get_live_price(coin)
        prices[coin] = price
        price_history[coin].append(price)

        if last_prices[coin] is not None:
            mom = (price - last_prices[coin]) / last_prices[coin] * 100
        else:
            mom = 0
        momentum[coin] = mom
        last_prices[coin] = price

    # Sort coins by momentum
    sorted_coins = sorted(COINS, key=lambda c: momentum[c], reverse=True)

    # Assign gridbot types
    gridbots = [
        ("Basic GridBot", BLUE, sorted_coins[0]),
        ("Sniper GridBot", YELLOW, sorted_coins[1]),
        ("Whale GridBot", MAGENTA, sorted_coins[2])
    ]

    # Whale alert logic
    if momentum[sorted_coins[0]] > 0.2:
        current_whale = sorted_coins[0]

    # Print Leaderboard
    print(WHITE + "=== TOP 3 MOMENTUM LEADERBOARD ===" + RESET)
    for i, coin in enumerate(sorted_coins, 1):
        print(f"{i}. {coin}  Price: {prices[coin]:,.2f}  "
              f"Momentum: {momentum[coin]:.2f}% {momentum_symbol(momentum[coin])} "
              f"{generate_sparkline(price_history[coin])}")
    print(WHITE + "==================================\n" + RESET)

    # Print GridBots
    for idx, (bot_type, color, coin) in enumerate(gridbots, 1):
        low, high, grids = generate_grid_settings(prices[coin])
        est_profit = round((high - low) / grids, 4)

        print(color + f"{idx} ▣ {bot_type}: {coin}" + RESET)
        print(f"   Price: {prices[coin]:,.2f} | Momentum: {momentum[coin]:.2f}%")
        print(color + f"   ─ Suggested Grid Settings ─" + RESET)
        print(f"   Low   : {low}")
        print(f"   High  : {high}")
        print(f"   Grids : {grids}")
        print(f"   Est. Profit/Grid: {GREEN}${est_profit}{RESET}\n")
        print(CYAN + "─────────────────────────────────────────────\n" + RESET)

# Main loop
cycle = 1
while True:
    print_cycle_header(cycle)
    run_cycle(cycle)
    print(CYAN + "╔════════════ END OF CYCLE ════════════╗\n" + RESET)
    cycle += 1
    time.sleep(CYCLE_DELAY)