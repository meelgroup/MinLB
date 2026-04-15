import os, argparse, tempfile
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()
file_name = args.i

with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
    temp_file = f.name
    os.system("cp {0} {1}".format(args.i, temp_file))
    input_file = os.path.basename(temp_file)

os.system('python propagator.py -i {0}'.format(input_file))
print(" === Computing a cut === ")
os.system('./td -decot 100 -decow 100 -tmpdir . -cs 3500 minimal_{0} >> result-{0}'.format(input_file))
os.system('python prepare_td.py -i {0}'.format(input_file))
print(" === Running ProjEnum === ")
os.system('python decomposition.py -i cut_{0} -c 1'.format(input_file))

os.system(f'rm -f {input_file} cut_{input_file}')