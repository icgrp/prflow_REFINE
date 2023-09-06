import os, argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--fail',help="default: fail=False",action='store_true')
    parser.add_argument('-m','--mono',help="default: mono=False",action='store_true')
    args = parser.parse_args()

    is_impl_failed = args.fail
    is_monolithic = args.mono 

    # impl_result_file = '_impl_result.txt'
    operator = os.path.basename(os.getcwd())

    # Noc ver.
    if not is_monolithic:
        if is_impl_failed:
            timing_rpt = [filename for filename in os.listdir('.') if filename.startswith("timing_") and filename.endswith(".rpt")]

            # At least it was successfully routed,
            if len(timing_rpt) == 1:
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
                    os.system('touch __timing_violation__')
                    print('--------------------------------')
                    print('## operator: ' + operator)
                    print('## result:   Timing violation')
                    print('--------------------------------')
                else:
                    os.system('touch __impl_failure__')
                    print('--------------------------------')
                    print('## operator: ' + operator)
                    print('## result:   Implementation failed')
                    print('--------------------------------')
            # If timing rpt is not available, it failed in previous implementation step
            else:
                os.system('touch __impl_failure__')
                print('--------------------------------')
                print('## operator: ' + operator)
                print('## result:   Implementation failed')
                print('--------------------------------')

        else:
            os.system('touch __success__')
            print('--------------------------------')
            print('## operator: ' + operator)
            print('## result:   Success')
            print('--------------------------------')

    # Monolithic ver.
    else:
        if os.path.isfile('./zcu102/package/sd_card/mono.xclbin'):
            os.system('touch __success__')
        else:
            if os.path.isfile('./zcu102/mono_impl/dr_routed_timing.dcp'):
                os.system('touch __timing_violation__')
            else:
                os.system('touch __impl_failure__')



if __name__ == '__main__':
    main()



