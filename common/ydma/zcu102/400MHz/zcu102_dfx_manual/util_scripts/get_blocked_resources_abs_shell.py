import os.path
# from natsort import natsorted
import math
import json

SLICEM_X_index_list=[1,4,5,7,10,11,13,14,16,19,20,22,25,26,28,29,31,34,\
                     35,37,40,41,43,44,46,49,50,52,53,55,56,58,61,62,64,67,\
                     68,70,73,74,76,77,79,82,85,87,88,90,91,93,96]

clockregion_resource_dict = {'X0Y3': ['{SLICE_X0Y180:SLICE_X28Y239}',\
                                      '{DSP48E2_X0Y72:DSP48E2_X5Y95}',\
                                      '{RAMB18_X0Y72:RAMB18_X3Y95}',\
                                      '{RAMB36_X0Y36:RAMB36_X3Y47}'],
                             'X0Y4': ['{SLICE_X0Y240:SLICE_X28Y299}',\
                                      '{DSP48E2_X0Y96:DSP48E2_X5Y119}',\
                                      '{RAMB18_X0Y96:RAMB18_X3Y119}',\
                                      '{RAMB36_X0Y48:RAMB36_X3Y59}'],
                             'X0Y5': ['{SLICE_X0Y300:SLICE_X28Y359}',\
                                      '{DSP48E2_X0Y120:DSP48E2_X5Y143}',\
                                      '{RAMB18_X0Y120:RAMB18_X3Y143}',\
                                      '{RAMB36_X0Y60:RAMB36_X3Y71}'],
                             'X0Y6': ['{SLICE_X0Y360:SLICE_X28Y419}',\
                                      '{DSP48E2_X0Y144:DSP48E2_X5Y167}',\
                                      '{RAMB18_X0Y144:RAMB18_X3Y167}',\
                                      '{RAMB36_X0Y72:RAMB36_X3Y83}']}
pblock_page_dict = {
            'p4': ['4','5','6','7'], 
            'p8': ['8','9','10','11'],
            'p12': ['12','13','14','15'],
            'p16': ['16','17','18','19'],
            'p20': ['20','21','22','23'],

            'p2': ['2','3'], 
            'p4_p0': ['4','5'], 'p4_p1': ['6','7'],
            'p8_p0': ['8','9'], 'p8_p1': ['10','11'], 
            'p12_p0': ['12','13'], 'p12_p1': ['14','15'], 
            'p16_p0': ['16','17'], 'p16_p1': ['18','19'],
            'p20_p0': ['20','21'], 'p20_p1': ['22','23'],

            'p2_p0': ['2'], 'p2_p1': ['3'],
            'p4_p1_p0': ['6'], 'p4_p1_p1': ['7'],
            'p8_p0_p0': ['8'], 'p8_p0_p1': ['9'], 'p8_p1_p0': ['10'], 'p8_p1_p1': ['11'],
            'p12_p0_p0': ['12'], 'p12_p0_p1': ['13'], 'p12_p1_p0': ['14'], 'p12_p1_p1': ['15'],
            'p16_p0_p0': ['16'], 'p16_p0_p1': ['17'], 'p16_p1_p0': ['18'], 'p16_p1_p1': ['19'],
            'p20_p0_p0': ['20'], 'p20_p0_p1': ['21'], 'p20_p1_p0': ['22'], 'p20_p1_p1': ['23']
}
clock_boundary_Y = {59, 60, 119, 120, 179, 180, 239, 240, 299, 300, 359, 360}

def is_in_range(range_list, loc):
    loc_x = int(loc.split('Y')[0].split('X')[1])
    loc_y = int(loc.split('Y')[1])
    for range_elem in range_list:
        [loc_s, loc_e] = range_elem.split(':')
        loc_s_x = int(loc_s.split('Y')[0].split('X')[1])
        loc_s_y = int(loc_s.split('Y')[1])
        loc_e_x = int(loc_e.split('Y')[0].split('X')[1])
        loc_e_y = int(loc_e.split('Y')[1])
        if((loc_s_x <= loc_x <= loc_e_x) and (loc_s_y <= loc_y <= loc_e_y)):
            return True
    return False

# returns 'SLICE' from ['SLICE_X33Y190:SLICE_X33Y239', 'SLICE_X16Y180:SLICE_X32Y239']
def get_resource_type(resource_range_list):
    return resource_range_list[0].split('_')[0] 

