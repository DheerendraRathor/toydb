import argparse
import random


parser = argparse.ArgumentParser(description='Internals Report')

parser.add_argument('-n', '--num',
                   help='Limit', required=True)
parser.add_argument('-f','--file', help='File Name', default='random')

parser.add_argument('-r', '--num-range', help='Num Range')

args = parser.parse_args()

filename = args.file
num = int(args.num)
num_range = args.num_range
if num_range is None:
	num_range = num
else:
	num_range = int(num_range)
randnum = []
i = 0
while i < num:
	randnum.append(random.randint(0, num_range))
	i = i + 1

randsort = sorted(randnum)
f = open(filename, 'w')

for x in randnum:
 	f.write("%s\n" % x)
f.close()

f = open(filename+"_sort", 'w')

for x in randsort:
	f.write('%s\n' % x)



