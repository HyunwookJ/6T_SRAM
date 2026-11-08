import re
import subprocess
import numpy as np
import matplotlib.pyplot as plt

W_AX = 0.36e-6
VDD = 1.8
gammas = [0.5, 1, 1.5, 2, 3]

wr_template = open("circuit/wr_template.cir").read()   # trip 전압 (DC)
wt_template = open("circuit/wt_template.cir").read()   # 쓰기 시간 (tran)

v_trip = []
t_write = []

for gamma in gammas:
    wpu = f"{gamma * W_AX:.3e}"
    out_file = f"data/write/write_{gamma}.txt"

    # 1) trip 전압: BL을 1.8 -> 0V로 내리며 Q가 VDD/2 아래로 처음 내려가는 BL 전압
    with open("tmp.cir", "w") as f:
        f.write(wr_template.replace("WPU", wpu).replace("WRITE_FILE", out_file))
    subprocess.run(["ngspice", "-b", "tmp.cir"], capture_output=True)

    data = np.loadtxt(out_file, skiprows=1)
    v_bl, v_q = data[:, 0], data[:, 1]
    flip = np.where(v_q < VDD / 2)[0]
    v_trip.append(v_bl[flip[0]] if len(flip) else np.nan)

    # 2) 쓰기 시간: WL이 켜진 순간부터 Q가 VDD/2 아래로 내려갈 때까지
    with open("tmp.cir", "w") as f:
        f.write(wt_template.replace("WPU", wpu))
    result = subprocess.run(["ngspice", "-b", "tmp.cir"], capture_output=True, text=True)

    m = re.search(r"twr\s*=\s*([-+0-9.eE]+)", result.stdout)
    t_write.append(float(m.group(1)) if m else np.nan)
    if not m:
        print(f"[gamma={gamma}] twr 측정 실패:")
        print(result.stdout[-600:])

for g, vt, tw in zip(gammas, v_trip, t_write):
    print(f"gamma={g}  trip BL={vt*1000:.0f} mV  write time={tw*1e12:.1f} ps")


fig, ax1 = plt.subplots()
ax1.plot(gammas, np.array(v_trip) * 1000, "o-", color="tab:purple")
ax1.set_xlabel("γ ratio (PU / AX)")
ax1.set_ylabel("Write trip voltage of BL [mV]", color="tab:purple")
ax1.grid(alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(gammas, np.array(t_write) * 1e12, "s--", color="tab:brown")
ax2.set_ylabel("Write time [ps]", color="tab:brown")

ax1.set_title("Writability vs γ Ratio (VDD = 1.8 V)")
fig.tight_layout()
fig.savefig("Fig/write_sweep.png")