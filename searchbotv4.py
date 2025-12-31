import requests
import os
import time
import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Settings
REFRESH_RATE = 30  # seconds
TOP_COINS = ["LOKAUSDT", "MAGICUSDT", "RENUSDT"]

BINANCE_US_URL = "https://api.binance.us/api/v3/ticker/price"
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def fetch_binance_prices():
    """Fetch prices from Binance US"""
    try:
        resp = requests.get(BINANCE_US_URL, timeout=5)
        data = resp.json()
        prices = {}
        for item in data:
            symbol = item["symbol"]
            price = float(item["price"])
            if symbol in TOP_COINS:
                prices[symbol] = price
        return prices
    except Exception:
        return None

def fetch_coingecko_prices():
    """Fallback: Fetch prices from CoinGecko"""
    try:
        coins_map = {
            "LOKAUSDT": "league-of-kingdoms",
            "MAGICUSDT": "magic",
            "RENUSDT": "ren"
        }
        ids = ",".join(coins_map.values())
        resp = requests.get(
            f"{COINGECKO_URL}?ids={ids}&vs_currencies=usd", timeout=5
        )
        data = resp.json()
        return {
            "LOKAUSDT": data["league-of-kingdoms"]["usd"],
            "MAGICUSDT": data["magic"]["usd"],
            "RENUSDT": data["ren"]["usd"]
        }
    except Exception:
        return None

def display_dashboard(prices):
    os.system("cls" if os.name == "nt" else "clear")
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(Fore.CYAN + f"======  Ultimate Sentinel Dashboard v5.9 (Top 3)  ======")
    print(Fore.CYAN + f"Live @ {now}")
    print(Fore.WHITE + "Coin       Price      Osc%    Trend      Arrow   Osc-Bar      Volume-Bar")
    print("-" * 65)
    
    # Example static oscillation % for demo purposes
    osc_map = {
        "LOKAUSDT": 66.60,
        "MAGICUSDT": 27.39,
        "RENUSDT": 17.04
    }

    for coin in TOP_COINS:
        price = prices.get(coin, 0.0)
        osc = osc_map.get(coin, 0.0)
        trend = Fore.GREEN + "Bullish" if osc > 0 else Fore.RED + "Bearish"
        arrow = "→"
        bar = Fore.GREEN + "█" * int(osc // 3)
        print(f"{coin:<10} ${price:<8.4f} {osc:<6.2f} {trend:<10} {arrow:<3} {bar}")
    
    # Pick top oscillation coin for GridBot
    top_coin = max(osc_map, key=osc_map.get)
    top_osc = osc_map[top_coin]
    grid_step = round(top_osc / 13, 2)
    est_profit = round(grid_step, 2)
    
    print()
    print(Fore.RED + "🔥 GridBot of the Day:" + Fore.GREEN + f" {top_coin}")
    print(Fore.WHITE + f"Oscillation: {top_osc:.2f}% | Grids: 13 | Step: {grid_step:.2f}%")
    print(f"Range: {prices[top_coin]*0.67:.4f} → {prices[top_coin]*1.33:.4f}")
    print(Fore.YELLOW + f"💰 Est. Daily Profit Potential: {est_profit:.2f}%")
    print(Fore.CYAN + "=" * 65)

def main():
    while True:
        prices = fetch_binance_prices()
        if not prices:
            prices = fetch_coingecko_prices()
        
        if prices:
            display_dashboard(prices)
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print(Fore.RED + "API error - check connection.")
        
        time.sleep(REFRESH_RATE)

if __name__ == "__main__":
    main()