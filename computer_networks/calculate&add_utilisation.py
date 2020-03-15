from math import e

packetsizes = [64, 128, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
nodes = [5, 10, 15, 20]

bandwidth = 10000000
delay = 0.0000128
starttraf = 0.4

for packetsize in packetsizes:
	file = open('packetsizes/results_%s.txt' % packetsize, 'r')
	line = file.readline()
	while line:
		tokens = line.split()
		if (line.startswith("Total Packets received")):
			pkts_recv = int(tokens[4])
			data_recv = pkts_recv * packetsize * 8
		elif (line.startswith("Last Packet received at")):
			last_pkt_recv = float(tokens[5])
			transp_time = last_pkt_recv - starttraf
		line = file.readline()

	file.close()

	packet_bit_size = packetsize * 8.0
	R = float(data_recv / transp_time)
	P = float(packet_bit_size / bandwidth)
	practical_util = (R / bandwidth) * 100
	theoretical_util = (P / (P + 2*delay*e)) * 100

	file = open('packetsizes/results_%s.txt' % packetsize, 'a')
	file.write('Theoretical utilisation	: %0.2f%%\n' % theoretical_util)
	file.write('Practical utilisation	: %0.2f%%\n' % practical_util)
	file.close()


packetsize = 1500

for node_nr in nodes:
	file = open('nodes/results_%s.txt' % node_nr, 'r')
	line = file.readline()
	while line:
		tokens = line.split()
		if (line.startswith("Total Packets received")):
			pkts_recv = int(tokens[4])
			data_recv = pkts_recv * packetsize * 8
		elif (line.startswith("Last Packet received at")):
			last_pkt_recv = float(tokens[5])
			transp_time = last_pkt_recv - starttraf
		elif (line.startswith("Total Packets dropped")):
			pkts_drop = int(tokens[4])
			pkts_sent = float(pkts_recv + pkts_drop)
		line = file.readline()
	
	file.close()

	packet_bit_size = packetsize * 8.0
	R = float(data_recv / transp_time)
	P = float(packet_bit_size / bandwidth)
	practical_util = (R / bandwidth) * 100
	theoretical_util = (P / (P + 2*delay*e)) * 100
	dropped_perc = float(pkts_drop / pkts_sent) * 100

	file = open('nodes/results_%s.txt' % node_nr, 'a')
	file.write('Theoretical utilisation	: %0.2f%%\n' % theoretical_util)
	file.write('Practical utilisation	: %0.2f%%\n' % practical_util)
	file.write('Dropped Packets		: %0.2f%%\n' % dropped_perc)
	file.close()