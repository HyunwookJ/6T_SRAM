import numpy as np
import matplotlib.pyplot as plt
from curve_sum import snm
from sim import run_ngspice

vdds = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

snm_read = []
snm_hold = []

for vdd in vdds:

    read_file = f"data/vdd/read_{vdd}.txt"
    hold_file = f"data/vdd/hold_{vdd}.txt"

    run_ngspice("circuit/vdd_template.cir",
                {"VDD_VALUE": vdd, "READ_FILE": read_file, "HOLD_FILE": hold_file},
                out_files=[read_file, hold_file])

    v_in_r, v_out_r = np.loadtxt(read_file, unpack=True, skiprows=1)
    v_in_h, v_out_h = np.loadtxt(hold_file, unpack=True, skiprows=1)

    snm_read.append(snm(v_in_r, v_out_r)[0])
    snm_hold.append(snm(v_in_h, v_out_h)[0])


for v, sr, sh in zip(vdds, snm_read, snm_hold):
    print(f"VDD={v}  ReadSNM={sr*1000:.1f} mV  HoldSNM={sh*1000:.1f} mV")


plt.plot(vdds, np.array(snm_hold) * 1000, "^--", color="tab:green", label="Hold SNM")
plt.plot(vdds, np.array(snm_read) * 1000, "s--", color="tab:blue", label="Read SNM")

plt.title("SNM vs VDD (β = 2)")
plt.xlabel("VDD [V]")
plt.ylabel("SNM [mV]")

plt.legend()

plt.grid(alpha=0.3)
plt.savefig("Fig/vdd_sweep_2.png")