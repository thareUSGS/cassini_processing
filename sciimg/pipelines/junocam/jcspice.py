import spiceypy as spice
import sys
import os
import glob

def load_kernels(kernelbase, allow_predicted=False):
    kernels = [
        "%s/juno/kernels/pck/pck00010.tpc"%kernelbase,
        "%s/juno/kernels/fk/juno_v12.tf"%kernelbase,
        "%s/juno/kernels/ik/juno_junocam_v03.ti"%kernelbase,
        "%s/juno/kernels/lsk/naif0012.tls"%kernelbase,
        "%s/juno/kernels/sclk/jno_sclkscet_00094.tsc"%kernelbase,
        "%s/juno/kernels/tspk/de436s.bsp"%kernelbase,
        "%s/juno/kernels/tspk/jup365.bsp"%kernelbase,
        "%s/juno/kernels/tspk/de440s.bsp"%kernelbase,
        "%s/juno/kernels/tspk/jup310.bsp"%kernelbase,
        "%s/juno/kernels/spk/jup380s.bsp"%kernelbase,
        "%s/juno/kernels/spk/juno_struct_v04.bsp"%kernelbase
    ]


    kernel_prefix = "spk_rec_" if not allow_predicted else "spk_pre_"
    for file in glob.glob("%s/juno/kernels/spk/%s*bsp"%(kernelbase, kernel_prefix)):
        kernels.append(file)
    kernels.append("/home/kevinmgill/anaconda3/envs/isis3/data/juno/kernels/spk/spk_pre_201231_210720_210407_otm33_f.bsp")
    #kernels = ["/home/kevinmgill/anaconda3/envs/isis3/data/juno/kernels/spk/spk_pre_201231_210720_210407_otm33_f.bsp"]
    kernel_prefix = "juno_sc_rec_" if not allow_predicted else ""
    for file in glob.glob("%s/juno/kernels/ck/%s*bc"%(kernelbase, kernel_prefix)):
        kernels.append(file)

    for kernel in kernels:
        spice.furnsh(kernel)
