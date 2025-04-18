import math
import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

def series():
    series = Circuit('Series RLC Circuit')
    series.SinusoidalVoltageSource('input', 'in', series.gnd, amplitude=1@u_V)
    series.R(1, 'in', 1, resistance=250)
    series.L(1, 1, 'out1', inductance=650@u_mH)
    series.C(1, 'out1', series.gnd, capacitance=1.5@u_uF)

    simulator = series.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=1000@u_Hz, stop_frequency=10@u_kHz, number_of_points=100, variation='dec')

    L = float(series['L1'].inductance)
    C = float(series['C1'].capacitance)
    R = float(series['R1'].resistance)

    resonant_freq = 1 / (2 * math.pi * math.sqrt(L * C))
    quality = 1 / R * math.sqrt(L / C)
    print(f"Resonant Frequency: {resonant_freq:.2f} Hz")
    print(f"Quality Factor: {quality:.2f}")

    frequencies = analysis.frequency
    current = abs(analysis['Vinput'])

    plt.figure(figsize=(8, 5))
    plt.semilogx(frequencies, current)
    plt.title('Series RLC Circuit')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Current Magnitude [A]')
    plt.grid(True, which='both', ls='--')
    plt.axvline(resonant_freq, color='r', linestyle=':', label=f'Resonance ≈ {resonant_freq:.1f} Hz')
    plt.legend()
    plt.tight_layout()
    plt.savefig("D:\\AGH\\3\\pythonInElectrical\\series_plot.png", dpi=300)

def parallel():
    parallel = Circuit('Parallel RLC Circuit')
    parallel.SinusoidalVoltageSource('input', 'in', parallel.gnd, amplitude=1@u_V)
    parallel.R(1, 'in', 'out1', resistance=250)
    parallel.L(1, 'in', 'out1', inductance=650@u_mH)
    parallel.C(1, 'out1', parallel.gnd, capacitance=1.5@u_uF)

    # Set up simulator
    simulator = parallel.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=100@u_Hz, stop_frequency=10@u_kHz, number_of_points=100, variation='dec')

    L = float(parallel['L1'].inductance)
    C = float(parallel['C1'].capacitance)
    R = float(parallel['R1'].resistance)

    resonant_freq = 1 / (2 * math.pi * math.sqrt(L * C))
    quality = R * math.sqrt(C / L)
    print(f"Resonant Frequency: {resonant_freq:.2f} Hz")
    print(f"Quality Factor: {quality:.2f}")

    frequencies = analysis.frequency
    current = abs(analysis['Vinput'])

    plt.figure(figsize=(8, 5))
    plt.semilogx(frequencies, current)
    plt.title('Parallel RLC Circuit')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Current Magnitude [A]')
    plt.grid(True, which='both', ls='--')
    plt.axvline(resonant_freq, color='r', linestyle=':', label=f'Resonance ≈ {resonant_freq:.1f} Hz')
    plt.legend()
    plt.tight_layout()
    plt.savefig("D:\\AGH\\3\\pythonInElectrical\\parallel_plot.png", dpi=300)


# So formula for frequency is 1/(2*pi*sqrt(L*C)) and for quality factor is R*sqrt(C/L)
# for parallel circuit, in series it's 1/(R*sqrt(L/C)). Frequency wil be the same
# for both circuits, since we have the same L and C. It will be 161,182 Hz, so it
# agrees with the problem calculated value
if __name__ == "__main__":
    series()
    parallel()
