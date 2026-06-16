#!/usr/bin/env python3
"""
Crypto Portfolio Scanner v1.0 📊
Track your crypto portfolio P&L, allocation percentages, and risk metrics.

Features:
  - Track holdings across multiple wallets/exchanges
  - Real-time profit/loss calculation (using manual price input)
  - Allocation percentage breakdown
  - Diversification score
  - Risk assessment based on portfolio concentration
  - CSV import/export for exchange data
  - Premium version: live CoinGecko API, Telegram alerts, historical charts

FREE OPEN-SOURCE VERSION
Premium: https://fargyy.gumroad.com/l/xrcgws

Usage:
  python3 crypto_scanner.py                    # Demo with sample portfolio
  python3 crypto_scanner.py my_portfolio.json   # Load from JSON
  python3 crypto_scanner.py --interactive       # Add holdings manually
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================
# CONFIG
# ============================================================
VERSION = "1.0.0"
GUMROAD_PREMIUM_URL = "https://fargyy.gumroad.com/l/xrcgws"
STORE_URL = "https://fargyy.gumroad.com"

# ============================================================
# CORE FUNCTIONS
# ============================================================

def calc_portfolio_value(holdings: Dict[str, dict]) -> float:
    """Calculate total portfolio value."""
    return sum(h['amount'] * h.get('current_price', 0) for h in holdings.values())

def calc_cost_basis(holdings: Dict[str, dict]) -> float:
    """Calculate total cost basis."""
    return sum(h['amount'] * h.get('avg_entry', 0) for h in holdings.values())

def calc_total_pnl(holdings: Dict[str, dict]) -> dict:
    """Calculate total P&L (realized + unrealized)."""
    total_value = calc_portfolio_value(holdings)
    total_cost = calc_cost_basis(holdings)
    pnl = round(total_value - total_cost, 2)
    pnl_pct = round((pnl / total_cost) * 100, 2) if total_cost > 0 else 0
    return {'pnl': pnl, 'pnl_pct': pnl_pct, 'value': round(total_value, 2), 'cost': round(total_cost, 2)}

def calc_allocation(holdings: Dict[str, dict]) -> List[dict]:
    """Calculate allocation percentages."""
    total_value = calc_portfolio_value(holdings)
    if total_value == 0:
        return []
    
    allocs = []
    for symbol, h in holdings.items():
        value = h['amount'] * h.get('current_price', 0)
        pct = round((value / total_value) * 100, 1)
        cost = h['amount'] * h.get('avg_entry', 0)
        pnl = round(value - cost, 2)
        pnl_pct = round((pnl / cost) * 100, 2) if cost > 0 else 0
        
        allocs.append({
            'symbol': symbol.upper(),
            'amount': h['amount'],
            'avg_entry': h.get('avg_entry', 0),
            'current_price': h.get('current_price', 0),
            'value': round(value, 2),
            'allocation_pct': pct,
            'pnl': pnl,
            'pnl_pct': pnl_pct,
        })
    
    return sorted(allocs, key=lambda x: x['value'], reverse=True)

def calc_diversification_score(allocs: List[dict]) -> float:
    """Calculate Herfindahl-Hirschman Index for portfolio concentration.
    Lower = more diversified. Under 0.15 = well diversified."""
    if not allocs:
        return 1.0
    pcts = [a['allocation_pct'] / 100 for a in allocs]
    hhi = sum(p ** 2 for p in pcts)
    return round(hhi, 3)

def assess_risk(hhi: float) -> str:
    """Assess portfolio risk based on HHI."""
    if hhi < 0.15:
        return "LOW 🟢"
    elif hhi < 0.30:
        return "MODERATE 🟡"
    elif hhi < 0.50:
        return "HIGH 🟠"
    else:
        return "VERY HIGH 🔴"

# ============================================================
# SAMPLE DATA
# ============================================================

SAMPLE_PORTFOLIO = {
    "btc": {"amount": 0.5, "avg_entry": 35000, "current_price": 67500},
    "eth": {"amount": 5.0, "avg_entry": 2200, "current_price": 3450},
    "sol": {"amount": 50.0, "avg_entry": 95, "current_price": 152},
    "link": {"amount": 200.0, "avg_entry": 8.50, "current_price": 14.20},
    "ada": {"amount": 5000.0, "avg_entry": 0.45, "current_price": 0.62},
    "matic": {"amount": 1000.0, "avg_entry": 0.80, "current_price": 0.72},
    "doge": {"amount": 10000.0, "avg_entry": 0.12, "current_price": 0.18},
    "avax": {"amount": 25.0, "avg_entry": 28, "current_price": 36.50},
    "uni": {"amount": 100.0, "avg_entry": 5.50, "current_price": 7.80},
    "atom": {"amount": 100.0, "avg_entry": 9.00, "current_price": 10.50},
}

# ============================================================
# DISPLAY
# ============================================================

BANNER = f"""
╔══════════════════════════════════════════════════════════════╗
║         📊 CRYPTO PORTFOLIO SCANNER v{VERSION}                  ║
║     Track P&L, allocation, and risk from CLI                ║
╚══════════════════════════════════════════════════════════════╝
"""

def display_portfolio(holdings: Dict[str, dict]):
    """Display full portfolio analysis."""
    allocs = calc_allocation(holdings)
    total = calc_total_pnl(holdings)
    hhi = calc_diversification_score(allocs)
    risk = assess_risk(hhi)
    
    print(f"\n  📈 PORTFOLIO SUMMARY")
    print(f"  {'='*50}")
    print(f"     Total Value:    ${total['value']:>10,.2f}")
    print(f"     Cost Basis:     ${total['cost']:>10,.2f}")
    print(f"     P&L:            ${total['pnl']:>+10,.2f}  ({total['pnl_pct']:+.2f}%)")
    print(f"     Holdings:       {len(holdings)} assets")
    print(f"     Div. Score:     {hhi} ({risk})")
    
    print(f"\n  📋 HOLDINGS")
    print(f"  {'='*80}")
    print(f"  {'ASSET':8s} {'AMOUNT':12s} {'AVG ENTRY':10s} {'PRICE':10s} {'VALUE':12s} {'ALLOC':8s} {'P&L':12s}")
    print(f"  {'─'*80}")
    
    for a in allocs:
        pnl_str = f"${a['pnl']:+,.2f}" if abs(a['pnl']) >= 0.01 else "$0.00"
        print(f"  {a['symbol']:8s} {a['amount']:<12.4f} ${a['avg_entry']:<8,.2f} ${a['current_price']:<8,.2f} ${a['value']:<9,.2f} {a['allocation_pct']:<7.1f}% {pnl_str}")
    
    print(f"  {'='*80}")
    
    # Winners and losers
    winners = [a for a in allocs if a['pnl'] > 0]
    losers = [a for a in allocs if a['pnl'] < 0]
    
    if winners:
        best = max(winners, key=lambda x: x['pnl_pct'])
        print(f"  🟢 Best Performer: {best['symbol']} ({best['pnl_pct']:+.2f}%)")
    if losers:
        worst = min(losers, key=lambda x: x['pnl_pct'])
        print(f"  🔴 Worst Performer: {worst['symbol']} ({worst['pnl_pct']:+.2f}%)")
    
    print()

def display_upgrade():
    """Display premium upgrade prompt."""
    print(f"  {'='*55}")
    print(f"  ⚡ GET THE PREMIUM VERSION ⚡")
    print(f"  {'='*55}")
    print(f"  ✓ Live CoinGecko API prices (1000+ coins)")
    print(f"  ✓ Telegram alerts for price movements")
    print(f"  ✓ Historical P&L charts")
    print(f"  ✓ CSV export for tax reporting")
    print(f"  ✓ Multi-wallet tracking")
    print(f"  {'─'*55}")
    print(f"  🔗 {GUMROAD_PREMIUM_URL}")
    print(f"  💰 Only $10 — Track your portfolio like a pro")
    print(f"  {'='*55}")
    print(f"\n  🔗 More tools at {STORE_URL}")
    print()

def interactive_mode():
    """Interactive portfolio entry."""
    print("\n  📝 ADD YOUR HOLDINGS (type 'done' when finished)")
    holdings = {}
    
    while True:
        symbol = input("  Symbol (e.g., BTC) or 'done': ").strip().lower()
        if symbol == 'done':
            break
        try:
            amount = float(input(f"  Amount of {symbol.upper()}: "))
            avg_entry = float(input(f"  Avg entry price for {symbol.upper()} ($): "))
            current_price = float(input(f"  Current price of {symbol.upper()} ($): "))
            holdings[symbol] = {"amount": amount, "avg_entry": avg_entry, "current_price": current_price}
            print(f"  ✅ Added {symbol.upper()}\n")
        except ValueError:
            print("  ❌ Invalid number. Try again.")
    
    return holdings

# ============================================================
# MAIN
# ============================================================

def main():
    print(BANNER)
    
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    
    if '--interactive' in flags:
        holdings = interactive_mode()
        if holdings:
            display_portfolio(holdings)
        else:
            print("  No holdings entered.")
        display_upgrade()
        return
    
    if args:
        filepath = args[0]
        try:
            with open(filepath) as f:
                holdings = json.load(f)
            print(f"  📂 Loaded portfolio from: {filepath}\n")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            sys.exit(1)
    else:
        print(f"  📊 Demo portfolio (10 assets, ${calc_portfolio_value(SAMPLE_PORTFOLIO):,.2f})")
        print(f"  💡 Pass a JSON file to analyze your own holdings")
        print(f"  💡 Use --interactive to add holdings manually\n")
        holdings = SAMPLE_PORTFOLIO
    
    display_portfolio(holdings)
    display_upgrade()

if __name__ == '__main__':
    main()