import os

# files = [f for f in os.listdir('./' if isfile(f))]

# filelist = [] 
# for f in os.listdir('./'):
#     if(not f.endswith('.swp')):
#         filelist.append(f)

# for f in filelist:
#     command = 'diff '
#     command = command + f
#     diff_f = '/home/dopark/icgrid/simple_sim/v_src/pure_verilog/' + f
#     if(os.path.exists(diff_f)):
#         command = command + ' ' + diff_f
#         print("#########################################")
#         print("#### file name: " + f)
#         print("#########################################")
#         os.system(command)
#         print("")

except_list = ['bft.v', 'test.v']

# filelist = [] 
# for f in os.listdir('./'):
#     if(not f.endswith('.swp')):
#         filelist.append(f)

filelist = [ 'Config_Controls.v', 'rise_detect.v',         'converge_ctrl.v',
              'ExtractCtrl.v',     'Input_Port_Cluster.v',  'Input_Port.v',          'leaf_interface.v',   'Output_Port_Cluster.v',
              'Output_Port.v',     'read_b_in.v',           'ram0.v',                'single_ram.v',       'SynFIFO.v',
              'xram_triple.v',     'Stream_Flow_Control.v', 'write_b_in.v',          'write_b_out.v',
              'stream_shell.v',    'expand_queue.v',        'shrink_queue.v',        'send_IO_queue_cnt.v']

for f in filelist:
    command = 'diff '
    command = command + './workspace/F001_overlay/src/' + f
    diff_f = '/home/dopark/workspace/simulation_dir_22_1/af_rendering_is_done_sim_src/v_src/pure_verilog/' + f
    if(os.path.exists(diff_f) and f not in except_list):
        command = command + ' ' + diff_f
        print("#########################################")
        print("#### file name: " + f)
        print("#########################################")
        os.system(command)
        print("")