import os, argparse, tempfile
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()
file_name = args.i

with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
    temp_file = f.name
    os.system("cp {0} {1}".format(args.i, temp_file))
    input_file = os.path.basename(temp_file)

os.system('python compute_dlp.py -i {0}'.format(input_file))
print(" === Computing independent suport === ")
os.system('python compute_independent_support.py -i dlp_{0}'.format(input_file))
print(" === Running HashCount === ")
os.system('./hashcount --useind IS_dlp_{0} --asp dlp_{0}'.format(input_file))

os.system(f'rm -f {input_file} dlp_{input_file} IS_dlp_{input_file}')