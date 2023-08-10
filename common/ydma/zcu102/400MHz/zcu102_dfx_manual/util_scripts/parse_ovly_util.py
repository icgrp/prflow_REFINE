import os
# import pickle
import json

# e.g.: returns 'p2_p0' from 'utilization_p2_p0.rpt'
def get_n_rpt(rpt_file):
	return (rpt_file.split('utilization_')[1]).split('.')[0]

def main():
	# rpt_files = [f for f in os.listdir('.') if f.endswith('.rpt')]
	# # print(rpt_files)
	# n = len(rpt_files) + 1 # returns 10 when overlay_p10
	# # print(n)
	# rpt_files = ['utilization'+ str(i) +'.rpt' for i in range(2,n+1)] # sorted

	rpt_files = [f for f in os.listdir('.') if f.endswith('.rpt')]
	# print(rpt_files)
	# filedata=''
	util_dict = {}
	(num_lut, num_lut_mem, num_ff, num_ram36, num_ram18, num_dsp) = (0, 0, 0, 0, 0, 0)	
	for rpt_file in rpt_files:
		with open(rpt_file, 'r') as file:
			is_reg_done = False # there exist two | CLB Registers
			for line in file:
				if(line.startswith('| CLB LUTs')):
					num_lut = int(line.split()[16]) # 16 is magic number for "Available"
				elif(line.startswith('|   LUT as Memory')):
					num_lut_mem = int(line.split()[17]) # 17 is magic number for "Available"
				elif(line.startswith('| CLB Registers') and not is_reg_done):
					is_reg_done = True
					num_ff = int(line.split()[16]) # 16 is magic number for "Available"
					# print(line.split()[16]) # 16 is magic number for "Available"
				elif(line.startswith('|   RAMB36')):
					num_ram36 = int(line.split()[15]) # 15 is magic number for "Available"
					# print(line.split()[15]) # 15 is magic number for "Available"
				elif(line.startswith('|   RAMB18')):
					num_ram18 = int(line.split()[15]) # 15 is magic number for "Available"
					# print(line.split()[15]) # 15 is magic number for "Available"
				elif(line.startswith('| DSPs')):
					num_dsp = int(line.split()[15]) # 15 is magic number for "Available"
					# print(line.split()[15]) # 15 is magic number for "Available"

				# prohibited
				if(line.startswith('| CLB   ') and is_reg_done):
					num_prohibited_lut = int(line.split()[13])
					# num_lut = num_lut - num_prohibited_lut*8 # THIS IS ALREADY TAKEN INTO ACCOUNT IN UTIL REPORT
					num_ff = num_ff - num_prohibited_lut*16 # DJP: I think if Slice site is prohibited, FF has to be prohibited too
					# print(rpt_file)
					# print(num_ff)

		util_dict[get_n_rpt(rpt_file)] = {'LUT': num_lut,
										  'LUT_mem': num_lut_mem,
										  'FF': num_ff,
										  'RAMB36': num_ram36,
										  'RAMB18': num_ram18,
										  'DSP48E2': num_dsp}
		# (num_lut_logic, num_lut_mem, num_ff, num_ram36, num_ram18, num_dsp)
		# filedata = filedata + rpt_file + ': ' + str((num_clb, num_ram36, num_ram18, num_dsp)) + '\n'

	# print(util_dict)
	# print(len(util_dict))
	with open('util_all_pre_blocked.json', 'w') as outfile:
		json.dump(util_dict, outfile, sort_keys=True, indent=4)


	with open('blocked_util.json', 'r') as infile:
		blocked_resource_count_dict = json.load(infile)
	# print(blocked_resource_count_dict)

	for pblock_name in util_dict:
		num_blocked_lut = blocked_resource_count_dict[pblock_name]['LUT']
		num_blocked_lut_mem = blocked_resource_count_dict[pblock_name]['LUT_mem']
		num_blocked_ff = blocked_resource_count_dict[pblock_name]['FF']
		num_blocked_ram36 = blocked_resource_count_dict[pblock_name]['RAMB36']
		num_blocked_ram18_extra = blocked_resource_count_dict[pblock_name]['RAMB18_extra']
		num_blocked_dsp = blocked_resource_count_dict[pblock_name]['DSP48E2']

		num_lut = util_dict[pblock_name]['LUT'] - int(num_blocked_lut)
		num_lut_mem = util_dict[pblock_name]['LUT_mem'] - int(num_blocked_lut_mem)
		num_ff = util_dict[pblock_name]['FF'] - int(num_blocked_ff)
		num_ram36 = util_dict[pblock_name]['RAMB36'] - int(num_blocked_ram36)
		num_ram18 = util_dict[pblock_name]['RAMB18'] - int(num_blocked_ram36)*2 - int(num_blocked_ram18_extra)
		num_dsp = util_dict[pblock_name]['DSP48E2'] - int(num_blocked_dsp)

		# util_dict[pblock_name] = (num_lut_logic, num_lut_mem, num_ff, num_ram36, num_ram18, num_dsp) 
		# rewrite util_dict reflecting blocked resources
		util_dict[pblock_name] = {'LUT': num_lut,
								  'LUT_mem': num_lut_mem,
								  'FF': num_ff,
								  'RAMB36': num_ram36,
								  'RAMB18': num_ram18,
								  'DSP48E2': num_dsp}
	print(util_dict)
	with open('util_all.json', 'w') as outfile:
		json.dump(util_dict, outfile, sort_keys=True, indent=4)

if __name__ == '__main__':
	main()
