import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)

args = parser.parse_args()

file_name = args.i

cut_string = ""
for line in open("result-" + file_name):
    if line.startswith("c tree decomposition cut:"):
        cut_string = line.replace("c tree decomposition cut:", "c ind")
        cut_string = cut_string.replace(",", " ")

new_input_file = "cut_" + file_name
with open("minimal_" + file_name, 'r+') as cnffile:
    content = cnffile.read()
    cnffile = open(new_input_file, 'w')
    cnffile.write(content)
    cnffile.write(cut_string.rstrip() + '\n')
    cnffile.close

