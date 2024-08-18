import os, argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()
file_name = args.i

os.system('python compute_dlp.py -i {0}'.format(file_name))
print(" === Computing independent suport === ")
os.system('python compute_independent_support.py -i dlp_{0}'.format(file_name))
print(" === Running HashCount === ")
os.system('./hashcounter --useind IS_dlp_{0} --asp dlp_{0}'.format(file_name))