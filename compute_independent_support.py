import argparse
import networkx as nx
from networkx.algorithms.approximation import vertex_cover
from clingo import Control
from clingo import Function
import time

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
parser.add_argument('-t','--t', help='timeout', required=False)
args = parser.parse_args()

# default time for IS
max_time = 200
if args.t != None:
    max_time = args.t
small_time = 20

print("The timeout is set to {0}".format(max_time))
# the graph
grph = nx.Graph() 

print("The input file is: {0}".format(args.i))
print("=============== We create copy program ===============")

copy_program = "copy_" + args.i.replace("dlp_", "")
copy_program_writer = open(copy_program, 'w')

initial_independent_support = set()
for line in open(args.i, 'r'):
    if not line.startswith("%"):
        line1 = line.replace("v", "x")
        line2 = line.replace("v", "y")

        copy_program_writer.write(line1)
        copy_program_writer.write(line2)

        head_atoms = list()
        head_str = None
        if ":-" not in line:
            head_str = line.replace(".", "").strip()
        else:
            head_str = line[:line.find(":-")]
        # parse the head 
        head_atoms = head_str.split(";")
        # print("The number of head atoms: {0}".format(head_atoms))
        if len(head_atoms) > 1:
            for i1 in range(0, len(head_atoms)):
                initial_independent_support.add(head_atoms[i1])
                for i2 in range(i1 + 1, len(head_atoms)):
                    if i1 != i2 and head_atoms[i1] != head_atoms[i2]:
                        grph.add_edge(head_atoms[i1].strip(), head_atoms[i2].strip())


print("The number of nodes: {0} and edges: {1}".format(grph.number_of_nodes(), grph.number_of_edges()))
print("========== Computing the backdoor ========== ")
vc = vertex_cover.min_weighted_vertex_cover(grph)
print("The size of backdoor: {0}".format(len(vc)))
priority = dict()
for vc_nodes in vc:
    new_var = vc_nodes.replace("v", "z")
    x_var = vc_nodes.replace("v", "x")
    y_var = vc_nodes.replace("v", "y")
    copy_program_writer.write("{ " + new_var + " }.\n") # z_i is a free variable
    constraint1 = ":- {0}, not {1}, {2}.\n".format(x_var, y_var, new_var) 
    constraint2 = ":- not {0}, {1}, {2}.\n".format(x_var, y_var, new_var)
    copy_program_writer.write(constraint1)
    copy_program_writer.write(constraint2)
    # it is useful to do sorting
    priority[vc_nodes.replace("v", "")] = grph.degree[vc_nodes]

copy_program_writer.close()
# print(priority)

def get_index(element):
    return priority[element]
 
# Sort the original list based on the sort order list using sorted() function and the custom function as the key

print("========== Computing the independent support ========== ")
if True:
    ctl = Control(["0"])
    ctl.configuration.solve.models = 1 # check SAT or UNSAT
    ctl.load(copy_program)
    ctl.ground([("base", [])])

    unknown = []
    for _ in ctl.symbolic_atoms.signatures:
        if _[0].startswith("z"):
            unknown.append(_[0].replace("z", ""))

    start_time = time.perf_counter()
    print("The size of Independent support: {0}".format(len(unknown)))
    assumptions = list()
    unknown = sorted(unknown, key=get_index)
    mathcal_I = list()
    while len(unknown) > 0:
        assumptions.clear()
        index = unknown.pop()

        for j in mathcal_I:
            assumptions.append((Function("z"+j), True))
        for j in unknown:
            assumptions.append((Function("z"+j), True))

        assumptions.append((Function("x"+index), True)) # x is the original set of variable
        assumptions.append((Function("y"+index), False)) # y is the copy variable 
        # ret = ctl.solve(assumptions=assumptions)
        with ctl.solve(async_=True, assumptions=assumptions) as handle:
            handle.wait(small_time)
            handle.cancel()
            ret = handle.get()
            if not ret.unsatisfiable:
                mathcal_I.append(index)

        # run the script for a fixed time
        current_time = time.perf_counter()
        if current_time - start_time >= max_time:
            break

    print("The size of Final independent support: {0}".format(len(mathcal_I) + len(unknown)))
    # printing the independent support 
    IS_file_pointer = open("IS_" + args.i, 'w')
    independent_str = "c ind "
    for is_atoms in mathcal_I:
        independent_str += "v{0} ".format(is_atoms)
    for un_atoms in unknown:
        independent_str += "v{0} ".format(un_atoms)
    independent_str += "0"
    # print(independent_str)
    IS_file_pointer.write(independent_str)
    IS_file_pointer.close()

