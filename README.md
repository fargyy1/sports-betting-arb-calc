# Sports Betting Arbitrage Calculator

Find **guaranteed profit** opportunities across different bookmakers — no API keys required.

This tool scans odds data for arbitrage situations (also called "sure bets" or "arbing"). When two or more bookmakers disagree on the probability of an outcome, you can bet on all possible outcomes across those bookmakers and lock in a profit regardless of the result.

## Features

- Scans any number of 2-way and 3-way betting markets
- Detects arbitrage by calculating the total implied probability
- Computes optimal stakes (Dutching) so you get the same payout no matter what
- Shows exact profit margin and profit per $100 wagered
- Works with manual paste or from a JSON file

## Example Output

```
=======================================================
  SPORTS BETTING ARBITRAGE CALCULATOR v1.0
  Find guaranteed profit opportunities
=======================================================

📊 Using sample odds data (5 events)
  Tip: pass a JSON file as argument to use custom odds

🔍 Scanning 5 events for arbitrage...

=======================================================
  RESULTS: 2 arbitrages found
=======================================================

=======================================================
  #1 ⚡ REAL ARB: Lakers vs Celtics (NBA)
=======================================================
  Arb Percentage: 96.4%
  Profit Margin:  3.6% ✅
  Profit per $100: $3.73

  Outcomes:
    Lakers (DraftKings)                 @ 2.10    Stake: $49.40
    Celtics (FanDuel)                   @ 2.05    Stake: $50.60


=======================================================
  #2 ⚡ REAL ARB 3-WAY: Real Madrid vs Barcelona
=======================================================
  Arb Percentage: 98.37%
  Profit Margin:  1.63% ✅
  Profit per $100: $1.67

  Outcomes:
    Real Madrid (Betfair)               @ 2.80    Stake: $36.31
    Draw (Betfair)                      @ 3.55    Stake: $28.64
    Barcelona (Betfair)                 @ 2.90    Stake: $35.06


  💰 Total potential profit per $100: $5.40
```

## Usage

```bash
# Run with sample data
python3 arbitrage_calculator.py

# Run with your own odds (JSON format)
python3 arbitrage_calculator.py my_odds.json
```

### JSON Input Format

```json
{
  "Event Name": {
    "Outcome (Bookmaker)": 2.10,
    "Outcome2 (Bookmaker)": 1.85
  }
}
```

## Want the full version?

👉 [Get the Full Arbitrage Calculator](https://fargyy.gumroad.com/l/arbitrage-calculator)

**Buy for $15** — includes custom odds support, 3-way arb detection, stake calculator, and lifetime updates.