from itertools import combinations
import networkx as nx
import os, math
import argparse, time

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
parser.add_argument('-com','--com', help='use two components only', default=False, required=False)
parser.add_argument('-pro','--pro', help='do unit propagation over negated literals', default=False, required=False)
parser.add_argument('-t','--t', help='total time', default=5000, required=False)
args = parser.parse_args()
clingo_cmd = "clingo "
start_time = time.perf_counter()
max_time = int(args.t)
component_size_thresh = 50
# -com 1 components more than 2
# -com 0 components at most 2
if args.com == '1':
    print("Using components of size more than {0}".format(component_size_thresh))
else:
    print("Using only two components")

if args.pro == '1':
    print("Using unit propagation over negative answer set atoms")
else:
    print("Using no propagation")

file_name = args.i
input_formula = []
cut_var = []
previous_answer_sets = []
nvar = None
nclause = None
nanswer = 10**6
def compute_ASP(file_name, cnf):
    asp_file_name = "asp_" + file_name
    asp_file = open(asp_file_name, 'w')
    literals = set()
    for clause in cnf:
        body_list = []
        head_list = []
        for atom in clause:
            literals.add(abs(atom))
            if atom > 0:
                head_list.append(atom)
            elif atom < 0:
                body_list.append(abs(atom))
        rule_str = ""
        rule_str = ";".join("v"+str(_) for _ in head_list) \
            + ":-" + ",".join("v"+str(_) for _ in body_list) + ".\n"
        asp_file.write(rule_str)
    
    asp_file.close()
    return asp_file_name, literals

def blockLastAnswerSet(asp_input):
    asp_file = open(asp_input, 'a')
    for last_as in previous_answer_sets:
        # adding previous answer sets
        blocking_clause = ":- "
        if len(last_as) > 0:
            for index, symbol in enumerate(last_as):
                if symbol > 0:
                    blocking_clause = blocking_clause + " v" + str(symbol)
                elif symbol < 0:
                    blocking_clause = blocking_clause + " not v" + str(abs(symbol))
                if index < len(last_as) - 1:
                    blocking_clause += ","
                else:
                    blocking_clause += ".\n"
        else:
            blocking_clause += ".\n"
        asp_file.write(blocking_clause)
    asp_file.close()
        
def addConditioning(asp_file, positive, negative, literals):
    asp_file = open(asp_input, 'a')
    for _ in positive:
        if _ in literals:
            asp_file.write(":- not v{0}.\n".format(_))
    for _ in negative:
        if abs(_) in literals:
            asp_file.write(":- v{0}.\n".format(abs(_)))
    asp_file.close()

def addProjection(asp_file, projection):
    asp_file = open(asp_input, 'a')
    for _ in projection:
        asp_file.write("#project v{0}.\n".format(_))
    asp_file.close()

def ProjectedASPEnumeration(asp_file, project=True, time=0):
    if project:
        os.system("{0} --project=project -q -n {1} {2} > {3}-{2}".format(clingo_cmd, nanswer, asp_file, "result"))
    else:
        os.system("{0} -q -n 0 --time-limit={1} {2} > {3}-{2}".format(clingo_cmd, time, asp_file, "result"))
    # reading file 
    unsat = False
    ans = None
    underapprox = False
    for line in open("{0}-{1}".format("result", asp_file)):
        if line.startswith("Models"):
            l = line.strip().split(":")
            nSol = None
            if l[-1].endswith("+"):
                print("Under Approximation")
                underapprox = True
                l[-1] = l[-1][:-1]
            nSol = int(l[-1])

    return nSol, underapprox

        
def enumerateAnswerSet(asp_file):
    os.system("{0} {1} > {2}-{1}".format(clingo_cmd, asp_file, "result"))
    # reading file 
    unsat = False
    ans = None
    for line in open("{0}-{1}".format("result", asp_file)):
        if line.startswith("UNSATISFIABLE"):
            ans = None
            unsat = True
        elif line.startswith("v"):
            # we have answer set
            ans = []
            answer_set_symbols = line.split(" ")
            for symbol in answer_set_symbols:
                assert(symbol.startswith("v"))
                var = int(symbol[1:])
                if var in cut_var:
                    ans.append(var)

    # now negative variables 
    if not unsat:
        if ans is None:
            ans = []
        for var in cut_var:
            if var not in ans:
                ans.append(-var)
    return ans

