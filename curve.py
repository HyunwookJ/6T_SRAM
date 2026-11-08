import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from curve_sum import snm


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

plt.title("6T SRAM Butterfly Curve (VDD = 1.8 V, β = 2)")
plt.xlabel("Q [V]")
plt.ylabel("QB [V]")

plt.gca().set_aspect("equal")
plt.savefig("Fig/butterfly_curve_snm.png")

