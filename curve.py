import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from curve_sum import snm
from sim import run_ngspice

W_AX = 0.36e-6
VDD = 1.8
BETA = 2

run_ngspice("circuit/half_cell.cir",
            {"VDD_VALUE": VDD, "WPD": f"{BETA * W_AX:.3e}",
             "READ_FILE": "data/vtc_read.txt", "HOLD_FILE": "data/vtc_hold.txt"},
            out_files=["data/vtc_read.txt", "data/vtc_hold.txt"])

v_in_h, v_out_h = np.loadtxt("data/vtc_hold.txt", unpack=True, skiprows=1)
v_in_r, v_out_r = np.loadtxt("data/vtc_read.txt", unpack=True, skiprows=1)

snm_h, corner_h = snm(v_in_h, v_out_h)
snm_r, corner_r = snm(v_in_r, v_out_r)

ax = plt.gca()
ax.add_patch(Rectangle(corner_h, snm_h, snm_h, fill=False, edgecolor="tab:blue", linestyle="--"))
ax.add_patch(Rectangle(corner_r, snm_r, snm_r, fill=False, edgecolor="tab:red", linestyle="--"))

print(f"Hold SNM = {snm_h * 1000:.1f} mV")
print(f"Read SNM = {snm_r * 1000:.1f} mV")

plt.plot(v_in_h, v_out_h, color="tab:blue", label=f"Hold  SNM={snm_h * 1000:.0f} mV")
plt.plot(v_out_h, v_in_h, color="tab:blue")

plt.plot(v_in_r, v_out_r, color="tab:red", label=f"Read  SNM={snm_r * 1000:.0f} mV")
plt.plot(v_out_r, v_in_r, color="tab:red")

plt.legend()

plt.title(f"6T SRAM Butterfly Curve (VDD = {VDD} V, β = {BETA})")
plt.xlabel("Q [V]")
plt.ylabel("QB [V]")

plt.gca().set_aspect("equal")
plt.savefig("Fig/butterfly_curve_snm.png")

