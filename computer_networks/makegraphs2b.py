import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x_Axis = []
delay_Axis = []

for config in sys.argv[1:]:
	file = open(config)
	line = file.readline()
	while line:
		tokens = line.split()
		if (line.startswith("Average")):
			delay = float(tokens[3])

		line = file.readline()

	file.close()


	node_nr = config.strip('nodes/results_.txt')
	x_Axis.append(node_nr)
	delay_Axis.append(delay)

print x_Axis
print delay_Axis

fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("Nodes")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(delay_Axis) - 0.3 * min(delay_Axis), max(delay_Axis) + 0.2 * max(delay_Axis))
ax1.set_ylabel('Average Delay (sec)')
line1 = ax1.plot(delay_Axis, label="Average Delay", color="red",marker='o')

lns = line1
labs = [l.get_label() for l in lns]

plt.title("Average Delay")
lgd = plt.legend(lns, labs)
lgd.draw_frame(False)
plt.savefig("./nodes/delay.png",bbox_inches="tight")
