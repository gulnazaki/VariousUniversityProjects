import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x_Axis = []
dropped_perc_Axis = []

for config in sys.argv[1:]:
	file = open(config)
	line = file.readline()
	while line:
		tokens = line.split()
		if (line.startswith("Dropped")):
			dropped_perc = float(tokens[3].strip('%'))

		line = file.readline()

	file.close()


	node_nr = config.strip('nodes/results_.txt')
	x_Axis.append(node_nr)
	dropped_perc_Axis.append(dropped_perc)

print x_Axis
print dropped_perc_Axis

fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("Nodes")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(dropped_perc_Axis) - 0.3 * min(dropped_perc_Axis), max(dropped_perc_Axis) + 0.2 * max(dropped_perc_Axis))
ax1.set_ylabel('Dropped Packages Percentage (%)')
line1 = ax1.plot(dropped_perc_Axis, label="Dropped Packages", color="black",marker='o')

lns = line1
labs = [l.get_label() for l in lns]

plt.title("Dropped Packages Percentage")
lgd = plt.legend(lns, labs)
lgd.draw_frame(False)
plt.savefig("./nodes/dropped_perc.png",bbox_inches="tight")
