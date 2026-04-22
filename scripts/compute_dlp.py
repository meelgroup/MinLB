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
        if line.startswith("p cnf"):
            l = line.split()
            output_file_pointer.write("%rule size: {0}\n".format(int(l[-1])))
            # print("The number of literals: {0} and clauses: {1} [Unpreprocessed]".format(l[-2], l[-1]))
        elif line.startswith("c ind"):
            # for some benchmarks (e.g., item mining), we can compute independent support easily
            # prepare independent support file
            IS_file = open("IS_dlp_" + file_name, 'w') 
            numbers = [int(x) for x in line.split()[2:] if int(x) != 0]
            IS_str = "c ind "
            for item in numbers:
                IS_str += "v{0} ".format(item)
            IS_str += "0\n"
            IS_file.write(IS_str)
            IS_file.close()
        elif line.startswith("c"):
            continue
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
# do preprocessing 
compute_disjunctive_program(file_name)
preprocess = True
original_set_var = None
original_set_clause = None
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
# output_file_pointer = open(output_file, 'w')
# grph = nx.Graph() 
# varset = set()
minimal_file_pointer = open("minimal_" + file_name , 'w')
for line in file_pointer:
    if line.startswith("c"):
        if line.startswith("c Number of clauses:"):
            l = line.split()
            print("The number of non-trivial clauses: {0}".format(l[-1]))
        continue
    elif line.startswith("p cnf"):
        l = line.split()
        # output_file_pointer.write("%rule size: {0}\n".format(int(l[-1])))
        minimal_file_pointer.write(line)
        minimal_file_pointer.write("c opt {0}\n".format(original_set_var))
        print("The number of literals: {0} and clauses: {1}".format(l[-2], l[-1]))
    else:
        # l = line.split()
        minimal_file_pointer.write(line)
        # lit_list = []
        # for lit in l:
        #     var = int(lit)
        #     if var != 0:
        #         lit_list.append(var)
            
        # rule_str = ":- "
        # node_lit = []
        # for index, lit in enumerate(lit_list):
        #     if lit < 0:
        #         if abs(lit) <= original_set_var:
        #             rule_str = rule_str + " v({0}),".format(abs(lit))
        #         else:
        #             rule_str = rule_str + " a({0}),".format(abs(lit))
        #     else:
        #         if abs(lit) not in varset:
        #             varset.add(abs(lit))
        #         if abs(lit) <= original_set_var:
        #             rule_str = rule_str + " not v({0}),".format(abs(lit))
        #         else:
        #             rule_str = rule_str + " not a({0}),".format(abs(lit))

        # rule_str = rule_str[:-1] + "."  # end of rule
            
        
        # writing the rule 
        # output_file_pointer.write(rule_str + "\n")

os.remove("prep_" + file_name)
# writing choice rules
# rule_str = "{"
# for index, atom in enumerate(list(varset)):
#     if atom <= original_set_var:
#         rule_str = rule_str + " v({0}) ;".format(atom)
#     else:
#         rule_str = rule_str + " a({0}) ;".format(atom)

# rule_str = rule_str[:-1] + "}."  # end of rule
# output_file_pointer.write(rule_str + "\n")
# output_file_pointer.write("#heuristic v(X). [1, false]" + "\n")
# output_file_pointer.write("#show v/1. \n")

file_pointer.close()
minimal_file_pointer.close()
# output_file_pointer.close()

