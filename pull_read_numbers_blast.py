import sys

infile = sys.argv[1]
genus = sys.argv[2]

read_nums = set()
output_string = ""

with open(infile) as f:
    for line in f:
        if genus in line:
            line = line.split(",")
            read_nums.add(int(line[0]))

read_nums = sorted(read_nums)
for num in read_nums:
    output_string += str(num) + ", "

print(output_string[:-2])