for line in open(file_name, 'r'):
    if line.startswith("p cnf"):
        nvar = int(line.split()[-2])
        nclause = int(line.split()[-1])

    elif line.startswith("c"):
        if line.startswith("c ind"):
            l = line.split(" ")
            # start with c ind 
            # end with 0
            for index, _ in enumerate(l):
                if index > 1 and int(_) > 0:
                    cut_var.append(int(_))

    elif len(line) > 0 and line.endswith("0\n"):
        l = [int(_) for _ in line.split(" ") if int(_) != 0]
        input_formula.append(l)

def bcp(formula, unit):
    modified = []
    for clause in formula:
        if unit in clause: continue
        if -unit in clause:
            c = [x for x in clause if x != -unit]
            if len(c) == 0: return -1
            modified.append(c)
        else:
            modified.append(clause)
    return modified

def unit_propagation(formula, assumption):
    assignment = []
    unit_clauses = assumption
    while len(unit_clauses) > 0:
        unit = unit_clauses[0]
        assumption = [v for v in assumption if v != unit]
        formula = bcp(formula, unit)
        assignment += [unit]
        if formula == -1:
            return -1, []
        if not formula:
            return formula, assignment
        unit_clauses = assumption + [c[0] for c in formula if len(c) == 1]
    return formula, assignment

print("The size of cut: {0}".format(len(cut_var)))
print("Variables: {0} Clauses: {1}".format(nvar, len(input_formula)))


