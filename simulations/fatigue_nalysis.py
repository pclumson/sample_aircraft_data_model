import numpy as np
from models.component import AircraftComponent, LoadCase
from scipy.stats import weibull_min

class FatigueAnalyzer:
    """Simulates fatigue life based on load cycles."""

    def __init__(self, component: AircraftComponent):
        self.component = component
        self.material_properties = {
            'aluminum': {'S_ut': 310e6, 'S_e': 97e6, 'm': 3.0}, # Ultimate strength, Endurance limit, Basquin exponent
            'carbon_fiber': {'S_ut': 600e6, 'S_e': 200e6, 'm': 10.0}
        }

    def calculate_stress_amplitude(self, load_case):
        # Simplified stress calculation: Force / Area
        area = self.component.dimensions.width * self.component.dimensions.height
        force_mag = np.sqrt(sum(np.array(load_case.force_vector)**2))
        return force_mag / area

    def estimate_cycles_to_failure(self, stress_amp):
        props = self.material_properties[self.component.material.value]
        if stress_amp > props['S_ut']:
            return 0 # Immediate failure
        if stress_amp < props['S_e']:
            return float('inf') # Infinite life

        # Basquin's Law: S_a = S_f' * (2N)^b
        # Simplified: N = (S_a / S_f')^(1/b)
        b = -1 / props['m']
        S_f_prime = props['S_ut']
        cycles = (stress_amp / S_f_prime) ** (1/b)
        return cycles

    def run_simulation(self):
        results = []
        for lc in self.component.load_cases:
            if lc.case_type == LoadCase.FATIGUE:
                stress = self.calculate_stress_amplitude(lc)
                cycles = self.estimate_cycles_to_failure(stress)
                results.append({
                    'case': lc.case_type.value,
                    'stress_MPa': stress / 1e6,
                    'cycles_to_failure': cycles
                })
        return results

# Usage
# analyzer = FatigueAnalyzer(wing_splice)
# print(analyzer.run_simulation())
