import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x_Axis = []
theor_Axis = []
pract_Axis = []


for config in sys.argv[1:]:
	file = open(config)
	line = file.readline()
	while line:
		tokens = line.split()
		if (line.startswith("Theoretical")):
			theoretical_util = float(tokens[3].strip('%'))
		elif (line.startswith("Practical")):
			practical_util = float(tokens[3].strip('%'))


		line = file.readline()

	file.close()


	pkt_size = config.strip('packetsizes/results_.txt') + "B"
	x_Axis.append(pkt_size)
	theor_Axis.append(theoretical_util)
	pract_Axis.append(practical_util)

print x_Axis
print theor_Axis
print pract_Axis

fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("Packet size")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(theor_Axis) - 0.3 * min(theor_Axis), max(theor_Axis) + 0.15 * max(theor_Axis))
ax1.set_ylabel('Utilisation (%)')
line1 = ax1.plot(theor_Axis, label="Theoretical", color="blue",marker='o')

ax2 = ax1
ax2.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax2.set_xticklabels(x_Axis, rotation=45)
ax2.set_xlim(-0.5, len(x_Axis) - 0.5)
ax2.set_ylim(min(pract_Axis) - 0.3 * min(pract_Axis), max(pract_Axis) + 0.15 * max(pract_Axis))
ax2.set_ylabel('Utilisation (%)')
line2 = ax2.plot(pract_Axis, label="Practical", color="red",marker='o')

lns = line1 + line2
labs = [l.get_label() for l in lns]

plt.title("Theoretical and Practical Utilisation")
lgd = plt.legend(lns, labs)
lgd.draw_frame(False)
plt.savefig("./packetsizes/utilisation.png",bbox_inches="tight")
