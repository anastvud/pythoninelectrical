import pandapower as pp
import pandapower.plotting as plot
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def create_5bus_system():

    net = pp.create_empty_network(name="Set IX")

    # Create buses (20kV base)
    bus_slack_1 = pp.create_bus(net, vn_kv=230, name="Slack Bus")
    bus_pv_2 = pp.create_bus(net, vn_kv=230, name="PV Bus")
    bus_pq_3 = pp.create_bus(net, vn_kv=230, name="PQ Bus 3")
    bus_pq_4 = pp.create_bus(net, vn_kv=230, name="PQ Bus 4")
    bus_pq_5 = pp.create_bus(net, vn_kv=230, name="PQ Bus 5")

    # Add slack (reference bus)
    pp.create_ext_grid(net, bus=bus_slack_1, vm_pu=1.06)

    # Add generator (PV bus)
    pp.create_gen(net, bus=bus_pv_2, p_mw=40)

    # Add load (PQ bus)
    pp.create_load(net, bus=bus_pq_3, p_mw=45, q_mvar=15)
    pp.create_load(net, bus=bus_pq_4, p_mw=3594, q_mvar=5) # should be 40, but at 3594 fails
    pp.create_load(net, bus=bus_pq_3, p_mw=60, q_mvar=10)

    # Add lines (Z_base = 20²/100 = 4 Ω)
    pp.create_line_from_parameters(
        net,
        from_bus=bus_slack_1, to_bus=bus_pv_2,
        length_km=50,
        r_ohm_per_km=0.02,
        x_ohm_per_km=0.6,
        c_nf_per_km=0,
        max_i_ka=1
    )
    pp.create_line_from_parameters(
        net,
        from_bus=bus_slack_1, to_bus=bus_pq_3,
        length_km=60,
        r_ohm_per_km=0.08,
        x_ohm_per_km=0.24,
        c_nf_per_km=0,
        max_i_ka=1
    )
    pp.create_line_from_parameters(
        net,
        from_bus=bus_pv_2, to_bus=bus_pq_3,
        length_km=40,
        r_ohm_per_km=0.06,
        x_ohm_per_km=0.25,
        c_nf_per_km=0,
        max_i_ka=1
    )
    pp.create_line_from_parameters(
        net,
        from_bus=bus_pv_2, to_bus=bus_pq_4,
        length_km=30,
        r_ohm_per_km=0.06,
        x_ohm_per_km=0.18,
        c_nf_per_km=0,
        max_i_ka=1
    )
    pp.create_line_from_parameters(
        net,
        from_bus=bus_pv_2, to_bus=bus_pq_5,
        length_km=45,
        r_ohm_per_km=0.04,
        x_ohm_per_km=0.12,
        c_nf_per_km=0,
        max_i_ka=1
    )
    pp.create_line_from_parameters(
        net,
        from_bus=bus_pq_3, to_bus=bus_pq_4,
        length_km=55,
        r_ohm_per_km=0.01,
        x_ohm_per_km=0.03,
        c_nf_per_km=0,
        max_i_ka=1
    )
    pp.create_line_from_parameters(
        net,
        from_bus=bus_pq_4, to_bus=bus_pq_5,
        length_km=35,
        r_ohm_per_km=0.08,
        x_ohm_per_km=0.24,
        c_nf_per_km=0,
        max_i_ka=1
    )

    # Solve power flow
    pp.runpp(net)

    return net

def pv_curve_analysis(net, load_bus, scaling_range=np.linspace(0.1, 3.0, 30)):
    """
    Perform PV curve analysis by scaling load at specified bus

    Args:
        net: pandapower network
        load_bus: bus index where load is scaled
        scaling_range: array of load scaling factors

    Returns:
        tuple: (loadings, voltages, max_point)
    """
    voltages = []
    loadings = []
    max_point = None

    # Store original load values
    load_idx = net.load[net.load.bus == load_bus].index[0]
    original_p = net.load.at[load_idx, 'p_mw']
    original_q = net.load.at[load_idx, 'q_mvar']

    for scale in scaling_range:
        # Scale load
        net.load.at[load_idx, 'p_mw'] = original_p * scale
        net.load.at[load_idx, 'q_mvar'] = original_q * scale

        try:
            pp.runpp(net)
            voltages.append(net.res_bus.at[load_bus, 'vm_pu'])
            loadings.append(original_p * scale)
        except pp.powerflow.LoadflowNotConverged:
            print(f"Power flow did not converge at scale {scale:.2f}")
            break

    # Find maximum loadability point (nose point of PV curve)
    if len(loadings) > 3:
        try:
            # Use cubic interpolation to find maximum
            f = interp1d(loadings, voltages, kind='cubic', fill_value='extrapolate')
            load_fine = np.linspace(min(loadings), max(loadings), 100)
            voltage_fine = f(load_fine)
            max_idx = np.argmax(load_fine)
            max_point = (load_fine[max_idx], voltage_fine[max_idx])
        except:
            max_point = None

    # Restore original load
    net.load.at[load_idx, 'p_mw'] = original_p
    net.load.at[load_idx, 'q_mvar'] = original_q

    return loadings, voltages, max_point


def plot_pv_curve(loadings, voltages, max_point=None):
    """Plot PV curve with stability indicators"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot PV curve
    ax.plot(loadings, voltages, 'bo-', label='PV Curve')

    # Mark maximum loadability point if found
    if max_point:
        ax.plot(max_point[0], max_point[1], 'ro', markersize=10,
                label=f'Max Load: {max_point[0]:.2f} MW')
        ax.axvline(max_point[0], color='r', linestyle='--', alpha=0.5)

    # Add stability margin annotation
    if max_point and len(loadings) > 1:
        margin = (max_point[0] - loadings[-1]) / max_point[0] * 100
        ax.annotate(f'Stability Margin: {abs(margin):.1f}%',
                    xy=(loadings[-1], voltages[-1]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))

    ax.set_title('PV Curve - Voltage Stability Analysis', fontsize=14)
    ax.set_xlabel('Load Power [MW]', fontsize=12)
    ax.set_ylabel('Voltage [pu]', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    plt.tight_layout()
    plt.show()


def voltage_stability_analysis(net):
    """Complete voltage stability analysis workflow"""

    # Identify critical load bus (bus4 in our test system)
    load_bus = net.load.bus.iloc[0]

    # Run PV curve analysis
    print("Running PV curve analysis...")
    scaling_factors = np.linspace(0.1, 2.5, 30)  # More points for better resolution
    loadings, voltages, max_point = pv_curve_analysis(net, load_bus, scaling_factors)

    # Visualize results
    plot_pv_curve(loadings, voltages, max_point)

    # Print key stability metrics
    if max_point:
        print("\nVoltage Stability Metrics:")
        print(f"Maximum Loadability: {max_point[0]:.2f} MW")
        print(f"Critical Voltage: {max_point[1]:.4f} pu")

        # Calculate P-V margin
        p_margin = max_point[0] - loadings[-1]
        print(f"Load Margin: {p_margin:.2f} MW ({p_margin / max_point[0] * 100:.1f}%)")
    else:
        print("Warning: Could not determine maximum loadability point")

# Execute and print results
if __name__ == "__main__":
    network = create_5bus_system()

    print("\n--- Bus Results ---")
    print(network.res_bus[['vm_pu', 'va_degree']])

    print("\n--- Line Flows ---")
    print(network.res_line[['p_from_mw', 'q_from_mvar', 'loading_percent']])

    voltage_stability_analysis(network)