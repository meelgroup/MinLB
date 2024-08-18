import os, argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()
file_name = args.i

os.system('python propagator.py -i {0}'.format(file_name))
os.system('./hashcounter --useind IS_dlp_{0} --asp dlp_{0}'.format(file_name))