# returns 'X57Y185' from 'SLICE_X57Y185/GFF2' or
# returns 'X57Y185' from 'SLICE_X57Y185 \\'
def get_loc_tcl(line):
    if('/' in line):
        return line.split('/')[0].split('_')[1]
    else:
        return line.split('\\')[0].strip().split('_')[1]


# returns 'X28Y217/B' from ''SLICE_X28Y217/B6LUT \\''
def get_lut_loc(line):
    tile_loc = line.split('/')[0].split('_')[1]
    lut_idx = line.split('/')[1]
    lut_idx = lut_idx[0]
    return tile_loc + '/' + lut_idx


# returns [X33Y190:X33Y239, X16Y180:X32Y239] from {SLICE_X33Y190:SLICE_X33Y239 SLICE_X16Y180:SLICE_X32Y239}
def get_range_xdc(resource_range_list):
    range_list = []
    for range_elem in resource_range_list:
        [loc_s, loc_e] = range_elem.split(':')
        loc_s = loc_s.split('_')[1]
        loc_e = loc_e.split('_')[1]
        range_list.append(loc_s + ':' + loc_e)
    return range_list

def include_condition(line):
    # if(('CARRY8' in line) or ('MUX' in line) or ('FF' in line)):
    if(('CARRY8' in line) or ('MUX' in line)):
        return False
    else:
        return True

def pre_process(lines_raw):
    lines_processed = []
    lines_seen = set() # holds lines already seen
    for line in lines_raw:
        if (line not in lines_seen) and\
           (include_condition(line)) and\
           (not line.startswith('}]')) and\
           (not ' set mysites' in line) and\
           (not ' set mybels' in line) and\
           (not 'select_objects' in line):
            lines_processed.append(line)
            lines_seen.add(line)        
    return lines_processed

def update_seen_slice_loc_list(line, seen_lut_loc_list):
    lut_loc = get_lut_loc(line) # e.g. X16Y221/H
    # make sure that we don't double count 'SLICE_X16Y221/H5LUT' and 'SLICE_X16Y221/H6LUT
    if(lut_loc not in seen_lut_loc_list):
        seen_lut_loc_list.append(lut_loc)
    else:
        # print(lut_loc + ' is already in')
        pass


def update_seen_dsp_loc_list(line, seen_loc_list):
    loc = get_loc_tcl(line)
    # if one elem in DSP is blocked, then mark the DSP tile unavailable
    if(loc not in seen_loc_list):
        seen_loc_list.append(loc)

def update_seen_ram_loc_list(line, seen_loc_list):
    loc = get_loc_tcl(line)
    if(loc not in seen_loc_list):
        seen_loc_list.append(loc)


def gen_pblock_resource_dict(xdc_files):
    pblock_resource_dict = {}
    for xdc_file in xdc_files:        
        with open(xdc_file, 'r') as file:
            for line in file:
                if(line.startswith('create_pblock')):
                    pblock_name = line.split()[1]
                    # print(pblock_name)
                    if(pblock_name != 'p_bft' and pblock_name != 'p_NoC' and pblock_name != 'p_hier_0' and not pblock_name.endswith('_regs')):
                        pblock_resource_dict[pblock_name] = {}
                elif(line.startswith('resize_pblock')):
                    pblock_name = line.strip().split('-add ')[0].split('get_pblocks ')[1].split(']')[0]
                    if(pblock_name != 'p_bft' and pblock_name != 'p_NoC' and pblock_name != 'p_hier_0' and not pblock_name.endswith('_regs')):
                        resource_range_list = line.strip().split('-add ')[1].replace('{','').replace('}','').split()
                        # print(resource_range_list)
                        resource_type = get_resource_type(resource_range_list)
                        if(resource_type not in pblock_resource_dict[pblock_name]):
                            range_list = get_range_xdc(resource_range_list)
                            if resource_type == 'SLICE':
                                pblock_resource_dict[pblock_name]['SLICE_LUT'] = range_list
                                pblock_resource_dict[pblock_name]['SLICE_FF'] = range_list
                            else:
                                pblock_resource_dict[pblock_name][resource_type] = range_list
                        else:
                            range_list = get_range_xdc(resource_range_list)
                            if resource_type == 'SLICE':
                                pblock_resource_dict[pblock_name]['SLICE_LUT'] += range_list
                                pblock_resource_dict[pblock_name]['SLICE_FF'] += range_list
                            else:
                                pblock_resource_dict[pblock_name][resource_type] += range_list
                        # print(resource_type)
    return pblock_resource_dict

