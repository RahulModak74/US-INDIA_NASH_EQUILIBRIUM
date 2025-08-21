================================================================================
US-INDIA CURRENCY COMPETITION: PURE STRATEGY GAME ANALYSIS
================================================================================

GAME STRUCTURE:
Players: United States, BRICS (India)
US Strategies: Aggressive Tariffs, Cooperative Trade
India Strategies: Accelerate De-dollarization, Maintain Status Quo

PAYOFF MATRICES (Annual, Trillions USD):
US Payoffs:
                    Accelerate De-dollarization  Maintain Status Quo
Aggressive Tariffs                         -3.2                  0.1
Cooperative Trade                          -0.8                  1.5

BRICS (India) Payoffs:
                    Accelerate De-dollarization  Maintain Status Quo
Aggressive Tariffs                          2.5               -0.125
Cooperative Trade                           0.8                0.500

PURE STRATEGY NASH EQUILIBRIA:
Equilibrium 1:
  US: Cooperative Trade → Payoff: -0.8T
  India: Accelerate De-dollarization → Payoff: 0.8T

DOMINANT STRATEGIES:
US: Cooperative Trade
India: Accelerate De-dollarization

DETAILED SCENARIO PAYOFF COMPONENTS:
Us Aggressive Brics Accelerate:
  US Gains:
    Reduced Brics Imports: 0.125T
    Short Term Revenue: 0.030T
  US Losses:
    Lost Dollar Dominance: -2.500T
    Lost Defense Market: -0.150T
    Higher Debt Costs: -0.800T
    Lost Exports: -0.083T
    Tariff Retaliation: -0.200T
  India Gains:
    New Currency Benefits: 1.800T
    Defense Market Share: 0.150T
    Reduced Us Dependency: 0.500T
    Export Diversification: 0.300T
  India Losses:
    Transition Costs: -0.250T

Us Cooperative Brics Maintain:
  US Gains:
    Maintain Dollar Dominance: 2.500T
    Stable Exports: 0.083T
    Defense Market Preserved: 0.150T
    Brics Partnership: 0.200T
  US Losses:
    Trade Deficit Accepted: -0.042T
  India Gains:
    Stable Trade: 0.500T
    Us Market Access: 0.125T
    Technology Transfer: 0.100T
  India Losses:
    Dollar Dependency: -0.125T
    Limited Sovereignty: -0.100T

MATHEMATICAL ANALYSIS:

Unique Pure-Strategy Nash Equilibrium: (Cooperative Trade, Accelerate De-dollarization)
  → US receives -0.8T, India receives 0.8T

Rationality Check:
  - Given India plays 'Accelerate De-dollarization', US best response is 'Cooperative Trade'       
    because -0.8 > -3.2
  - Given US plays 'Cooperative Trade', India best response is 'Accelerate De-dollarization'       
    because 0.8 > 0.5

Conclusion:
  The game has a unique Nash equilibrium in pure strategies.
  This equilibrium yields suboptimal payoff for the US
  relative to (Cooperative Trade, Maintain Status Quo),
  but that outcome is not stable — India has incentive to deviate.

Mixed Strategy Check:
  Solving for US indifference: q*(-3.2) + (1-q)*0.1 = q*(-0.8) + (1-q)*1.5
  → -3.2q + 0.1 - 0.1q = -0.8q + 1.5 - 1.5q
  → -3.3q + 0.1 = -2.3q + 1.5
  → -1.0q = 1.4 → q = -1.4 → invalid probability
  → No valid mixed-strategy equilibrium exists.
