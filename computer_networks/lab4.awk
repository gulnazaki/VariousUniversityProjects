BEGIN {
  data=0;
  packets=0;
  first_package_sent=1.3;
}

/^r/&&/tcp/ {
  data+=$6;
  packets++;
}

/^r/&&/ack/ {
  last_ack_received=$2
}

END{
  printf("Total Data received\t: %d Bytes\n", data);
  printf("Total Packets received\t: %d\n", packets);
  printf("Total Transmission time\t: %f\n", (last_ack_received-first_package_sent));
}