# e.g. returns ['X0Y3','X0Y4']
def get_clockregion_list(loc_s,loc_e):
    loc_s_x = int(loc_s.split('Y')[0].split('X')[1])
    loc_s_y = int(loc_s.split('Y')[1])
    loc_e_x = int(loc_e.split('Y')[0].split('X')[1])
    loc_e_y = int(loc_e.split('Y')[1])
    assert(loc_s_x == 0 and loc_e_x == 0)
    clockregion_list = []
    for idx in range(loc_s_y, loc_e_y+1):
        clockregion_list.append('X0Y'+str(idx))
    return clockregion_list

def get_clockregion_resources_lines(pblock_name, clockregion_list):
    new_lines = ''
    for clockregion in clockregion_list:
        new_resources = clockregion_resource_dict[clockregion]
        for elem in new_resources:
            new_lines += 'resize_pblock [get_pblocks ' + pblock_name + '] -add ' + elem + '\n'
    return new_lines

# changes CLOCKREGION into valid data elements in .xdc files
# Currently only supports CLOCKREGION_X0Y3 ~ CLOCKREGION_X0Y6
def pre_process_xdc(target_dir, xdc_dir, xdc_file):
    filedata = ''
    print_flag = False
    with open(xdc_dir + xdc_file, 'r') as file:
        for line in file:
            if(line.startswith('resize_pblock')):
                pblock_name = line.strip().split('-add ')[0].split('get_pblocks ')[1].split(']')[0]
                if(pblock_name != 'p_bft' and pblock_name != 'p_NoC' and pblock_name != 'p_hier_0' and not pblock_name.endswith('_regs')):
                    resource_range_list = line.strip().split('-add ')[1].replace('{','').replace('}','').split()
                    # print(resource_range_list)
                    resource_type = get_resource_type(resource_range_list)
                    if(resource_type == 'CLOCKREGION'):
                        # print(xdc_file)
                        print_flag = True
                        range_list = get_range_xdc(resource_range_list)
                        # TODO: For now, assume that something like 
                        # {CLOCKREGION_X0Y3:CLOCKREGION_X0Y3 CLOCKREGION_X0Y4:CLOCKREGION_X0Y4} does NOT exist
                        loc_s = range_list[0].split(':')[0]
                        loc_e = range_list[0].split(':')[1]
                        clockregion_list = get_clockregion_list(loc_s,loc_e)
                        # print(line)
                        # print(loc_s + ', ' + loc_e)
                        # print(clockregion_list)

                        new_lines = get_clockregion_resources_lines(pblock_name, clockregion_list)
                        line = new_lines
            filedata += line
    if(print_flag):
        # print("----FILE NAME: " + xdc_file)
        # print(filedata)
        pass

    with open(target_dir + xdc_file, "w") as file:
        file.write(filedata)

# returns the number of ramb18 sites whose parent ramb36 sites are NOT blocked
def get_num_ramb18_extra(blocked_resource_loc_dict, pblock_name):
    ramb36_list = blocked_resource_loc_dict[pblock_name]['RAMB36']
    ramb18_list = blocked_resource_loc_dict[pblock_name]['RAMB18']
    count = 0
    for ramb18_loc in ramb18_list:
        loc_x = int(ramb18_loc.split('Y')[0].split('X')[1])
        loc_y = int(ramb18_loc.split('Y')[1])
        ramb36_loc_x = loc_x
        ramb36_loc_y = int(math.floor(loc_y/2))
        ramb36_loc = 'X' + str(ramb36_loc_x) + 'Y' + str(ramb36_loc_y)
        if(ramb36_loc not in ramb36_list):
            count += 1
    return count



