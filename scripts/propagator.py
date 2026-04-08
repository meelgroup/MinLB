import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i','--i', help='input trasaction file', required=True)
parser.add_argument('-t','--t', help='timeout', required=False)
args = parser.parse_args()

file_name = args.i
union_of_items = set()
ntransaction = 0
nitems = 0
for line in open(file_name):
    if len(line) > 0:
        l = line.rstrip().split()
        l = [int(_) for _ in l]
        union_of_items = union_of_items.union(set(l))
        ntransaction += 1

print("Number of items: {0} number of transaction: {1}".format(len(union_of_items), ntransaction))
variable_transaction_map = dict()
transaction_items = []

transaction_id = 1
for line in open(file_name):
    if len(line) > 0:
        l = line.rstrip().split()
        l = [int(_) for _ in l]
        absent_items = union_of_items - set(l)
        transaction_items.append(absent_items)
        for _ in absent_items:
            if _ not in variable_transaction_map:
                variable_transaction_map[_] = [transaction_id]
            else:
                variable_transaction_map[_].append(transaction_id)
        
        transaction_id += 1

asp_file_name = "dlp_" + file_name
IS_file_name = "IS_dlp_" + file_name
cut_file_name = "minimal_" + file_name
asp_file = open(asp_file_name, 'w')
IS_file = open(IS_file_name, 'w')
cut_file = open(cut_file_name, 'w')
cut_str = "p cnf {0} {1}\n".format(int(max(union_of_items)) + transaction_id - 1, transaction_id - 1)
cut_file.write(cut_str)
transaction_id = int(max(union_of_items))

for index, transaction in enumerate(transaction_items):
    rule_str = "t({0})".format(index + 1)
    clause_str = "{0} ".format(transaction_id + index + 1)
    if len(transaction_items) > 0:
        rule_str += "".join("; i(" + str(_) + ")" for _ in transaction)
        clause_str += "".join(str(_) + " " for _ in transaction)
    rule_str += ".\n"
    clause_str += "0\n"
    asp_file.write(rule_str)
    cut_file.write(clause_str)


IS_str = "c ind "
for item in union_of_items:
    IS_str += "i({0}) ".format(item)
IS_str += "0\n"
IS_file.write(IS_str)
IS_file.close()
asp_file.close()
cut_file.close()

# ctl.load(asp_file_name)
# ctl.ground([("base", [])])
# small_time = 10
# nModel = 0
# with ctl.solve(yield_=True, async_=True) as hnd:
#     while True:
#         hnd.resume()
#         hnd.wait(small_time)
#         # some computation here
#         _ = hnd.wait()
#         m = hnd.model()
#         if m is None:
#             break
#         else:
#             nModel += 1
# print("[ASP] Number of minimal generators: {0}".format(nModel))