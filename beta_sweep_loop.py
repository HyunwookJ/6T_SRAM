import numpy as np
import matplotlib.pyplot as plt
from curve_sum import snm
from sim import run_ngspice

W_AX = 0.36e-6
betas = [0.5, 1, 1.5, 2, 2.5, 3, 4]

q_read = []
snm_read = []
snm_hold = []
i_read = []

for beta in betas:

    wpd = beta * W_AX
    read_file = f"data/Beta/read_{beta}.txt"
    hold_file = f"data/Beta/hold_{beta}.txt"

    run_ngspice("circuit/beta_template.cir",
                {"WPD": f"{wpd:.3e}", "READ_FILE": read_file, "HOLD_FILE": hold_file},
                out_files=[read_file, hold_file])

    d_r = np.loadtxt(read_file, skiprows=1)
    v_in_r, v_out_r = d_r[:, 0], d_r[:, 1]
    v_in_h, v_out_h = np.loadtxt(hold_file, unpack=True, skiprows=1)

    q_read.append(v_out_r[-1])
    snm_read.append(snm(v_in_r, v_out_r)[0])
    snm_hold.append(snm(v_in_h, v_out_h)[0])
    i_read.append(-d_r[-1, 3])

for b, q, sr, sh, ir in zip(betas, q_read, snm_read, snm_hold, i_read):
    print(f"beta={b}  Q(read)={q*1000:.1f} mV  ReadSNM={sr*1000:.1f} mV  HoldSNM={sh*1000:.1f} mV Iread={ir*1e6:.0f} uA")

q_mV = np.array(q_read) * 1000
snm_r_mV = np.array(snm_read) * 1000
snm_h_mV = np.array(snm_hold) * 1000

fig, ax1 = plt.subplots()

ax1.plot(betas, q_mV, "o-", color="tab:red")
ax1.set_xlabel("β ratio")
ax1.set_ylabel("Q during read [mV]", color="tab:red")

ax2 = ax1.twinx()                     
ax2.plot(betas, snm_r_mV, "s--", color="tab:blue", label="Read SNM")
ax2.plot(betas, snm_h_mV, "^--", color="tab:green", label="Hold SNM")
ax2.set_ylabel("SNM [mV]")
ax2.legend()

ax2.legend(loc="center right")

ax1.set_title("Effect of β Ratio on Stability (VDD = 1.8 V)")

plt.savefig("Fig/beta_sweep.png")

i_uA = np.array(i_read) * 1e6
ref = betas.index(2)                     # β=2의 위치

snm_norm = snm_r_mV / snm_r_mV[ref]
i_norm = i_uA / i_uA[ref]

fig2, bx = plt.subplots()

bx.plot(betas, snm_norm, "s--", color="tab:blue", label="Read SNM")
bx.plot(betas, i_norm, "D-", color="tab:orange", label="Read current")

bx.axhline(1, color="gray", linestyle=":")      # 기준선 (β=2)

bx.set_title("Relative change of Read SNM and Read Current vs β")
bx.set_xlabel("β ratio")
bx.set_ylabel("Normalized to β = 2")

bx.legend()
bx.grid(alpha=0.3)

fig2.savefig("Fig/beta_iread.png")