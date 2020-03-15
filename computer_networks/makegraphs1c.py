import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x_Axis = []
last_pakt_Axis = []

for config in sys.argv[1:]:
	file = open(config)
	line = file.readline()
	while line:
		tokens = line.split()
		if (line.startswith("Last")):
			last_pakt = float(tokens[5])

		line = file.readline()

	file.close()


	pkt_size = config.strip('packetsizes/results_.txt') + "B"
	x_Axis.append(pkt_size)
	last_pakt_Axis.append(last_pakt)

print x_Axis
print last_pakt_Axis

fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("Packet size")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(last_pakt_Axis) - 0.3 * min(last_pakt_Axis), max(last_pakt_Axis) + 0.2 * max(last_pakt_Axis))
ax1.set_ylabel('Last Packet received at (sec)')
line1 = ax1.plot(last_pakt_Axis, label="Last Packet received at", color="green",marker='o')

lns = line1
labs = [l.get_label() for l in lns]

plt.title("Last Packet received at")
lgd = plt.legend(lns, labs)
lgd.draw_frame(False)
plt.savefig("./packetsizes/last_pakt.png",bbox_inches="tight")
