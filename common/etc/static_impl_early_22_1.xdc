# Copyright 2021 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Clock domain priority
# ------------------------------------------------------------------------------
set_property HIGH_PRIORITY true [get_nets pfm_top_i/static_region/base_clocking/clkwiz_sysclks/inst/clk_out1]
set_property HIGH_PRIORITY true [get_nets pfm_top_i/static_region/base_clocking/clkwiz_sysclks/inst/clk_out2]

# Additional timing constraints
# ------------------------------------------------------------------------------

# Programmable clock delay
create_property MAX_PROG_DELAY net

# Configuration
# ------------------------------------------------------------------------------
set_property CONFIG_VOLTAGE 1.8                        [current_design]
set_property BITSTREAM.CONFIG.CONFIGFALLBACK Enable    [current_design]
set_property BITSTREAM.GENERAL.COMPRESS TRUE           [current_design]
####set_property CONFIG_MODE SPIx4                         [current_design]
####set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4           [current_design]
set_property BITSTREAM.CONFIG.EXTMASTERCCLK_EN disable [current_design]
####set_property BITSTREAM.CONFIG.CONFIGRATE 85.0          [current_design]
####set_property BITSTREAM.CONFIG.SPI_FALL_EDGE YES        [current_design]
set_property BITSTREAM.CONFIG.UNUSEDPIN Pullup         [current_design]
####set_property BITSTREAM.CONFIG.SPI_32BIT_ADDR Yes       [current_design]

# IO constraints
# ------------------------------------------------------------------------------

# Floorplanning
# ------------------------------------------------------------------------------
set_property DONT_TOUCH true [get_cells pfm_top_i/dynamic_region]
set_property HD.RECONFIGURABLE true [get_cells pfm_top_i/dynamic_region]

# Dynamic region pblock, modified by dopark
create_pblock pblock_dynamic_region
add_cells_to_pblock [get_pblocks pblock_dynamic_region] [get_cells -quiet [list pfm_top_i/dynamic_region]]

resize_pblock [get_pblocks pblock_dynamic_region] -add {SLICE_X41Y120:SLICE_X95Y179 SLICE_X87Y60:SLICE_X95Y119 SLICE_X77Y60:SLICE_X84Y119 SLICE_X41Y60:SLICE_X55Y119 SLICE_X41Y0:SLICE_X95Y59}
resize_pblock [get_pblocks pblock_dynamic_region] -add {CFGIO_SITE_X0Y0:CFGIO_SITE_X0Y0}
resize_pblock [get_pblocks pblock_dynamic_region] -add {DSP48E2_X16Y0:DSP48E2_X17Y71 DSP48E2_X12Y48:DSP48E2_X15Y71 DSP48E2_X12Y0:DSP48E2_X15Y23 DSP48E2_X8Y0:DSP48E2_X11Y71}
resize_pblock [get_pblocks pblock_dynamic_region] -add {IOB_X0Y0:IOB_X0Y37}
resize_pblock [get_pblocks pblock_dynamic_region] -add {RAMB18_X10Y0:RAMB18_X12Y71 RAMB18_X7Y48:RAMB18_X9Y71 RAMB18_X7Y0:RAMB18_X9Y23 RAMB18_X6Y0:RAMB18_X6Y71}
resize_pblock [get_pblocks pblock_dynamic_region] -add {RAMB36_X10Y0:RAMB36_X12Y35 RAMB36_X7Y24:RAMB36_X9Y35 RAMB36_X7Y0:RAMB36_X9Y11 RAMB36_X6Y0:RAMB36_X6Y35}
resize_pblock [get_pblocks pblock_dynamic_region] -add {SYSMONE4_X0Y0:SYSMONE4_X0Y0}
resize_pblock [get_pblocks pblock_dynamic_region] -add {CLOCKREGION_X0Y3:CLOCKREGION_X3Y6 CLOCKREGION_X2Y1:CLOCKREGION_X2Y1}
set_property SNAPPING_MODE ON [get_pblocks pblock_dynamic_region]





#To avoid placement of static cells in the island to help with timing enclosure
set_property PROHIBIT 1  [get_sites -range SLICE_X85Y60:SLICE_X86Y119]
set_property PROHIBIT 1  [get_sites -range SLICE_X96Y0:SLICE_X96Y179]

#revert back to original instance
current_instance -quiet
