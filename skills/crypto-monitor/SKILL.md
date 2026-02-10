---
name: crypto-monitor
description: Crypto portfolio monitoring and market analysis - checks prices daily, alerts on target hits, summarizes market sentiment. Use for portfolio tracking and market awareness.
---

# Crypto Monitor

**Mission:** Keep Kevin informed about crypto markets and portfolio performance.

## Daily Routine (18:00 PST)

### 1. Price Check
Check current prices for portfolio coins:
- BTC, ETH, SOL, ADA (and any holdings)
- Compare to buy targets
- Compare to sell targets

### 2. Market Sentiment
- Pull Fear & Greed Index
- Check Bitcoin dominance
- Note major market events

### 3. Alert Check
Notify if:
- Price hits buy target (DCA opportunity)
- Price hits sell target (profit taking)
- Price hits stop loss (risk management)
- Fear & Greed < 20 (extreme fear = buying opp)
- Fear & Greed > 80 (extreme greed = caution)

## Alert Format

**Buy Opportunity:**
"🟢 BTC hit your $40K buy target! Current: $39,800. DCA opportunity?"

**Sell Signal:**
"🟡 ETH hit your $3,500 sell target! Current: $3,520. Take 25% profits?"

**Market Extreme:**
"📊 Fear & Greed at 18 (Extreme Fear). Historically good buying opportunity."

## Weekly Report (Sunday)

Summarize:
- Portfolio P/L for week
- Best/worst performers
- Market trends observed
- Opportunities for next week

## Research Tasks

When asked, research:
- Specific coins (tech, team, roadmap)
- Market trends
- News impact analysis
- Compare coins

## Data Management

**Read from:** `projects/lab-repo/personal-dashboard/crypto/portfolio.md`

**Track:**
- Holdings and quantities
- Average buy prices
- Target prices
- Stop loss levels

## Safety Reminders

Always include:
- "Not financial advice"
- "DYOR (Do Your Own Research)"
- Risk warnings for volatile markets
- Reminder to never invest more than can afford to lose

## Command Triggers

User can ask:
- "Check crypto prices" → Current prices + changes
- "Any crypto alerts?" → Check targets
- "Crypto market summary" → Fear & Greed + trends
- "Research [coin]" → Deep dive
