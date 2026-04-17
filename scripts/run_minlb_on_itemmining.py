import os, argparse, tempfile
import subprocess as sp
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()
file_name = args.i

def run(cmd, timeout, ttl = 3, silent = False):
    proc = sp.Popen([cmd], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    print(f"Running command: {cmd}")
    try:
        (out, err) = proc.communicate(timeout = int(timeout * 1.1) + 1)
        out = out.decode("utf-8")
    except sp.TimeoutExpired:
        proc.kill()
        try:
            (out, err) = proc.communicate()
            out = out.decode("utf-8")
        except ValueError:
            if ttl > 0:
                return run(cmd, timeout, ttl - 1)
            out = ""
    return out

with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
    temp_file = f.name
    os.system("cp {0} {1}".format(args.i, temp_file))
    input_file = os.path.basename(temp_file)

cmd = 'python propagator.py -i {0}'.format(input_file)

out = run(cmd, 100)
# print(" === Computing a cut === ")
cmd = './td -decot 50 -decow 100 -tmpdir . -cs 3500 minimal_{0}'.format(input_file)
out = run(cmd, 120)
cut_size = None
cut_string = ""
for line in out.splitlines():
    if line.startswith("c the size of cut:"):
        l = line.split()
        print("minlb: cut size: {0}".format(l[-1]))
        cut_size = int(l[-1])
    elif line.startswith("c tree decomposition cut:"):
        cut_string = line.replace("c tree decomposition cut:", "c ind")
        cut_string = cut_string.replace(",", " ")

new_input_file = "cut_" + input_file
with open("minimal_" + input_file, 'r+') as cnffile:
    content = cnffile.read()
    cnffile = open(new_input_file, 'w')
    cnffile.write(content)
    cnffile.write(cut_string.rstrip() + '\n')
    cnffile.close

if cut_size is not None and cut_size <= 50:
    # we can run ProjEnum
    # print(" === Running ProjEnum === ")
    cmd = 'python decomposition.py -i cut_{0} -c 1'.format(input_file)
    out = run(cmd, 5000)
    print(out)
    cnt = None
    for line in out.splitlines():
        if line.startswith("Final count:"):
            cnt = line
            print("minlb: projenum: {0}".format(line))

    if cnt is None:
        print("No estimate found in the projenum.")

    os.system(f'rm -f {input_file} cut_{input_file} minimal_{input_file}')

else:
    cmd = './hashcount --useind IS_dlp_{0} --asp dlp_{0}'.format(input_file)
    out = run(cmd, 5000)
    print(out)
    cnt = None
    for line in out.splitlines():
        if line.startswith("After the iteration, the lower bound:"):
            cnt = line
            print("minlb: hashcount: {0}".format(line))

    if cnt is None:
        print("No estimate found in the hashcount.")

    os.system(f'rm -f {input_file} IS_dlp_{input_file} dlp_{input_file}')