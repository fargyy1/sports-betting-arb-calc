# 🏆 Sports Betting, Crypto & News CLI Tool Suite

**Find guaranteed profit across 30+ bookmakers, track your crypto portfolio, and get breaking tech news in your terminal.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Gumroad Store](https://img.shields.io/badge/Store-Gumroad-orange)](https://fargyy.gumroad.com)

---

## 🛠 Tools in This Repo

### 1️⃣ Sports Betting Arbitrage Scanner (`arbitrage_scanner.py`)
Find **risk-free** guaranteed profit by betting on all outcomes across different bookmakers.

### 2️⃣ Crypto Portfolio Scanner (`crypto_scanner.py`)
Track your portfolio P&L, allocation percentages, and risk metrics from the command line.

### 3️⃣ NewsSnapper — News Aggregator (`news_snapper.py`) 🆕
Get breaking tech/news headlines from Hacker News, TechCrunch, and RSS feeds—right in your terminal. No browser needed.

---

Sports betting arbitrage (aka "sure bets" or "arbing") is a **risk-free** betting strategy where you place bets on **all possible outcomes** of an event across different bookmakers. Because bookmakers set slightly different odds, you can lock in a guaranteed profit — **regardless of who wins**.

**Example:** If DraftKings has Lakers at 2.15 (+115) and FanDuel has Celtics at 2.00 (+100), a $100 split correctly gives you **$3.61 guaranteed profit** no matter the result.

---

## ✨ Features

### Free Version (This Repo)
- ✅ **2-way, 3-way & N-way arbitrage detection** — moneyline, 1X2, multi-outcome
- ✅ **Dutching stake calculator** — optimal stake splitting for guaranteed profit
- ✅ **Multiple odds formats** — Decimal, American (+/-), and Fractional
- ✅ **ROI & profit margin calculation** — know exactly what you'll earn
- ✅ **Batch file scanning** — load hundreds of events from JSON
- ✅ **Interactive mode** — enter odds manually at the command line
- ✅ **Profit tracker** — log your bets, track P&L over time
- ✅ **Confidence scoring** — HIGH/MEDIUM/LOW based on profit margin
- ✅ **No API keys needed** — works entirely offline
- ✅ **NewsSnapper** — Aggregates HN, TechCrunch, RSS headlines in your terminal (NEW!)

### Premium Version
[👉 **Get Premium on Gumroad — $15**](https://fargyy.gumroad.com/l/arbitrage-calculator)

- 🔴 **Live odds API integration** — scan 30+ bookmakers in real-time
- 🔴 **Telegram alerts** — get notified the moment an arb appears
- 🔴 **Email/SMS push notifications**
- 🔴 **Portfolio dashboard** — track P&L with visual charts
- 🔴 **Historical arb tracking** — see what worked and what didn't
- 🔴 **50+ bookmaker coverage** (DraftKings, FanDuel, Bet365, BetMGM, Caesars, PointsBet, Unibet, and more)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/fargyy1/sports-betting-arbitrage-scanner.git
cd sports-betting-arbitrage-scanner

# No dependencies needed — pure Python 3
python3 arbitrage_scanner.py
```

---

## 🔧 Usage

### Quick Demo (Sample Data)
```bash
python3 arbitrage_scanner.py
```

### Scan From a JSON File
Create a file with your odds:
```json
{
  "Lakers vs Celtics": {
    "Lakers (DraftKings)": 2.15,
    "Celtics (FanDuel)": 2.00
  },
  "Chiefs vs 49ers": {
    "Chiefs (BetMGM)": 2.50,
    "49ers (Caesars)": 1.72
  }
}
```

Then run:
```bash
python3 arbitrage_scanner.py my_odds.json
```

### Interactive Mode
```bash
python3 arbitrage_scanner.py --interactive
```

### Track Your Bets
```bash
python3 arbitrage_scanner.py --profit-tracker
```

---

## 📊 Sample Output

```
╔══════════════════════════════════════════════════════════════╗
║         🏆 SPORTS BETTING ARBITRAGE SCANNER v2.0.0          ║
║     Find guaranteed profit across 30+ bookmakers            ║
╚══════════════════════════════════════════════════════════════╝

  🔍 Scanning 11 events for arbitrage...
  📊 Found 5 arbitrage opportunities!
  💰 Total potential profit per $100: $8.00

  🟢 #1 🏀 Lakers vs Celtics (NBA)
     Arb %: 96.51% | Profit: 3.49% | ROI: 3.61%
     Profit/100: $3.61 | Confidence: HIGH
       Lakers (DraftKings)  2.15 (+115)  Stake: $48.19
       Celtics (FanDuel)    2.00 (+100)  Stake: $51.81
```

---

## 🧠 Strategy Tips

1. **Start small** — Practice with small stakes until you're comfortable
2. **Multiple accounts** — You need accounts at 3+ bookmakers to find arbs
3. **Act fast** — Arb opportunities disappear within minutes
4. **Track everything** — Use `--profit-tracker` to log your results
5. **Go premium** — The free version requires manual odds entry; Premium auto-scans live odds

---

## ⚖️ Disclaimer

Sports betting arbitrage is legal in most jurisdictions, but some bookmakers may restrict or close accounts of known arbitrage bettors. Always check your local laws and the terms of service of the bookmakers you use. This tool is for educational and informational purposes only.

---

## 📈 Roadmap

- [x] Core arbitrage engine (2-way, 3-way, N-way)
- [x] Odds format converter (Decimal/American/Fractional)
- [x] Crypto portfolio scanner with P&L & allocation
- [x] Profit tracker with P&L
- [x] Interactive mode
- [ ] Live odds scraping from public sources
- [ ] CSV export for tax reporting
- [ ] Web GUI version (coming in Premium)

---

## 🔗 Links

- **Gumroad Store:** [https://fargyy.gumroad.com](https://fargyy.gumroad.com)
- **Arbitrage Calculator (Premium):** [https://fargyy.gumroad.com/l/arbitrage-calculator](https://fargyy.gumroad.com/l/arbitrage-calculator) — $15
- **Crypto Portfolio Tracker (Premium):** [https://fargyy.gumroad.com/l/xrcgws](https://fargyy.gumroad.com/l/xrcgws) — $10
- **NewsSnapper (News Aggregator):** [https://fargyy.gumroad.com/l/zrevxw](https://fargyy.gumroad.com/l/zrevxw) — $7+
- **GitHub Repo:** [https://github.com/fargyy1/sports-betting-arb-calc](https://github.com/fargyy1/sports-betting-arb-calc)
- **All Products:** Options Calculator, Stock Screener, AI Prompts, Markdown Converter, Email Templates & more

---

**⭐ If this tool helps you, star the repo and share it with a friend!**
