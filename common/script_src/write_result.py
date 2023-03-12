import os, argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--fail',help="default: fail=False",action='store_true')
    args = parser.parse_args()

    is_impl_failed = args.fail
    impl_result_file = '_impl_result.txt'
    operator = os.path.basename(os.getcwd())
    if is_impl_failed:
        with open(impl_result_file, 'w') as infile:
            infile.write('Implementation failed')
            print('--------------------------------')
            print('## operator: ' + operator)
            print('## result:   Implementation failed')
            print('--------------------------------')
    else:
        timing_rpt = [filename for filename in os.listdir('.') if filename.startswith("timing_") and filename.endswith(".rpt")]
        assert(len(timing_rpt) == 1)
        timing_rpt = timing_rpt[0]
        with open(timing_rpt, 'r') as infile:
            find_summary_flag = False
            line_offset = 0
            for line in infile:
                if 'Design Timing Summary' in line:
                    find_summary_flag = True
                if find_summary_flag:
                    line_offset += 1
                if line_offset == 7:
                    timing_list =  line.split()
                    WNS = float(timing_list[0])

        # Check timing violation
        if WNS < 0:
            with open(impl_result_file, 'w') as infile:
                infile.write('Timing violation')
                print('--------------------------------')
                print('## operator: ' + operator)
                print('## result:   Timing violation')
                print('--------------------------------')
        else:
            with open(impl_result_file, 'w') as infile:
                infile.write('Success')
                print('--------------------------------')
                print('## operator: ' + operator)
                print('## result:   Success')
                print('--------------------------------')


if __name__ == '__main__':
    main()



