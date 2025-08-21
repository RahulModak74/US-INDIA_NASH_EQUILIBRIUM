import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product

class CurrencyGameTheory:
    def __init__(self):
        """
        Initialize the US_INDIA (with BRICS) currency competition game
        
        Players: US, BRICS(India)
        US Strategies: Aggressive Tariffs, Cooperative Trade
        India Strategies: Accelerate De-dollarization, Maintain Status Quo
        """
        
        # Economic parameters (in trillions USD)
        self.us_debt = 37.0  # US national debt
        self.us_exports_to_brics = 0.083  # US exports to India
        self.brics_exports_to_us = 0.125  # India  exports to US
        self.us_defense_market = 0.150  # USD Value of Global defense market dominated by US that India can disrupt (missiles-F16)
        self.dollar_privilege_value = 2.5  # Annual value of dollar dominance in trillion
        self.brics_gdp_share = 0.379  # BRICS share of global GDP by 2028
        
        # Define payoff matrices
        self.setup_payoff_matrices()
    
    def setup_payoff_matrices(self):
        """Define payoff matrices for the currency competition game"""
        
        # US Payoffs (in trillions USD annually)
        # Rows: US strategies (Aggressive Tariffs, Cooperative Trade)
        # Columns: India strategies (Accelerate De-dollarization, Maintain Status Quo)
        
        self.us_payoffs = np.array([
            # India : Accelerate De-dollarization, Maintain Status Quo
            [-3.2, 0.1],    # US: Aggressive Tariffs
            [-0.8, 1.5]     # US: Cooperative Trade
        ])
        
        # India  Payoffs (in trillions USD annually)
        self.brics_payoffs = np.array([
            # India: Accelerate De-dollarization, Maintain Status Quo
            [2.5, -0.125],   # US: Aggressive Tariffs
            [0.8, 0.5]       # US: Cooperative Trade
        ])
        
        # Strategy labels
        self.us_strategies = ['Aggressive Tariffs', 'Cooperative Trade']
        self.brics_strategies = ['Accelerate De-dollarization', 'Maintain Status Quo']
    
    def calculate_detailed_payoffs(self):
        """Calculate detailed breakdown of payoffs for each scenario"""
        
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
        """Find Nash equilibria in the game"""
        
        nash_equilibria = []
        
        for i in range(len(self.us_strategies)):
            for j in range(len(self.brics_strategies)):
                is_nash = True
                
                # Check if US has incentive to deviate
                current_us_payoff = self.us_payoffs[i, j]
                for alt_i in range(len(self.us_strategies)):
                    if alt_i != i and self.us_payoffs[alt_i, j] > current_us_payoff:
                        is_nash = False
                        break
                
                # Check if BRICS has incentive to deviate
                if is_nash:
                    current_brics_payoff = self.brics_payoffs[i, j]
                    for alt_j in range(len(self.brics_strategies)):
                        if alt_j != j and self.brics_payoffs[i, alt_j] > current_brics_payoff:
                            is_nash = False
                            break
                
                if is_nash:
                    nash_equilibria.append((i, j, self.us_payoffs[i, j], self.brics_payoffs[i, j]))
        
        return nash_equilibria
    
    def analyze_dominant_strategies(self):
        """Analyze if any player has dominant strategies"""
        
        analysis = {}
        
        # Check US dominant strategies
        us_dominant = None
        for i in range(len(self.us_strategies)):
            is_dominant = True
            for alt_i in range(len(self.us_strategies)):
                if alt_i != i:
                    # Check if strategy i dominates alt_i
                    dominates = all(self.us_payoffs[i, j] >= self.us_payoffs[alt_i, j] 
                                  for j in range(len(self.brics_strategies)))
                    strictly_dominates = any(self.us_payoffs[i, j] > self.us_payoffs[alt_i, j] 
                                           for j in range(len(self.brics_strategies)))
                    
                    if not (dominates and strictly_dominates):
                        is_dominant = False
                        break
            
            if is_dominant:
                us_dominant = self.us_strategies[i]
                break
        
        # Check BRICS dominant strategies
        brics_dominant = None
        for j in range(len(self.brics_strategies)):
            is_dominant = True
            for alt_j in range(len(self.brics_strategies)):
                if alt_j != j:
                    # Check if strategy j dominates alt_j
                    dominates = all(self.brics_payoffs[i, j] >= self.brics_payoffs[i, alt_j] 
                                  for i in range(len(self.us_strategies)))
                    strictly_dominates = any(self.brics_payoffs[i, j] > self.brics_payoffs[i, alt_j] 
                                           for i in range(len(self.us_strategies)))
                    
                    if not (dominates and strictly_dominates):
                        is_dominant = False
                        break
            
            if is_dominant:
                brics_dominant = self.brics_strategies[j]
                break
        
        analysis['US_dominant_strategy'] = us_dominant
        analysis['BRICS_dominant_strategy'] = brics_dominant
        
        return analysis
    
    def calculate_mixed_strategy_equilibrium(self):
        """Calculate mixed strategy Nash equilibrium if pure strategy doesn't exist"""
        
        # For 2x2 game, mixed strategy equilibrium exists if no pure strategy equilibrium
        # US player's mixed strategy: probability p of playing Aggressive Tariffs
        # BRICS player's mixed strategy: probability q of playing Accelerate De-dollarization
        
        # BRICS must be indifferent between strategies
        # Expected payoff from Accelerate De-dollarization = Expected payoff from Maintain Status Quo
        # p * 2.5 + (1-p) * 0.8 = p * (-0.125) + (1-p) * 0.5
        
        # Solving: 2.5p + 0.8 - 0.8p = -0.125p + 0.5 - 0.5p
        # 1.7p + 0.8 = -0.625p + 0.5
        # 2.325p = -0.3
        # p = -0.3 / 2.325 = -0.129 (invalid, must be positive)
        
        # US must be indifferent between strategies
        # q * (-3.2) + (1-q) * 0.1 = q * (-0.8) + (1-q) * 1.5
        # -3.2q + 0.1 - 0.1q = -0.8q + 1.5 - 1.5q
        # -3.3q + 0.1 = -2.3q + 1.5
        # -q = 1.4
        # q = -1.4 (invalid)
        
        return None  # No mixed strategy equilibrium with these payoffs
    
    def visualize_game_matrix(self):
        """Create visualization of the game matrix"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # US Payoffs
        df_us = pd.DataFrame(self.us_payoffs, 
                            index=self.us_strategies, 
                            columns=self.brics_strategies)
        
        sns.heatmap(df_us, annot=True, fmt='.1f', cmap='RdYlGn', center=0, 
                   ax=ax1, cbar_kws={'label': 'Payoff (Trillions USD)'})
        ax1.set_title('US Payoffs', fontsize=14, fontweight='bold')
        ax1.set_xlabel('BRICS Strategy')
        ax1.set_ylabel('US Strategy')
        
        # BRICS Payoffs
        df_brics = pd.DataFrame(self.brics_payoffs, 
                               index=self.us_strategies, 
                               columns=self.brics_strategies)
        
        sns.heatmap(df_brics, annot=True, fmt='.1f', cmap='RdYlGn', center=0, 
                   ax=ax2, cbar_kws={'label': 'Payoff (Trillions USD)'})
        ax2.set_title('BRICS Payoffs', fontsize=14, fontweight='bold')
        ax2.set_xlabel('BRICS Strategy')
        ax2.set_ylabel('US Strategy')
        
        plt.tight_layout()
        plt.show()
    
    def run_complete_analysis(self):
        """Run complete Nash equilibrium analysis"""
        
        print("=" * 80)
        print("US-BRICS CURRENCY COMPETITION: NASH EQUILIBRIUM ANALYSIS")
        print("=" * 80)
        print()
        
        # Display game setup
        print("GAME SETUP:")
        print("Players: United States vs BRICS Nations")
        print("US Strategies: Aggressive Tariffs vs Cooperative Trade")
        print("BRICS Strategies: Accelerate De-dollarization vs Maintain Status Quo")
        print()
        
        # Display payoff matrices
        print("PAYOFF MATRICES (Annual Trillions USD):")
        print()
        print("US Payoffs:")
        us_df = pd.DataFrame(self.us_payoffs, 
                            index=self.us_strategies, 
                            columns=self.brics_strategies)
        print(us_df)
        print()
        
        print("BRICS Payoffs:")
        brics_df = pd.DataFrame(self.brics_payoffs, 
                               index=self.us_strategies, 
                               columns=self.brics_strategies)
        print(brics_df)
        print()
        
        # Find Nash equilibria
        nash_eq = self.find_nash_equilibria()
        print("NASH EQUILIBRIA:")
        if nash_eq:
            for i, (us_idx, brics_idx, us_payoff, brics_payoff) in enumerate(nash_eq):
                print(f"Equilibrium {i+1}:")
                print(f"  US Strategy: {self.us_strategies[us_idx]}")
                print(f"  BRICS Strategy: {self.brics_strategies[brics_idx]}")
                print(f"  US Payoff: ${us_payoff:.1f} trillion")
                print(f"  BRICS Payoff: ${brics_payoff:.1f} trillion")
                print()
        else:
            print("No pure strategy Nash equilibria found.")
            print()
        
        # Analyze dominant strategies
        dominant_analysis = self.analyze_dominant_strategies()
        print("DOMINANT STRATEGY ANALYSIS:")
        print(f"US Dominant Strategy: {dominant_analysis['US_dominant_strategy'] or 'None'}")
        print(f"BRICS Dominant Strategy: {dominant_analysis['BRICS_dominant_strategy'] or 'None'}")
        print()
        
        # Detailed scenario analysis
        scenarios = self.calculate_detailed_payoffs()
        print("DETAILED SCENARIO BREAKDOWN:")
        print()
        
        for scenario_name, details in scenarios.items():
            print(f"{scenario_name.replace('_', ' ').title()}:")
            
            if 'US_gains' in details:
                print("  US Gains:")
                for item, value in details['US_gains'].items():
                    print(f"    {item.replace('_', ' ')}: ${value:.3f}T")
            
            if 'US_losses' in details:
                print("  US Losses:")
                for item, value in details['US_losses'].items():
                    print(f"    {item.replace('_', ' ')}: ${value:.3f}T")
            
            if 'BRICS_gains' in details:
                print("  BRICS Gains:")
                for item, value in details['BRICS_gains'].items():
                    print(f"    {item.replace('_', ' ')}: ${value:.3f}T")
            
            if 'BRICS_losses' in details:
                print("  BRICS Losses:")
                for item, value in details['BRICS_losses'].items():
                    print(f"    {item.replace('_', ' ')}: ${value:.3f}T")
            print()
        
        # Strategic recommendations
        print("STRATEGIC ANALYSIS:")
        print()
        print("Current Nash Equilibrium suggests that:")
        if nash_eq:
            equilibrium = nash_eq[0]  # Take first equilibrium
            us_idx, brics_idx = equilibrium[0], equilibrium[1]
            
            if us_idx == 1 and brics_idx == 1:  # Cooperative Trade, Maintain Status Quo
                print("✓ OPTIMAL OUTCOME: US should pursue Cooperative Trade")
                print("✓ This maintains dollar dominance worth $2.5T annually")
                print("✓ BRICS benefits from stable trade relationships")
                print("✓ Both players achieve positive payoffs")
            else:
                print("⚠ SUB-OPTIMAL EQUILIBRIUM DETECTED")
                print("  Current path leads to mutual losses")
                print("  US risks losing dollar dominance ($2.5T annually)")
                print("  BRICS accelerates de-dollarization")
        
        print()
        print("POLICY IMPLICATIONS:")
        print("1. Aggressive tariffs trigger BRICS de-dollarization")
        print("2. Cooperative approach preserves US dollar dominance")
        print("3. Current Trump strategy appears to be Nash-dominated")
        print("4. Economic losses from tariff war exceed any trade benefits")
        print()
        
        return nash_eq, dominant_analysis, scenarios

# Run the analysis
if __name__ == "__main__":
    game = CurrencyGameTheory()
    nash_equilibria, dominant_strategies, scenario_details = game.run_complete_analysis()
    
    # Visualize the game
    game.visualize_game_matrix()