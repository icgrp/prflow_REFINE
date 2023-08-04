import sys, json, argparse
parser = argparse.ArgumentParser()
parser.add_argument('-prj',       '--project_name',        help="operators directory")
args = parser.parse_args()


def get_num_op(operator):
    return len(operator.split())

def main():
    project_name = args.project_name
    pblock_ops_dir = './input_src/' + project_name + '/operators'
    with open(pblock_ops_dir + '/kernel_clk.json', 'r') as infile:
        # pblock_operators_list = json.load(infile)
        pblock_operators_dict = json.load(infile)
    pblock_operators_list = pblock_operators_dict.keys()
    operators_impl = ''
    for pblock_op in pblock_operators_list:
        if(get_num_op(pblock_op)==1):
            operators_impl = operators_impl + " " + pblock_op
        else:
            pblock_op = pblock_op.split()[0] # only the first operator as representative op
            operators_impl = operators_impl + " " + pblock_op            
    operators_impl_sorted = '' # for debugging
    operators_impl = sorted(operators_impl.split())
    for op in operators_impl:
        operators_impl_sorted = operators_impl_sorted + " " + op
    print(operators_impl_sorted)


if __name__ == '__main__':
    main()