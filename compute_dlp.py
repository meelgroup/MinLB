import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input CNF file', required=True)
args = parser.parse_args()

def compute_disjunctive_program(file_name):
    output_file = "dlp_" + file_name 
    # os.system("mv {0} {1}".format("prep_" + file_name, file_name))
    # file_pointer = open(file_name, 'r')
    file_pointer = open(file_name, 'r')
    output_file_pointer = open(output_file, 'w')
    for line in file_pointer:
        if line.startswith("c"):
            continue
        elif line.startswith("p cnf"):
            l = line.split()
            output_file_pointer.write("%rule size: {0}\n".format(int(l[-1])))
            # print("The number of literals: {0} and clauses: {1} [Unpreprocessed]".format(l[-2], l[-1]))
        else:
            l = line.split()
            lit_list = []
            for lit in l:
                var = int(lit)
                if var != 0:
                    lit_list.append(var)
                
            rule_string = ""
            head_lit = []
            head_str = ""
            body_lit = []
            body_str = ""
            rule_str = ""
            node_lit = []
            for index, lit in enumerate(lit_list):
                if lit < 0:
                    body_lit.append("v{0}".format(abs(lit)))
                else:
                    head_lit.append("v{0}".format(lit))
                    node_lit.append(lit)
            
            for index, lit in enumerate(head_lit):
                if index == 0:
                    head_str = lit
                else:
                    head_str += (" ; " + lit)
            
            for index, lit in enumerate(body_lit):
                if index == 0:
                    body_str = lit
                else:
                    body_str += (" , " + lit)
            if len(body_lit) == 0 and len(head_lit) == 0:
                continue
            elif len(body_lit) == 0:
                rule_str = head_str + "."
            elif len(head_lit) == 0:
                rule_str = ":- " + body_str + "."
            else:
                rule_str = head_str + " :- " + body_str + "."
            # writing the rule 
            output_file_pointer.write(rule_str + "\n")

        
    file_pointer.close()
    output_file_pointer.close()

file_name = args.i
# first we are computing the cautious reasoning
output_file = "lp_" + file_name 
# doing the preprocessing first 
# using the cautious reasoning computed from wasp
# do preprocessing 
compute_disjunctive_program(file_name)
preprocess = True
original_set_var = None
original_set_clause = None
cautious = False # set to True to turn on cautious reasoning
if preprocess:
    file_pointer = open(file_name, 'r')
    for line in file_pointer:
        if line.startswith("c"):
            continue
        elif line.startswith("p cnf"):
            l = line.split()
            # print("The number of literals: {0} and clauses: {1} [Unpreprocessed]".format(l[-2], l[-1]))
            original_set_var = int(l[-2]) 
            original_set_clause = int(l[-1]) 
            break
    file_pointer.close()
    # check_positive_literals(file_name)
    os.system("cp {0} prep_{0}".format(file_name))
    # os.system("mv {0} {1}".format("prep_" + file_name, file_name))
# file_pointer = open(file_name, 'r')
# check whether the preprocessing failed or not
final_input_filename = "prep_" + file_name
file_pointer = open(final_input_filename, 'r')
output_file_pointer = open(output_file, 'w')
# grph = nx.Graph() 
varset = set()
aspino_file_pointer = open("aspino_" + file_name , 'w')
minimal_file_pointer = open("minimal_" + file_name , 'w')
asprin_file_pointer = open("asprin_" + file_name , 'w')
aspino_file_pointer.write("p ccnf -\n")
o_line = "o "
for _ in range(1, original_set_var + 1):
    o_line = o_line + (str(_) + " ")
o_line = o_line + ("0")
aspino_file_pointer.write(o_line + "\n")
for line in file_pointer:
    if line.startswith("c"):
        if line.startswith("c Number of clauses:"):
            l = line.split()
            print("The number of non-trivial clauses: {0}".format(l[-1]))
        continue
    elif line.startswith("p cnf"):
        l = line.split()
        output_file_pointer.write("%rule size: {0}\n".format(int(l[-1])))
        asprin_file_pointer.write("%rule size: {0}\n".format(int(l[-1])))
        minimal_file_pointer.write(line)
        minimal_file_pointer.write("c opt {0}\n".format(original_set_var))
        print("The number of literals: {0} and clauses: {1}".format(l[-2], l[-1]))
    else:
        l = line.split()
        aspino_file_pointer.write(line)
        minimal_file_pointer.write(line)
        lit_list = []
        for lit in l:
            var = int(lit)
            if var != 0:
                lit_list.append(var)
            
        rule_string = ""
        rule_str = ":- "
        node_lit = []
        for index, lit in enumerate(lit_list):
            if lit < 0:
                if abs(lit) <= original_set_var:
                    rule_str = rule_str + " v({0}),".format(abs(lit))
                else:
                    rule_str = rule_str + " a({0}),".format(abs(lit))
            else:
                if abs(lit) not in varset:
                    varset.add(abs(lit))
                if abs(lit) <= original_set_var:
                    rule_str = rule_str + " not v({0}),".format(abs(lit))
                else:
                    rule_str = rule_str + " not a({0}),".format(abs(lit))

        rule_str = rule_str[:-1] + "."  # end of rule
            
        
        # writing the rule 
        output_file_pointer.write(rule_str + "\n")
        asprin_file_pointer.write(rule_str + "\n")

# writing choice rules
rule_str = "{"
for index, atom in enumerate(list(varset)):
    if atom <= original_set_var:
        rule_str = rule_str + " v({0}) ;".format(atom)
    else:
        rule_str = rule_str + " a({0}) ;".format(atom)

rule_str = rule_str[:-1] + "}."  # end of rule
output_file_pointer.write(rule_str + "\n")
asprin_file_pointer.write(rule_str + "\n")
output_file_pointer.write("#heuristic v(X). [1, false]" + "\n")
asprin_file_pointer.write("#preference(p, subset) { v(X) }. #optimize(p)." + "\n")
output_file_pointer.write("#show v/1. \n")
asprin_file_pointer.write("#show v/1. \n")

file_pointer.close()
aspino_file_pointer.close()
minimal_file_pointer.close()
output_file_pointer.close()
asprin_file_pointer.close()

