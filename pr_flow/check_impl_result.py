import os
from pr_flow.gen_basic import gen_basic

class check_impl_result(gen_basic):
  def __init__(self, prflow_params):
    gen_basic.__init__(self, prflow_params)

  # Depending on implementation results, it prints "Success" or "Fail"
  def run(self, operators):
    operator_list = operators.split()
    # print(operator_list)
    results_dict = {}
    for op in operator_list:
      if os.path.isfile(self.pr_dir + '/' + op + '/__success__'):
        results_dict[op] = 'Success'
      elif os.path.isfile(self.pr_dir + '/' + op + '/__timing_violation__'):
        results_dict[op] = 'Timing violation'
      elif os.path.isfile(self.pr_dir + '/' + op + '/__impl_failure__'):
        results_dict[op] = 'Implementation failed'


    failed_ops_list = []
    for op in results_dict:
      if results_dict[op] == 'Timing violation':
        # If there's at least one timing violation
        print('Timing')
        return
      elif results_dict[op] == 'Implementation failed':
        failed_ops_list.append(op)

    # If impl failed, return the ops that failed in implementation
    if len(failed_ops_list) == 0:
      print('Success')
    else:
      print(' '.join(failed_ops_list))

    # if all(results_list):
    #   print("Success") # If all impl runs succeeded
    # else:
    #   print("Timing") # If at least one impl runs failed