import numpy as np
import pandas as pd

class ExtendedCurrencyGame:
    def __init__(self):
        # Base parameters (in trillions USD)
        self.base_us_payoffs = np.array([
            [-3.2, 0.1],   # Aggressive Tariffs
            [-0.8, 1.5]    # Cooperative Trade
        ])
        self.base_brics_payoffs = np.array([
            [2.5, -0.125], # US Aggressive
            [0.8, 0.5]     # US Cooperative
        ])
        
        self.us_strategies = ['Aggressive Tariffs', 'Cooperative Trade']
        self.india_strategies = ['Accelerate De-dollarization', 'Maintain Status Quo']
        
        # Intervention flags
        self.incentives = False
        self.retaliation = False
        self.fragmentation = False
        self.digital_dollar = False

    def apply_interventions(self):
        """Modify payoffs based on active interventions"""
        us_pay = self.base_us_payoffs.copy()
        brics_pay = self.base_brics_payoffs.copy()

        # 1. Positive Incentives: Increase payoff for Maintain under cooperation
        if self.incentives:
            brics_pay[1, 1] += 0.4  # e.g., tech, defense access → 0.5 → 0.9

        # 2. Credible Retaliation: Reduce payoff for Accelerate under cooperation
        if self.retaliation:
            brics_pay[1, 0] -= 0.3  # 0.8 → 0.5

        # 3. BRICS Fragmentation: Reduce solidarity benefit
        if self.fragmentation:
            brics_pay[0, 0] -= 0.5  # 2.5 → 2.0 (less collective power)
            brics_pay[1, 0] -= 0.3  # 0.8 → 0.5

        # 4. Digital Dollar: Increase transition cost of de-dollarization
        if self.digital_dollar:
            brics_pay[:, 0] -= 0.3  # Both rows: 2.5→2.2, 0.8→0.5

        return us_pay, brics_pay

    def find_nash_equilibria(self, us_pay, brics_pay):
        """Find all pure-strategy Nash equilibria"""
        equilibria = []
        for i in range(2):
            for j in range(2):
                us_val = us_pay[i, j]
                brics_val = brics_pay[i, j]

                # US best response?
                us_br = all(us_pay[k, j] <= us_val for k in range(2))

                # BRICS best response?
                brics_br = all(brics_pay[i, k] <= brics_val for k in range(2))

                if us_br and brics_br:
                    equilibria.append((i, j, us_val, brics_val))
        return equilibria

    def run_scenario(self, incentives=False, retaliation=False, fragmentation=False, digital_dollar=False):
        """Run one scenario with specified interventions"""
        self.incentives = incentives
        self.retaliation = retaliation
        self.fragmentation = fragmentation
        self.digital_dollar = digital_dollar

        us_pay, brics_pay = self.apply_interventions()

        eq = self.find_nash_equilibria(us_pay, brics_pay)

        # Print summary
        print("🎮 STRATEGIC INTERVENTION ANALYSIS")
        print("—" * 60)
        flags = []
        if incentives: flags.append("Positive Incentives")
        if retaliation: flags.append("Credible Retaliation")
        if fragmentation: flags.append("BRICS Fragmentation")
        if digital_dollar: flags.append("Digital Dollar")
        print("Applied: " + (", ".join(flags) if flags else "None (Baseline)"))

        print("\n🔢 PAYOFF MATRICES:")
        df_us = pd.DataFrame(us_pay,
                            index=self.us_strategies,
                            columns=self.india_strategies)
        print("US Payoffs (Trillion USD):")
        print(df_us)
        print()

        df_br = pd.DataFrame(brics_pay,
                            index=self.us_strategies,
                            columns=self.india_strategies)
        print("India (BRICS) Payoffs (Trillion USD):")
        print(df_br)
        print()

        print("🎯 NASH EQUILIBRIA:")
        if eq:
            for i, (us_i, br_i, us_p, br_p) in enumerate(eq):
                print(f"  Equilibrium {i+1}:")
                print(f"    US: {self.us_strategies[us_i]} → ${us_p:.2f}T")
                print(f"    India: {self.india_strategies[br_i]} → ${br_p:.2f}T")
        else:
            print("  None — no stable outcome")

        print("\n" + "—" * 60 + "\n")
        return eq

# 🔥 Run all combinations
if __name__ == "__main__":
    game = ExtendedCurrencyGame()

    print("="*70)
    print("   US-INDIA CURRENCY GAME: HOW STRATEGY CHANGES THE EQUILIBRIUM")
    print("   Based on Nash Equilibrium | Model: Rahul Modak")
    print("   GitHub: https://github.com/RahulModak74/US-INDIA_NASH_EQUILIBRIUM")
    print("="*70)
    print("\n")

    # Test all key scenarios
    scenarios = [
        ("Baseline", False, False, False, False),
        ("+ Positive Incentives", True, False, False, False),
        ("+ Credible Retaliation", False, True, False, False),
        ("+ BRICS Fragmentation", False, False, True, False),
        ("+ Digital Dollar", False, False, False, True),
        ("Full Strategy Package", True, True, True, True),
    ]

    for name, inc, ret, frag, dig in scenarios:
        print(f"🧪 {name}")
        game.run_scenario(inc, ret, frag, dig)