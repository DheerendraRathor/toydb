import subprocess
import matplotlib.pyplot as plt
import numpy as np

sizes = [10, 100, 1000, 10000, 100000, 1000000]

time = []
time_sort = []

buffer_hit = []
buffer_hit_sort = []

nodes = []
nodes_sort = []

space = []
space_sort = []

level = []
level_sort = []

subprocess.call("make", shell=True)
for size in sizes:
	print "Processing for %s" % size
	filename = " random_"+str(size)
	subprocess.call("python create_input.py -n "+ str(size)+" -f"+filename, shell=True)
	output = subprocess.check_output("./a.out"+filename, shell=True)
	output = output.split('\n')
	time.append(float(output[0]))
	buf = output[1].split()
	buf_hit = int(buf[0])
	buf_miss = int(buf[1])
	buffer_hit.append((buf_hit)* 100.0/(buf_hit + buf_miss))
	node_lev = output[2].split()
	nodes.append(int(node_lev[1]))
	space.append(float(output[3]))
	level.append(int(node_lev[0]))

	output = subprocess.check_output("./a.out"+filename+"_sort", shell=True)
	output = output.split('\n')
	time_sort.append(float(output[0]))
	buf = output[1].split()
	buf_hit = int(buf[0])
	buf_miss = int(buf[1])
	buffer_hit_sort.append((buf_hit)* 100.0/(buf_hit + buf_miss))
	node_lev = output[2].split()
	nodes_sort.append(int(node_lev[1]))
	space_sort.append(float(output[3]))
	level_sort.append(int(node_lev[1]))

print "generating plots"

######################################################################################
print "Plot for timings"
ind = np.arange(len(sizes))
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, time, width, color='r')
rects2 = ax.bar(ind+width, time_sort, width, color='y')

ax.set_xlabel('Insertion Count')
ax.set_ylabel('Time in millis')
ax.set_title('Time in millis in insertion for sorted and unsorted file')
ax.set_xticks(ind+width)
ax.set_xticklabels(sizes)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.legend( (rects1[0], rects2[0]), ('unsorted', 'sorted'), loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('plots/time.png')
plt.gcf().clear()
######################################################################################

print "Generating plots for buffer hit"
ind = np.arange(len(sizes))
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, buffer_hit, width, color='r')
rects2 = ax.bar(ind+width, buffer_hit_sort, width, color='y')

ax.set_xlabel('Insertion Count')
ax.set_ylabel('Buffer hit in \%')
ax.set_title('buffer hit in \% in insertion for sorted and unsorted file')
ax.set_xticks(ind+width)
ax.set_xticklabels(sizes)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.legend( (rects1[0], rects2[0]), ('unsorted', 'sorted'), loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('plots/buff.png')
plt.gcf().clear()
######################################################################################

print "Generating plots for node count"
ind = np.arange(len(sizes))
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, nodes, width, color='r')
rects2 = ax.bar(ind+width, nodes_sort, width, color='y')

ax.set_xlabel('Insertion Count')
ax.set_ylabel('node count')
ax.set_title('node count in insertion for sorted and unsorted file')
ax.set_xticks(ind+width)
ax.set_xticklabels(sizes)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.legend( (rects1[0], rects2[0]), ('unsorted', 'sorted'), loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('plots/node.png')
plt.gcf().clear()
######################################################################################

print "Space Utilization plots"
ind = np.arange(len(sizes))
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, space, width, color='r')
rects2 = ax.bar(ind+width, space_sort, width, color='y')

ax.set_xlabel('Insertion Count')
ax.set_ylabel('space utilization factor in %')
ax.set_title('space utilization in insertion for sorted and unsorted file')
ax.set_xticks(ind+width)
ax.set_xticklabels(sizes)

box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.legend( (rects1[0], rects2[0]), ('unsorted', 'sorted'), loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('plots/space.png')
plt.gcf().clear()
######################################################################################

print "Plots generated, please check your plots folder"

print "Elemenet Count Table\n############################################################################"
i = 0
width =10
print "{:9s}type {:5s}time {:4s}buffer_hit {:4s}nodes {:4s}space {:4s}level".format("", "", "", "", "", "")
print "-------------------------------------------------------------------------"
for item in sizes:
	print "{:{width}d}_us {:{width}.3f} {:{width}.3f} {:{width}d} {:{width}.3f} {:{width}d}".format(item, time[i], buffer_hit[i], nodes[i], space[i], level[i], width=width)
	print "{:{width}d}_so {:{width}.3f} {:{width}.3f} {:{width}d} {:{width}.3f} {:{width}d}\n".format(item, time_sort[i], buffer_hit_sort[i], nodes_sort[i], space_sort[i], level[i], width=width)
	i = i+1

print "-------------------------------------------------------------------------"
print "legend: us:'unsorted' so:'sorted'"
print "################################################################################"


