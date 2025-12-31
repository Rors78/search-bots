import time
import random
import os
from datetime import datetime

# Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"

# Cycle Colors (alternating)
CYCLE_COLORS = [CYAN, GREEN, MAGENTA, YELLOW]

def momentum_color(value):
    """Return color and arrow for momentum values."""
    if value > 0.2:
        return f"{GREEN}{BOLD}{value:.2f}% ▲{RESET}"
    elif value < -0.2:
        return f"{RED}{BOLD}{value:.2f}% ▼{RESET}"
    else:
        return f"{WHITE}{value:.2f}% •{RESET}"

def sparkline(pulse_step):
    """Generate a pseudo-live ASCII sparkline."""
    blocks = ["▁","▂","▃","▄","▅","▆","▇","█"]
    # Animate last block to look alive
    line = "".join(random.choice(blocks) for _ in range(6))
    pulsing = "█" if pulse_step % 2 == 0 else "▇"
    return line + pulsing

def whale_flash(text, cycle_step):
    """Make Whale alerts flash for 3 cycles if momentum ≥ 0.2%."""
    return (MAGENTA if cycle_step % 2 == 0 else WHITE) + text + RESET

def generate_gridbot_data():
    """Simulate API feed for 3 GridBots"""
    coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    prices = [113000 + random.uniform(-200, 200),
              3500 + random.uniform(-10, 10),
              165 + random.uniform(-1, 1)]
    momentum = [random.uniform(-0.1, 0.3),
                random.uniform(-0.05, 0.2),
                random.uniform(-0.05, 0.25)]
    data = []
    for i, coin in enumerate(coins):
        price = prices[i]
        mom = momentum[i]
        low = price * (1 - random.uniform(0.001, 0.002))
        high = price * (1 + random.uniform(0.001, 0.002))
        grids = 5
        est_profit = (high - low) / grids
        data.append({
            "coin": coin,
            "price": price,
            "momentum": mom,
            "low": low,
            "high": high,
            "grids": grids,
            "profit": est_profit
        })
    return data

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

cycle = 1
pulse_step = 0

while True:
    clear_terminal()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cycle_color = CYCLE_COLORS[cycle % len(CYCLE_COLORS)]
    
    print(f"{cycle_color}{BOLD} GRID BOT PICKS CYCLE #{cycle} [{now}]{RESET}\n")

    # Simulate leaderboard
    data = generate_gridbot_data()
    sorted_data = sorted(data, key=lambda x: x['momentum'], reverse=True)

    print(f"{BOLD}=== TOP 3 MOMENTUM LEADERBOARD ==={RESET}")
    for i, bot in enumerate(sorted_data[:3]):
        mom_text = momentum_color(bot["momentum"]*100)
        print(f"{i+1}. {bot['coin']:<7} Price: {bot['price']:.2f}  Momentum: {mom_text}")
    print(f"{BOLD}==============================={RESET}\n")

    # GridBot Details
    for idx, bot in enumerate(sorted_data[:3]):
        is_whale = bot["momentum"] >= 0.2
        header_color = MAGENTA if idx == 2 else (CYAN if idx == 0 else YELLOW)
        bot_title = f"{idx+1} ▢ {'Whale' if idx==2 else 'Sniper' if idx==1 else 'Basic'} GridBot: {bot['coin']}"
        if is_whale:
            bot_title = whale_flash(bot_title, cycle)
        print(f"{header_color}{BOLD}{bot_title}{RESET}")
        print(f"  Price: {bot['price']:.2f} | Momentum: {momentum_color(bot['momentum']*100)}")
        print(f"  {YELLOW}— Suggested Grid Settings —{RESET}")
        print(f"   Low   : {bot['low']:.4f}")
        print(f"   High  : {bot['high']:.4f}")
        print(f"   Grids : {bot['grids']}")
        print(f"   Est. Profit/Grid: {GREEN}${bot['profit']:.4f}{RESET}")
        print(f"   Sparkline: {sparkline(pulse_step)}\n")
        print(cycle_color + "─" * 70 + RESET)

    # End of Cycle
    print(f"\n{cycle_color}{BOLD}────── END OF CYCLE ──────{RESET}\n")
    
    cycle += 1
    pulse_step += 1
    time.sleep(3)