total_mm = 0
prompt = "iter: "
itera = 1
underapprox = False
size_of_SCC = []
while True:
    asp_input, literals = compute_ASP(file_name, input_formula)
    blockLastAnswerSet(asp_input)
    answer_set = enumerateAnswerSet(asp_input)
    previous_answer_sets.append(answer_set)
    prompt = "[iter: {0}] ".format(itera)
    # print(answer_set)
    if answer_set == None:
        # found UNSAT
        if underapprox:
            print("Final count: [under] The number of minimal models: {0}".format(total_mm))
        else:
            print("Final count: [exact] The number of minimal models: {0}".format(total_mm))
        exit()
    modified_input_formula, unit_assignment = unit_propagation(input_formula, [_ for _ in answer_set if _ < 0])
    print(prompt + "The unit propagated formula consists of {0} clauses".format(len(modified_input_formula)))

    G = nx.Graph()
    for clause in modified_input_formula:
        # check what happen for unit clauses
        for node1, node2 in list(combinations(clause, 2)):
            G.add_edge(abs(node1), abs(node2))

    print(prompt + "V, E: {0}, {1}".format(G.number_of_nodes(), G.number_of_edges()))
    list_scc = sorted(list(nx.connected_components(G)), key=len)
    size_of_SCC.append(len(list_scc))
    if len(list_scc) <= 1:
        print("The size of SCC: {0}".format(len(list_scc)))
        previous_answer_sets.pop()
        itera += 1
        if len(size_of_SCC) > 2 and size_of_SCC[-3] <= 1 and size_of_SCC[-2] <= 1 and size_of_SCC[-1] <= 1:
            print("We stop decomposition and start non-projected enumeration !!")
            break
        continue
    max_size = 0
    max_index = 0
    size_of_components = []
    var_of_components = []
    print("The size of SCC:", end="")
    for _ in list_scc:
        print(len(_), end=" ")
    print()
    if args.com == '1':
        size_of_components.append(len(list_scc[0]))
        var_of_components.append(list_scc[0])
        # print("Using components of size more than {0}".format(component_size_thresh))
        for _ in range(1,len(list_scc)):
            if size_of_components[-1] + len(list_scc[_]) > component_size_thresh:
                var_of_components.append(list_scc[_])
                size_of_components.append(len(list_scc[_]))
            else:
                size_of_components[-1] = size_of_components[-1] + len(list_scc[_])
                var_of_components[-1] = var_of_components[-1].union(list_scc[_])
    else: 
        # print("Using only two components")
        var_of_components.append(list_scc[0])
        var_of_components.append(list_scc[1])
        size_of_components.append(len(list_scc[0]))
        size_of_components.append(len(list_scc[1]))
        for _ in range(2, len(list_scc)):
            if size_of_components[0] <= size_of_components[1]:
                var_of_components[0] = var_of_components[0].union(list_scc[_])
                size_of_components[0] += len(list_scc[_])
            else:
                var_of_components[1] = var_of_components[1].union(list_scc[_])
                size_of_components[1] += len(list_scc[_])
            
    print(prompt + "The size of components:", end="")
    for _ in var_of_components:
        print(len(_), end=" ")
    print()
    # print(prompt + "The first consists of {0} variables.".format(len(first)))
    # print(prompt + "The second consists of {0} variables.".format(len(second)))
    negated = [_ for _ in answer_set if _ < 0]
    positive = [_ for _ in answer_set if _ > 0]
    if args.pro == '1':
        modified_input_formula, unit_assignment = unit_propagation(input_formula, negated)
        print("The negated formula consists of {0} clauses".format(len(modified_input_formula)))
    else:
        print("The negated formula consists of {0} clauses".format(len(input_formula)))
    cond_mm = 1
    count_in_iteration = 1
    enum_in_iteration = 0
    for index, com in enumerate(var_of_components):
        print(prompt + "Answer set w.r.t. {0}th component".format(index))
        if args.pro == '1':
            asp_input, literals = compute_ASP(file_name, modified_input_formula)
            addConditioning(asp_input, positive, negated, literals)
        else:
            asp_input, literals = compute_ASP(file_name, input_formula)
            addConditioning(asp_input, positive, negated, literals)
        addProjection(asp_input, com)
        n1, approx = ProjectedASPEnumeration(asp_input)
        underapprox = underapprox or approx
        print(prompt + "The number of projected answer set ({0}th component): {1}".format(index, n1))
        cond_mm = cond_mm * n1
        count_in_iteration = count_in_iteration * n1
        enum_in_iteration = enum_in_iteration + n1
        current_time = time.perf_counter()
        if current_time - start_time >= 0.75 * max_time:
            if index < len(var_of_components) - 1:
                underapprox = True
            break
    # print(prompt + "Answer set w.r.t. second set")
    # asp_input = compute_ASP(file_name, input_formula)
    # addConditioning(asp_input,positive,negated)
    # addProjection(asp_input,second)
    # n2 = ProjectedASPEnumeration(asp_input)
    # print(prompt + "The number of projected answer set: {0}".format(n2))
    total_mm = total_mm + cond_mm
    print(prompt + "Minimal models: {0}".format(total_mm))
    itera += 1
    current_time = time.perf_counter()
    if current_time - start_time >= 0.75 * max_time:
        break
    if count_in_iteration <= enum_in_iteration:
        size_of_SCC[-1] = 0
        if len(size_of_SCC) > 2 and size_of_SCC[-3] <= 1 and size_of_SCC[-2] <= 1 and size_of_SCC[-1] <= 1:
            print("We stop decomposition and start non-projected enumeration !!")
            break
    else:
        print("Decomposition has advantages !!!")

asp_input, literals = compute_ASP(file_name, input_formula)
blockLastAnswerSet(asp_input)
current_time = time.perf_counter()
remaining_time = max_time - (current_time - start_time)
if math.ceil(remaining_time) > 0:
    print("Time remaining for non projected enumeration: {0}".format(math.ceil(remaining_time)))
    nfinal, approx = ProjectedASPEnumeration(asp_input, False, math.ceil(remaining_time))
else:
    nfinal, approx = 0, False
underapprox = underapprox or approx
print("Non-projected number of answer sets: {0}".format(nfinal))
total_mm += nfinal
if underapprox:
    print("Final count: [under] The number of minimal models: {0}".format(total_mm))
else:
    print("Final count: [exact] The number of minimal models: {0}".format(total_mm))

os.system("rm result-*")

