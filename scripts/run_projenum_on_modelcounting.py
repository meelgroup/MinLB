import os, argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()
file_name = args.i

os.system('python compute_dlp.py -i {0}'.format(file_name))
print(" === Computing a cut === ")
os.system('./td -decot 100 -decow 100 -tmpdir . -cs 4000 minimal_{0} >> result-{0}'.format(file_name))
os.system('python prepare_td.py -i {0}'.format(file_name))
print(" === Running ProjEnum === ")
os.system('python decomposition.py -i cut_{0} -c 1'.format(file_name))