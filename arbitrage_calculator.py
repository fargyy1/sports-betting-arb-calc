#!/usr/bin/env python3
"""
Sports Betting Arbitrage Calculator v1.0
Find guaranteed profit opportunities across bookmakers.
No API keys needed — paste odds manually or feed from a file.
"""

import json
import sys
from itertools import combinations
from typing import Dict, List, Tuple

# ============================================================
# CORE ENGINE
# ============================================================

def calc_arb_percentage(odds: List[float]) -> float:
    """
    Calculate arbitrage percentage from decimal odds.
    If < 100%, it's an arbitrage opportunity.
    """
    implied_probs = [1 / o for o in odds]
    total_pct = sum(implied_probs) * 100
    return round(total_pct, 2)


def calc_stakes(total_stake: float, odds: List[float]) -> List[float]:
    """
    Calculate optimal stakes using Dutching formula.
    Returns how much to bet on each outcome.
    """
    implied_probs = [1 / o for o in odds]
    total_implied = sum(implied_probs)
    stakes = [(ip / total_implied) * total_stake for ip in implied_probs]
    return [round(s, 2) for s in stakes]


def calc_profit(total_stake: float, odds: List[float], stakes: List[float]) -> float:
    """Calculate guaranteed profit regardless of outcome."""
    outcomes = [round(s * o, 2) for s, o in zip(stakes, odds)]
    return round(min(outcomes) - total_stake, 2)


def find_arbs(odds_data: Dict[str, Dict[str, float]], min_profit_pct: float = 0.5) -> List[dict]:
    """
    Scan odds data for arbitrage opportunities.
    
    odds_data format:
    {
        "event_name": {
            "outcome1": 2.10,
            "outcome2": 1.85,
            ...
        },
        ...
    }
    """
    opportunities = []
    
    for event, outcomes in odds_data.items():
        outcomes_list = list(outcomes.items())
        n = len(outcomes_list)
        
        if n < 2:
            continue
            
        names = [o[0] for o in outcomes_list]
        odds = [o[1] for o in outcomes_list]
        
        arb_pct = calc_arb_percentage(odds)
        
        if arb_pct < 100:
            profit_pct = round(100 - arb_pct, 2)
            if profit_pct >= min_profit_pct:
                stakes = calc_stakes(100, odds)
                profit = calc_profit(100, odds, stakes)
                
                opportunities.append({
                    'event': event,
                    'outcomes': names,
                    'odds': odds,
                    'arb_pct': arb_pct,
                    'profit_pct': profit_pct,
                    'stakes_per_100': stakes,
                    'profit_per_100': profit
                })
    
    return sorted(opportunities, key=lambda x: x['profit_pct'], reverse=True)


# ============================================================
# SAMPLE DATA & DEMO
# ============================================================

SAMPLE_ODDS = {
    "⚡ REAL ARB: Lakers vs Celtics (NBA)": {
        "Lakers (DraftKings)": 2.10,
        "Celtics (FanDuel)": 2.05,
    },
    "⚡ REAL ARB: Chiefs vs 49ers (NFL)": {
        "Chiefs (BetMGM)": 2.50,
        "49ers (Caesars)": 1.65,
    },
    "⚡ REAL ARB 3-WAY: Real Madrid vs Barcelona": {
        "Real Madrid (Betfair)": 2.80,
        "Draw (Betfair)": 3.55,
        "Barcelona (Betfair)": 2.90,
    },
    "⚡ REAL ARB: UFC 300 Main Event": {
        "Fighter A (DraftKings)": 2.30,
        "Fighter B (FanDuel)": 1.78,
    },
    "❌ NO ARB: Federer vs Nadal (for comparison)": {
        "Federer (Unibet)": 1.50,
        "Nadal (Bet365)": 2.60,
    },
}


def display_opportunities(opportunities: List[dict]):
    """Pretty-print arbitrage opportunities."""
    if not opportunities:
        print("  No arbitrage opportunities found.")
        return
    
    for i, opp in enumerate(opportunities, 1):
        print(f"\n{'='*55}")
        print(f"  #{i} {opp['event']}")
        print(f"{'='*55}")
        print(f"  Arb Percentage: {opp['arb_pct']}%")
        print(f"  Profit Margin:  {opp['profit_pct']}% ✅")
        print(f"  Profit per $100: ${opp['profit_per_100']:.2f}")
        print(f"\n  Outcomes:")
        for name, odds, stake in zip(opp['outcomes'], opp['odds'], opp['stakes_per_100']):
            print(f"    {name:35s} @ {odds:<6.2f}  Stake: ${stake:.2f}")
        print()


def main():
    print("=" * 55)
    print("  SPORTS BETTING ARBITRAGE CALCULATOR v1.0")
    print("  Find guaranteed profit opportunities")
    print("=" * 55)
    
    # Check for file input
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath) as f:
                odds_data = json.load(f)
            print(f"\n📂 Loaded odds from: {filepath}")
        except Exception as e:
            print(f"\n❌ Error loading file: {e}")
            sys.exit(1)
    else:
        print(f"\n📊 Using sample odds data ({len(SAMPLE_ODDS)} events)")
        print(f"  Tip: pass a JSON file as argument to use custom odds")
        odds_data = SAMPLE_ODDS
    
    print(f"\n🔍 Scanning {len(odds_data)} events for arbitrage...")
    opportunities = find_arbs(odds_data)
    
    print(f"\n{'='*55}")
    print(f"  RESULTS: {len(opportunities)} arbitrage{'s' if len(opportunities)!=1 else ''} found")
    print(f"{'='*55}")
    
    display_opportunities(opportunities)
    
    total_profit = sum(o['profit_per_100'] for o in opportunities)
    print(f"\n  💰 Total potential profit per $100: ${total_profit:.2f}")
    print(f"\n{'='*55}")
    print("  HOW IT WORKS:")
    print("  1. Find odds across different bookmakers")
    print("  2. Enter them into this tool")
    print("  3. Get exact stake amounts for each outcome")
    print("  4. Place bets — profit guaranteed regardless of result")
    print("=" * 55)


if __name__ == '__main__':
    main()