def main():

    xdc_dir = '../xdc/nested/'
    xdc_files = [f for f in os.listdir(xdc_dir) if f.endswith('.xdc')]
    # print(xdc_files)
    if(not os.path.isdir(xdc_dir + '_xdc')):
        os.mkdir(xdc_dir + '_xdc')
    for xdc_file in xdc_files:
        if(not os.path.isfile(xdc_dir + '_xdc/' + xdc_file)): 
            pre_process_xdc(xdc_dir + '_xdc/', xdc_dir, xdc_file)
        else:
            print("- Clock_region fixed ver. already exists")
            break
    xdc_files = [(xdc_dir + '_xdc/' + f) for f in os.listdir(xdc_dir + '_xdc/') if f.endswith('.xdc')]

    pblock_resource_dict = gen_pblock_resource_dict(xdc_files) # From xdc file, get resource range for each pblock
    print("- Get resource range for each pblock from xdc files")
    # e.g. {'p8_p0_p0': {'SLICE': ['SLICE_X0Y180:SLICE_X15Y239', 'SLICE_X33Y190:SLICE_X33Y239', 'SLICE_X16Y180:SLICE_X32Y239'], 
    #               'DSP48E2': ...]}}
    # for elem in pblock_resource_dict:
    #     # print(elem + ": ")
    #     # print(pblock_resource_dict[elem])
    #     resources = pblock_resource_dict[elem].keys()
    #     if 'SLICE' not in resources:
    #         print('SLICE not in')
    #     if 'DSP48E2' not in resources:
    #         print('DSP48E2 not in')
    #     if 'RAMB18' not in resources or 'RAMB36' not in resources:
    #         print('RAMb not in')
    # for pblock_name in pblock_resource_dict:
    #     print("####" + pblock_name)
    #     for resource_type in pblock_resource_dict[pblock_name]:
    #         print(resource_type)
    #         print(pblock_resource_dict[pblock_name][resource_type])


    # STEP 1 ############################################################################################################
    blocked_resource_dict = {}
    for pblock_name in pblock_resource_dict:
        blocked_resource_dict[pblock_name] = {}
        blocked_resource_dict[pblock_name]['SLICEL'] = []
        blocked_resource_dict[pblock_name]['SLICEM'] = []
        blocked_resource_dict[pblock_name]['SLICE_FF'] = []
        blocked_resource_dict[pblock_name]['DSP48E2'] = []
        blocked_resource_dict[pblock_name]['RAMB18'] = []
        blocked_resource_dict[pblock_name]['RAMB36'] = []
    # First, just based on XY value, add to blocked_resource_dict
    blocked_sites_file = '../hd_visual_dir/hd_visual_p20_p1/blockedSitesInputs.tcl' # "sites_file" is the same for all
    for pblock_name in pblock_resource_dict: 
        # Only care about blockedBelsOutputs.tcl from the pblock's abstrach shell
        blocked_file = './blocked_dir/' + pblock_name + '/hd_visual/blockedBelsOutputs.tcl'
        lines_raw = []
        if os.path.isfile(blocked_file):
            with open(blocked_file, 'r') as file:
                lines_raw = file.readlines()
        with open(blocked_sites_file, 'r') as file:
            lines_raw = lines_raw + file.readlines()
        lines_processed = pre_process(lines_raw) # remove unneccessary lines and unnecessary blocked resources like CARRY8, etc
        for line in lines_processed:
            line = line.strip()
            if(line.startswith('DSP48E2')):
                loc = get_loc_tcl(line)
                if(is_in_range(pblock_resource_dict[pblock_name]['DSP48E2'], loc)):
                        blocked_resource_dict[pblock_name]['DSP48E2'].append(line)
                        # blocked_resource_dict[pblock_name]['DSP48E2'].append(loc)

            elif(line.startswith('SLICE')):
                loc = get_loc_tcl(line) # returns 'X57Y185' from 'SLICE_X57Y185/GFF2' or
                loc_x = int(loc.split('Y')[0].split('X')[1])
                loc_y = int(loc.split('Y')[1])
                if(is_in_range(pblock_resource_dict[pblock_name]['SLICE_LUT'], loc) and
                    'FF' not in line and
                    loc_x not in SLICEM_X_index_list and 
                    loc_y not in clock_boundary_Y):
                    blocked_resource_dict[pblock_name]['SLICEL'].append(line)
                elif(is_in_range(pblock_resource_dict[pblock_name]['SLICE_LUT'], loc) and
                    'FF' not in line and
                    loc_x in SLICEM_X_index_list and # SLICEM 
                    loc_y not in clock_boundary_Y):
                    blocked_resource_dict[pblock_name]['SLICEM'].append(line)
                elif(is_in_range(pblock_resource_dict[pblock_name]['SLICE_LUT'], loc) and
                    'FF' in line and
                    loc_y not in clock_boundary_Y):
                    blocked_resource_dict[pblock_name]['SLICE_FF'].append(line)

            elif(line.startswith('RAMB18')):
                loc = get_loc_tcl(line)
                # print(loc)
                if(is_in_range(pblock_resource_dict[pblock_name]['RAMB18'], loc)):
                        blocked_resource_dict[pblock_name]['RAMB18'].append(line)
                        # blocked_resource_dict[pblock_name]['RAMB18'].append(loc)

            elif(line.startswith('RAMB36')):
                loc = get_loc_tcl(line)
                if(is_in_range(pblock_resource_dict[pblock_name]['RAMB36'], loc)):
                        blocked_resource_dict[pblock_name]['RAMB36'].append(line)
    # print(blocked_resource_dict)
    # e.g. {'p16_p0_p0': {'SLICE': ['SLICE_X16Y361/C5LUT \\', 'SLICE_X16Y361/CARRY8 \\',  ... ], 
    #                     'DSP48E2': ['DSP48E2_X3Y144/DSP_A_B_DATA \\', 'DSP48E2_X3Y144/DSP_C_DATA \\', ... ], 
    #                     'RAMB18': [ ... ], 
    #                     'RAMB36': [ ... ]}, 
    #       'p16_p0_p1': { ... }
    #       ... }

    print("- Added blocked resource to each pblock dict")
    # for pblock_name in blocked_resource_dict:
    #     print("####" + pblock_name)
    #     for resource_type in blocked_resource_dict[pblock_name]:
    #         print(resource_type)
    #         print(blocked_resource_dict[pblock_name][resource_type])
    #         print(len(blocked_resource_dict[pblock_name][resource_type]))


    # STEP 2 ############################################################################################################
    blocked_resource_loc_dict = {}
    for pblock_name in pblock_resource_dict:
        blocked_resource_loc_dict[pblock_name] = {}
        blocked_resource_loc_dict[pblock_name]['SLICEL'] = []
        blocked_resource_loc_dict[pblock_name]['SLICEM'] = []
        blocked_resource_loc_dict[pblock_name]['SLICE_FF'] = []
        blocked_resource_loc_dict[pblock_name]['DSP48E2'] = []
        blocked_resource_loc_dict[pblock_name]['RAMB18'] = []
        blocked_resource_loc_dict[pblock_name]['RAMB36'] = []

    # 'DSP48E2_X3Y144/DSP_A_B_DATA' and 'DSP48E2_X3Y144/DSP_C_DATA' are from a single DSP48E2.
    # So remove resources from "seen locations" in blocked_resource_dict
    for pblock_name in blocked_resource_dict:
        # print(pblock_name)
        for resource_type in blocked_resource_dict[pblock_name]:
            if(resource_type == 'SLICEL'):
                seen_lut_loc_list = []
                for line in blocked_resource_dict[pblock_name]['SLICEL']:
                    update_seen_slice_loc_list(line, seen_lut_loc_list)
                blocked_resource_loc_dict[pblock_name]['SLICEL'] = seen_lut_loc_list

            elif(resource_type == 'SLICEM'):
                seen_lut_loc_list = []
                for line in blocked_resource_dict[pblock_name]['SLICEM']:
                    update_seen_slice_loc_list(line, seen_lut_loc_list)
                blocked_resource_loc_dict[pblock_name]['SLICEM'] = seen_lut_loc_list

            elif(resource_type == 'SLICE_FF'): # nothing to do here
                blocked_resource_loc_dict[pblock_name]['SLICE_FF'] = blocked_resource_dict[pblock_name]['SLICE_FF']

            elif(resource_type == 'DSP48E2'):
                seen_loc_list = []
                for line in blocked_resource_dict[pblock_name]['DSP48E2']:
                    update_seen_dsp_loc_list(line, seen_loc_list)
                blocked_resource_loc_dict[pblock_name]['DSP48E2'] = seen_loc_list

            elif(resource_type == 'RAMB36'):
                seen_loc_list = []
                for line in blocked_resource_dict[pblock_name]['RAMB36']:
                    update_seen_ram_loc_list(line, seen_loc_list)
                blocked_resource_loc_dict[pblock_name]['RAMB36'] = seen_loc_list

            elif(resource_type == 'RAMB18'):
                seen_loc_list = []
                for line in blocked_resource_dict[pblock_name]['RAMB18']:
                    update_seen_ram_loc_list(line, seen_loc_list)
                blocked_resource_loc_dict[pblock_name]['RAMB18'] = seen_loc_list
    print("- Post-processed resources based on locations")
    # for pblock_name in blocked_resource_loc_dict.keys():
    # for pblock_name in ['p4_p0_p0']:
    #     print(pblock_name)
    #     for resource_type in blocked_resource_loc_dict[pblock_name]:
    #         # print(resource_type + ': ' + str(len(blocked_resource_loc_dict[pblock_name][resource_type])))
    #         print(resource_type)
    #         print(blocked_resource_loc_dict[pblock_name][resource_type])
    #         print(len(blocked_resource_loc_dict[pblock_name][resource_type]))
    #     print()


    # STEP 3 ############################################################################################################
    blocked_resource_count_dict = {}
    for pblock_name in pblock_resource_dict:
        blocked_resource_count_dict[pblock_name] = {}
        # blocked_resource_count_dict[pblock_name]['LUT'] = 0
        # blocked_resource_count_dict[pblock_name]['LUT_mem'] = 0
        # blocked_resource_count_dict[pblock_name]['FF'] = 0
        # blocked_resource_count_dict[pblock_name]['DSP48E2'] = 0
        # blocked_resource_count_dict[pblock_name]['RAMB18'] = 0
        # blocked_resource_count_dict[pblock_name]['RAMB36'] = 0

    # Count the number of blocked resources, RAMB is important!
    for pblock_name in blocked_resource_loc_dict.keys():
        blocked_resource_count_dict[pblock_name]['LUT']          = len(blocked_resource_loc_dict[pblock_name]['SLICEL']) +\
                                                                   len(blocked_resource_loc_dict[pblock_name]['SLICEM'])
        blocked_resource_count_dict[pblock_name]['LUT_mem']      = len(blocked_resource_loc_dict[pblock_name]['SLICEM'])
        blocked_resource_count_dict[pblock_name]['FF']           = len(blocked_resource_loc_dict[pblock_name]['SLICE_FF'])
        blocked_resource_count_dict[pblock_name]['DSP48E2']      = len(blocked_resource_loc_dict[pblock_name]['DSP48E2'])
        blocked_resource_count_dict[pblock_name]['RAMB36']       = len(blocked_resource_loc_dict[pblock_name]['RAMB36'])

        num_ramb18_extra = get_num_ramb18_extra(blocked_resource_loc_dict, pblock_name)
        blocked_resource_count_dict[pblock_name]['RAMB18_extra'] = num_ramb18_extra

        # print(pblock_name)
        # for resource_type in blocked_resource_loc_dict[pblock_name]:
        #     if(resource_type == 'SLICEL'):
        #         blocked_resource_count_dict[pblock_name]['LUT'] = len(blocked_resource_loc_dict[pblock_name]['SLICEL']) + 
        #                                                           len(blocked_resource_loc_dict[pblock_name]['SLICEM'])
        #     elif(resource_type == 'SLICEM'):
        #         blocked_resource_count_dict[pblock_name]['LUT_mem'] = len(blocked_resource_loc_dict[pblock_name][resource_type])
        #     elif(resource_type == 'SLICE_FF'):
        #         blocked_resource_count_dict[pblock_name]['FF'] = len(blocked_resource_loc_dict[pblock_name][resource_type])
        #     elif(resource_type == 'DSP48E2'):
        #         blocked_resource_count_dict[pblock_name]['DSP48E2'] = len(blocked_resource_loc_dict[pblock_name][resource_type])
        #     elif(resource_type == 'RAMB36'):
        #         blocked_resource_count_dict[pblock_name]['RAMB36'] = len(blocked_resource_loc_dict[pblock_name][resource_type])
        #     elif(resource_type == 'RAMB18'): # IMPORTANT!
        #         num_ramb18_extra = get_num_ramb18_extra(blocked_resource_loc_dict, pblock_name)
        #         blocked_resource_count_dict[pblock_name]['RAMB18_extra'] = num_ramb18_extra
    print("- Count blocked resources")
    # print(blocked_resource_count_dict)
    # {'p8_p0': {'SLICE_LUTs': 33, 'DSP48E2': 11, 'RAMB18_extra': 0, 'RAMB36': 0}, ... }
    # print(blocked_resource_count_dict['p16'])
    # print(blocked_resource_count_dict['p16_p1'])
    # print(blocked_resource_count_dict['p16_p1_p0'])
    # print('--------------------------------------------------')

    print(blocked_resource_count_dict)
    with open('blocked_util.json', 'w') as outfile:
        json.dump(blocked_resource_count_dict, outfile, sort_keys=True, indent=4) # json for human readable file


if __name__ == '__main__':
    main()
