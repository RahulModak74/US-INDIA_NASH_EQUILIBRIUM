import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class CurrencyGameTheory:
    def __init__(self):
        """
        US-BRICS Currency Competition Game
        Players: US, BRICS (India)
        Strategies:
            US: Aggressive Tariffs, Cooperative Trade
            India: Accelerate De-dollarization, Maintain Status Quo
        Payoffs based on provided economic estimates.
        """
        
        # Economic parameters (in trillions USD)
        self.us_debt = 37.0
        self.us_exports_to_brics = 0.083
        self.brics_exports_to_us = 0.125
        self.us_defense_market = 0.150
        self.dollar_privilege_value = 2.5
        self.brics_gdp_share = 0.379
        
        # Define payoff matrices
        self.setup_payoff_matrices()
    
    def setup_payoff_matrices(self):
        """Define payoff matrices as per input data"""
        # US Payoffs: [Aggressive Tariffs; Cooperative Trade] x [Accel, Maintain]
        self.us_payoffs = np.array([
            [-3.2, 0.1],   # Aggressive Tariffs
            [-0.8, 1.5]    # Cooperative Trade
        ])
        
        # BRICS (India) Payoffs
        self.brics_payoffs = np.array([
            [2.5, -0.125],  # Against Aggressive Tariffs
            [0.8, 0.5]      # Against Cooperative Trade
        ])
        
        self.us_strategies = ['Aggressive Tariffs', 'Cooperative Trade']
        self.brics_strategies = ['Accelerate De-dollarization', 'Maintain Status Quo']
    
    def calculate_detailed_payoffs(self):
        """Return detailed economic components of key scenarios"""
        scenarios = {
            'US_Aggressive_BRICS_Accelerate': {
                'US_losses': {
                    'Lost_dollar_dominance': -2.5,
                    'Lost_defense_market': -0.15,
                    'Higher_debt_costs': -0.8,
                    'Lost_exports': -0.083,
                    'Tariff_retaliation': -0.2
                },
                'US_gains': {
                    'Reduced_BRICS_imports': 0.125,
                    'Short_term_revenue': 0.03
                },
                'BRICS_gains': {
                    'New_currency_benefits': 1.8,
                    'Defense_market_share': 0.15,
                    'Reduced_US_dependency': 0.5,
                    'Export_diversification': 0.3
                },
                'BRICS_losses': {
                    'Transition_costs': -0.25
                }
            },
            'US_Cooperative_BRICS_Maintain': {
                'US_gains': {
                    'Maintain_dollar_dominance': 2.5,
                    'Stable_exports': 0.083,
                    'Defense_market_preserved': 0.15,
                    'BRICS_partnership': 0.2
                },
                'US_losses': {
                    'Trade_deficit_accepted': -0.042
                },
                'BRICS_gains': {
                    'Stable_trade': 0.5,
                    'US_market_access': 0.125,
                    'Technology_transfer': 0.1
                },
                'BRICS_losses': {
                    'Dollar_dependency': -0.125,
                    'Limited_sovereignty': -0.1
                }
            }
        }
        return scenarios

    def find_nash_equilibria(self):
        """Find all pure-strategy Nash equilibria"""
        nash_eq = []
        for i in range(2):
            for j in range(2):
                us_payoff = self.us_payoffs[i, j]
                brics_payoff = self.brics_payoffs[i, j]
                
                # Check if US can improve by deviating
                us_best = all(self.us_payoffs[alt_i, j] <= us_payoff for alt_i in range(2))
                
                # Check if BRICS can improve by deviating
                brics_best = all(self.brics_payoffs[i, alt_j] <= brics_payoff for alt_j in range(2))
                
                if us_best and brics_best:
                    nash_eq.append((i, j, us_payoff, brics_payoff))
        return nash_eq

    def analyze_dominant_strategies(self):
        """Check for strictly dominant strategies"""
        us_dom = None
        for i in range(2):
            dominates = True
            for j in range(2):
                if not all(self.us_payoffs[i, j] >= self.us_payoffs[k, j] for k in range(2) if k != i):
                    dominates = False
                    break
                if not any(self.us_payoffs[i, j] > self.us_payoffs[k, j] for k in range(2) if k != i):
                    dominates = False
                    break
            if dominates:
                us_dom = self.us_strategies[i]
                break

        brics_dom = None
        for j in range(2):
            dominates = True
            for i in range(2):
                if not all(self.brics_payoffs[i, j] >= self.brics_payoffs[i, k] for k in range(2) if k != j):
                    dominates = False
                    break
                if not any(self.brics_payoffs[i, j] > self.brics_payoffs[i, k] for k in range(2) if k != j):
                    dominates = False
                    break
            if dominates:
                brics_dom = self.brics_strategies[j]
                break

        return {'US_dominant_strategy': us_dom, 'BRICS_dominant_strategy': brics_dom}

    def calculate_mixed_strategy_equilibrium(self):
        """Solve for mixed strategy equilibrium if exists"""
        # Let p = Pr(US plays Aggressive Tariffs)
        # Let q = Pr(India plays Accelerate De-dollarization)

        # BRICS indifference: EU_BRICS(Accel) = EU_BRICS(Maintain)
        # q: not needed, solve for p
        # p * 2.5 + (1-p)*0.8 = p*(-0.125) + (1-p)*0.5
        # => p*(2.5 - 0.8 + 0.125 - 0.5) = 0.5 - 0.8
        # => p*(1.325) = -0.3 → p = -0.3 / 1.325 ≈ -0.226 → invalid

        # US indifference: EU_US(Agg) = EU_US(Coop)
        # q*(-3.2) + (1-q)*0.1 = q*(-0.8) + (1-q)*1.5
        # => q*(-3.2 + 0.8 + 0.1 - 1.5) = 1.5 - 0.1
        # => q*(-3.8) = 1.4 → q = -1.4 / 3.8 ≈ -0.368 → invalid

        return None  # No valid mixed strategy equilibrium

    def visualize_game_matrix(self):
        """Plot payoff matrices"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        df_us = pd.DataFrame(self.us_payoffs, 
                            index=self.us_strategies, 
                            columns=self.brics_strategies)
        sns.heatmap(df_us, annot=True, fmt='.1f', cmap='RdYlGn', center=0, ax=ax1, cbar_kws={'label': 'Payoff (Trillion USD)'})
        ax1.set_title('US Payoffs', fontweight='bold')
        ax1.set_xlabel('BRICS Strategy')
        ax1.set_ylabel('US Strategy')

        df_brics = pd.DataFrame(self.brics_payoffs, 
                               index=self.us_strategies, 
                               columns=self.brics_strategies)
        sns.heatmap(df_brics, annot=True, fmt='.1f', cmap='RdYlGn', center=0, ax=ax2, cbar_kws={'label': 'Payoff (Trillion USD)'})
        ax2.set_title('BRICS (India) Payoffs', fontweight='bold')
        ax2.set_xlabel('BRICS Strategy')
        ax2.set_ylabel('US Strategy')

        plt.tight_layout()
        plt.show()

    def run_complete_analysis(self):
        """Run full analysis with no normative commentary"""
        print("=" * 80)
        print("US-BRICS CURRENCY COMPETITION: PURE STRATEGY GAME ANALYSIS")
        print("=" * 80)
        print()

        print("GAME STRUCTURE:")
        print("Players: United States, BRICS (India)")
        print("US Strategies: Aggressive Tariffs, Cooperative Trade")
        print("India Strategies: Accelerate De-dollarization, Maintain Status Quo")
        print()

        print("PAYOFF MATRICES (Annual, Trillions USD):")
        us_df = pd.DataFrame(self.us_payoffs,
                            index=self.us_strategies,
                            columns=self.brics_strategies)
        print("US Payoffs:")
        print(us_df)
        print()

        brics_df = pd.DataFrame(self.brics_payoffs,
                               index=self.us_strategies,
                               columns=self.brics_strategies)
        print("BRICS (India) Payoffs:")
        print(brics_df)
        print()

        # Find Nash equilibria
        nash_eq = self.find_nash_equilibria()
        print("PURE STRATEGY NASH EQUILIBRIA:")
        if nash_eq:
            for idx, (i, j, u, b) in enumerate(nash_eq):
                print(f"Equilibrium {idx+1}:")
                print(f"  US: {self.us_strategies[i]} → Payoff: {u:.1f}T")
                print(f"  India: {self.brics_strategies[j]} → Payoff: {b:.1f}T")
        else:
            print("None found.")
        print()

        # Dominant strategies
        dom = self.analyze_dominant_strategies()
        print("DOMINANT STRATEGIES:")
        print(f"US: {dom['US_dominant_strategy'] or 'None'}")
        print(f"India: {dom['BRICS_dominant_strategy'] or 'None'}")
        print()

        # Detailed scenarios
        scenarios = self.calculate_detailed_payoffs()
        print("DETAILED SCENARIO PAYOFF COMPONENTS:")
        for name, data in scenarios.items():
            title = name.replace('_', ' ').title()
            print(f"{title}:")
            if 'US_gains' in data:
                print("  US Gains:")
                for k, v in data['US_gains'].items():
                    print(f"    {k.replace('_', ' ').title()}: {v:.3f}T")
            if 'US_losses' in data:
                print("  US Losses:")
                for k, v in data['US_losses'].items():
                    print(f"    {k.replace('_', ' ').title()}: {v:.3f}T")
            if 'BRICS_gains' in data:
                print("  India Gains:")
                for k, v in data['BRICS_gains'].items():
                    print(f"    {k.replace('_', ' ').title()}: {v:.3f}T")
            if 'BRICS_losses' in data:
                print("  India Losses:")
                for k, v in data['BRICS_losses'].items():
                    print(f"    {k.replace('_', ' ').title()}: {v:.3f}T")
            print()

        # Mathematical analysis only
        print("MATHEMATICAL ANALYSIS:")
        print()
        if nash_eq:
            eq = nash_eq[0]
            us_strat = self.us_strategies[eq[0]]
            brics_strat = self.brics_strategies[eq[1]]
            us_payoff = eq[2]
            brics_payoff = eq[3]

            print(f"Unique Pure-Strategy Nash Equilibrium: ({us_strat}, {brics_strat})")
            print(f"  → US receives {us_payoff:.1f}T, India receives {brics_payoff:.1f}T")
            print()
            print("Rationality Check:")
            print("  - Given India plays 'Accelerate De-dollarization', US best response is 'Cooperative Trade'")
            print("    because -0.8 > -3.2")
            print("  - Given US plays 'Cooperative Trade', India best response is 'Accelerate De-dollarization'")
            print("    because 0.8 > 0.5")
            print()
            print("Conclusion:")
            print("  The game has a unique Nash equilibrium in pure strategies.")
            print("  This equilibrium yields suboptimal payoff for the US")
            print("  relative to (Cooperative Trade, Maintain Status Quo),")
            print("  but that outcome is not stable — India has incentive to deviate.")
            print()
            print("Mixed Strategy Check:")
            print("  Solving for US indifference: q*(-3.2) + (1-q)*0.1 = q*(-0.8) + (1-q)*1.5")
            print("  → -3.2q + 0.1 - 0.1q = -0.8q + 1.5 - 1.5q")
            print("  → -3.3q + 0.1 = -2.3q + 1.5")
            print("  → -1.0q = 1.4 → q = -1.4 → invalid probability")
            print("  → No valid mixed-strategy equilibrium exists.")
        else:
            print("No pure-strategy Nash equilibrium exists in this game.")
            print("Players lack stable best-response cycles under simultaneous play.")

        return nash_eq, dom, scenarios


# Run analysis
if __name__ == "__main__":
    game = CurrencyGameTheory()
    nash_equilibria, dominant_strategies, scenario_details = game.run_complete_analysis()
    game.visualize_game_matrix()