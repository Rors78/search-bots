# Search Bots - Altcoin Price Monitor Collection

A collection of price monitoring bots for tracking specific altcoins with dual API support.

## Versions

### SearchBot v2 (`searchbotv2.py`)
Original version with basic price tracking.

### SearchBot v3 (`searchbotv3.py`)
Enhanced with improved error handling.

### SearchBot v4 (`searchbotv4.py`) - Latest
Most refined version with colorama terminal output.

## Features

- **Dual API Support**: Binance US primary, CoinGecko fallback
- **Specific Coin Tracking**: Monitors LOKA, MAGIC, and REN
- **Color-Coded Output**: Terminal colors for easy reading
- **Auto-Refresh**: Configurable refresh rate
- **Resilient**: Graceful error handling

## Tracked Coins

- **LOKAUSDT** - League of Kingdoms
- **MAGICUSDT** - Magic
- **RENUSDT** - Ren

## Installation

**Windows:**
```powershell
pip install requests colorama
```

**Linux/macOS:**
```bash
pip3 install requests colorama
```

## Usage

### Latest Version (v4)
**Windows:**
```powershell
python searchbotv4.py
```

**Linux/macOS:**
```bash
python3 searchbotv4.py
```

### Configuration

Edit the top of the file:
```python
REFRESH_RATE = 30  # seconds
TOP_COINS = ["LOKAUSDT", "MAGICUSDT", "RENUSDT"]  # Add more coins
```

## API Sources

1. **Binance US** (Primary)
2. **CoinGecko** (Fallback if Binance fails)

## Version Comparison

| Feature | v2 | v3 | v4 |
|---------|----|----|---- |
| Basic tracking | ✅ | ✅ | ✅ |
| Error handling | Basic | Better | Best |
| Color output | ❌ | ❌ | ✅ |
| API fallback | ✅ | ✅ | ✅ |

## Customization

Add more coins by editing `TOP_COINS` and the CoinGecko mapping:

```python
TOP_COINS = ["LOKAUSDT", "MAGICUSDT", "RENUSDT", "BTCUSDT"]

coins_map = {
    "LOKAUSDT": "league-of-kingdoms",
    "MAGICUSDT": "magic",
    "RENUSDT": "ren",
    "BTCUSDT": "bitcoin"
}
```

## License

Provided as-is for personal use.
