import os, argparse, tempfile
import subprocess as sp
parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()
file_name = args.i

def run(cmd, timeout, ttl = 3, silent = False):
    proc = sp.Popen([cmd], stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
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

cmd = './hashcount --useind IS_dlp_{0} --asp dlp_{0}'.format(input_file)
out = run(cmd, 5000)
cnt = None
for line in out.splitlines():
    if line.startswith("After the iteration, the lower bound:") or line.startswith("The exact number of solution:"):
        cnt = line
        print("hashcount: {0}".format(line))

if cnt is None:
    print("No estimate found in the hashcount.")

os.system(f'rm -f {input_file} IS_dlp_{input_file} dlp_{input_file}')