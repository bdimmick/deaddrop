deaddrop
========

Simple service to drop data over the network: clients can connect through TCP and 
write bytes to the service which will be recorded to a local directory in a file that is named 
for the client's IP and the timestamp the client connected.

This service is ideally used to aggregate data from many different machines on an intranet that 
are then processed by the server (e.g. log aggregation, packet analysis, etc.)

The clients connecting are assumed to be trusted and acting in the server's best interests 
(e.g. won't write forever and fill up disk).

