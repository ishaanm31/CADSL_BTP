# Copyright (c) 2012-2013 ARM Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Copyright (c) 2006-2008 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Simple test script
#
# "m5 test.py"

import argparse
import sys
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.params import NULL
from m5.util import addToPath, fatal, warn
from gem5.isas import ISA
from gem5.runtime import get_runtime_isa

addToPath("../configs")

from ruby import Ruby

from common import Options
from common import Simulation
from common import CacheConfig
from common import CpuConfig
from common import ObjectList
from common import MemConfig
from common.FileSystemConfig import config_filesystem
from common.Caches import *
from common.cpu2000 import *

import spec06_benchmarks

def get_processes(args):
    """Interprets provided args and returns a list of processes"""

    multiprocesses = []
    inputs = []
    outputs = []
    errouts = []
    pargs = []

    workloads = args.cmd.split(";")
    if args.input != "":
        inputs = args.input.split(";")
    if args.output != "":
        outputs = args.output.split(";")
    if args.errout != "":
        errouts = args.errout.split(";")
    if args.options != "":
        pargs = args.options.split(";")

    idx = 0
    for wrkld in workloads:
        process = Process(pid=100 + idx)
        process.executable = wrkld
        process.cwd = os.getcwd()
        process.gid = os.getgid()

        if args.env:
            with open(args.env, "r") as f:
                process.env = [line.rstrip() for line in f]

        if len(pargs) > idx:
            process.cmd = [wrkld] + pargs[idx].split()
        else:
            process.cmd = [wrkld]

        if len(inputs) > idx:
            process.input = inputs[idx]
        if len(outputs) > idx:
            process.output = outputs[idx]
        if len(errouts) > idx:
            process.errout = errouts[idx]

        multiprocesses.append(process)
        idx += 1

    if args.smt:
        assert args.cpu_type == "DerivO3CPU"
        return multiprocesses, idx
    else:
        return multiprocesses, 1


parser = argparse.ArgumentParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

parser.add_argument(
    "-b", "--benchmark",
    type=str,
    default="",
    help="The SPEC benchmark to be loaded."
)
parser.add_argument(
    "--benchmark_stdout",
    type=str,
    default="",
    help="Absolute path for stdout redirection for the benchmark."
)
parser.add_argument(
    "--benchmark_stderr",
    type=str,
    default="",
    help="Absolute path for stderr redirection for the benchmark."
)
parser.add_argument(
    "--execMode",
    type=str,
    default=False,
    help="Execution Mode.",
)
parser.add_argument(
    "--issueInProgramOrder",
    type=bool,
    default=False,
    help="Issue instructions in program order.",
)
parser.add_argument(
    "--utilizeBranchHints",
    type=bool,
    default=False,
    help="Enable branch hint utilization.",
)
# Branch outcome file options
parser.add_argument(
    "--branch_outcome_file",
    type=str,
    default="",
    help="File containing Branch instruction PCs, Target Addresses and Branch direction.",
)

if "--ruby" in sys.argv:
    Ruby.define_options(parser)

args = parser.parse_args()

# multiprocesses = []
numThreads = 1

if args.benchmark:
    print('Selected SPEC_CPU2006 benchmark')
    if args.benchmark == 'perlbench':
        print('--> perlbench')
        process = spec06_benchmarks.perlbench
    elif args.benchmark == 'hello':
        print('--> hello')
        process = spec06_benchmarks.hello
    elif args.benchmark == 'bzip2':
        print('--> bzip2')
        process = spec06_benchmarks.bzip2
    elif args.benchmark == 'gcc':
        print('--> gcc')
        process = spec06_benchmarks.gcc
    elif args.benchmark == 'bwaves':
        print('--> bwaves')
        process = spec06_benchmarks.bwaves
    elif args.benchmark == 'gamess':
        print('--> gamess')
        process = spec06_benchmarks.gamess
    elif args.benchmark == 'mcf':
        print('--> mcf')
        process = spec06_benchmarks.mcf
    elif args.benchmark == 'milc':
        print('--> milc')
        process = spec06_benchmarks.milc
    elif args.benchmark == 'zeusmp':
        print('--> zeusmp')
        process = spec06_benchmarks.zeusmp
    elif args.benchmark == 'gromacs':
        print('--> gromacs')
        process = spec06_benchmarks.gromacs
    elif args.benchmark == 'cactusADM':
        print('--> cactusADM')
        process = spec06_benchmarks.cactusADM
    elif args.benchmark == 'leslie3d':
        print('--> leslie3d')
        process = spec06_benchmarks.leslie3d
    elif args.benchmark == 'namd':
        print('--> namd')
        process = spec06_benchmarks.namd
    elif args.benchmark == 'gobmk':
        print('--> gobmk')
        process = spec06_benchmarks.gobmk
    elif args.benchmark == 'dealII':
        print('--> dealII')
        process = spec06_benchmarks.dealII
    elif args.benchmark == 'soplex':
        print('--> soplex')
        process = spec06_benchmarks.soplex
    elif args.benchmark == 'povray':
        print('--> povray')
        process = spec06_benchmarks.povray
    elif args.benchmark == 'calculix':
        print('--> calculix')
        process = spec06_benchmarks.calculix
    elif args.benchmark == 'hmmer':
        print('--> hmmer')
        process = spec06_benchmarks.hmmer
    elif args.benchmark == 'sjeng':
        print('--> sjeng')
        process = spec06_benchmarks.sjeng
    elif args.benchmark == 'GemsFDTD':
        print('--> GemsFDTD')
        process = spec06_benchmarks.GemsFDTD
    elif args.benchmark == 'libquantum':
        print('--> libquantum')
        process = spec06_benchmarks.libquantum
    elif args.benchmark == 'h264ref':
        print('--> h264ref')
        process = spec06_benchmarks.h264ref
    elif args.benchmark == 'tonto':
        print('--> tonto')
        process = spec06_benchmarks.tonto
    elif args.benchmark == 'lbm':
        print('--> lbm')
        process = spec06_benchmarks.lbm
    elif args.benchmark == 'omnetpp':
        print('--> omnetpp')
        process = spec06_benchmarks.omnetpp
    elif args.benchmark == 'astar':
        print('--> astar')
        process = spec06_benchmarks.astar
    elif args.benchmark == 'wrf':
        print('--> wrf')
        process = spec06_benchmarks.wrf
    elif args.benchmark == 'sphinx3':
        print('--> sphinx3')
        process = spec06_benchmarks.sphinx3
    elif args.benchmark == 'Xalan':
        print('--> xalancbmk')
        process = spec06_benchmarks.Xalan
    elif args.benchmark == 'specrand_i':
        print('--> specrand_i')
        process = spec06_benchmarks.specrand_i
    elif args.benchmark == 'specrand_f':
        print('--> specrand_f')
        process = spec06_benchmarks.specrand_f
    # elif args.benchmark == 'gobmk_base.armv7-gcc':
    #     print('--> gobmk_base.armv7-gcc')
    #     process = spec06_benchmarks.gobmk
    else:
        print("No recognized SPEC2006 benchmark selected! Exiting.")
        sys.exit(1)
else:
    print("Need --benchmark switch to specify SPEC CPU2006 workload. Exiting!\n")
    sys.exit(1)

# Set process stdout/stderr
if args.benchmark_stdout:
    process.output = args.benchmark_stdout
    print("Process stdout file: " + process.output)
if args.benchmark_stderr:
    process.errout = args.benchmark_stderr
    print("Process stderr file: " + process.errout)

# if args.bench:
#     apps = args.bench.split("-")
#     if len(apps) != args.num_cpus:
#         print("number of benchmarks not equal to set num_cpus!")
#         sys.exit(1)

#     for app in apps:
#         try:
#             if get_runtime_isa() == ISA.ARM:
#                 exec(
#                     "workload = %s('arm_%s', 'linux', '%s')"
#                     % (app, args.arm_iset, args.spec_input)
#                 )
#             else:
#                 # TARGET_ISA has been removed, but this is missing a ], so it
#                 # has incorrect syntax and wasn't being used anyway.
#                 exec(
#                     "workload = %s(buildEnv['TARGET_ISA', 'linux', '%s')"
#                     % (app, args.spec_input)
#                 )
#             multiprocesses.append(workload.makeProcess())
#         except:
#             print(
#                 "Unable to find workload for %s: %s"
#                 % (get_runtime_isa().name(), app),
#                 file=sys.stderr,
#             )
#             sys.exit(1)
# elif args.cmd:
#     multiprocesses, numThreads = get_processes(args)
# else:
#     print("No workload specified. Exiting!\n", file=sys.stderr)
#     sys.exit(1)


(CPUClass, test_mem_mode, FutureClass) = Simulation.setCPUClass(args)
CPUClass.numThreads = numThreads

# Check -- do not allow SMT with multiple CPUs
if args.smt and args.num_cpus > 1:
    fatal("You cannot use SMT with multiple CPUs!")

np = args.num_cpus
# mp0_path = multiprocesses[0].executable
system = System(
    cpu=[CPUClass(cpu_id=i) for i in range(np)],
    mem_mode=test_mem_mode,
    mem_ranges=[AddrRange(args.mem_size)],
    cache_line_size=args.cacheline_size,
)

if numThreads > 1:
    system.multi_thread = True

# Create a top-level voltage domain
system.voltage_domain = VoltageDomain(voltage=args.sys_voltage)

# Create a source clock for the system and set the clock period
system.clk_domain = SrcClockDomain(
    clock=args.sys_clock, voltage_domain=system.voltage_domain
)

# Create a CPU voltage domain
system.cpu_voltage_domain = VoltageDomain()

# Create a separate clock domain for the CPUs
system.cpu_clk_domain = SrcClockDomain(
    clock=args.cpu_clock, voltage_domain=system.cpu_voltage_domain
)

# If elastic tracing is enabled, then configure the cpu and attach the elastic
# trace probe
if args.elastic_trace_en:
    CpuConfig.config_etrace(CPUClass, system.cpu, args)

# All cpus belong to a common cpu_clk_domain, therefore running at a common
# frequency.
for cpu in system.cpu:
    cpu.clk_domain = system.cpu_clk_domain

if ObjectList.is_kvm_cpu(CPUClass) or ObjectList.is_kvm_cpu(FutureClass):
    if buildEnv["USE_X86_ISA"]:
        system.kvm_vm = KvmVM()
        system.m5ops_base = 0xFFFF0000
        for process in multiprocesses:
            process.useArchPT = True
            process.kvmInSE = True
    else:
        fatal("KvmCPU can only be used in SE mode with x86")

# Sanity check
if args.simpoint_profile:
    if not ObjectList.is_noncaching_cpu(CPUClass):
        fatal("SimPoint/BPProbe should be done with an atomic cpu")
    if np > 1:
        fatal("SimPoint generation not supported with more than one CPUs")

# for i in range(np):
#     if args.smt:
#         system.cpu[i].workload = multiprocesses
#     elif len(multiprocesses) == 1:
#         system.cpu[i].workload = multiprocesses[0]
#     else:
#         system.cpu[i].workload = multiprocesses[i]

#     if args.simpoint_profile:
#         system.cpu[i].addSimPointProbe(args.simpoint_interval)

#     if args.checker:
#         system.cpu[i].addCheckerCpu()

#     if args.bp_type:
#         bpClass = ObjectList.bp_list.get(args.bp_type)
#         system.cpu[i].branchPred = bpClass()

#     if args.indirect_bp_type:
#         indirectBPClass = ObjectList.indirect_bp_list.get(
#             args.indirect_bp_type
#         )
#         system.cpu[i].branchPred.indirectBranchPred = indirectBPClass()

#     system.cpu[i].createThreads()

if args.ruby:
    Ruby.create_system(args, False, system)
    assert args.num_cpus == len(system.ruby._cpu_ports)

    system.ruby.clk_domain = SrcClockDomain(
        clock=args.ruby_clock, voltage_domain=system.voltage_domain
    )
    for i in range(np):
        ruby_port = system.ruby._cpu_ports[i]

        # Create the interrupt controller and connect its ports to Ruby
        # Note that the interrupt controller is always present but only
        # in x86 does it have message ports that need to be connected
        system.cpu[i].createInterruptController()

        # Connect the cpu's cache ports to Ruby
        ruby_port.connectCpuPorts(system.cpu[i])
else:
    MemClass = Simulation.setMemClass(args)
    system.membus = SystemXBar()
    system.system_port = system.membus.cpu_side_ports
    CacheConfig.config_cache(args, system)
    MemConfig.config_mem(args, system)
    config_filesystem(system, args)

for i in range(np): 
    system.cpu[i].workload = process
    system.cpu[i].createThreads()
    print(process.cmd)

    # if args.cpu_type in ["DerivO3CPU"]:
    if system.cpu[i].type in ["BaseO3CPU"]:
        system.cpu[i].issueInProgramOrder=args.issueInProgramOrder
        system.cpu[i].branchOutcomeFile=args.branch_outcome_file
        system.cpu[i].utilizeBranchHints=args.utilizeBranchHints

        if args.execMode in ["OoO"]:
            system.cpu[i].fetchWidth=8
            system.cpu[i].fetchBufferSize=64
            system.cpu[i].fetchQueueSize=32
            system.cpu[i].decodeWidth=8
            system.cpu[i].renameWidth=8
            system.cpu[i].dispatchWidth=8
            system.cpu[i].issueWidth=8
            system.cpu[i].wbWidth=8
            system.cpu[i].fuPool=DefaultFUPool()
            system.cpu[i].commitWidth=8
            system.cpu[i].squashWidth=8
            system.cpu[i].LQEntries=32
            system.cpu[i].SQEntries=32
            system.cpu[i].numPhysIntRegs=256
            system.cpu[i].numPhysFloatRegs=256
            system.cpu[i].numIQEntries=64
            system.cpu[i].numROBEntries=192
        elif args.execMode in ["OoOasInO"]:
            system.cpu[i].fetchWidth=2
            system.cpu[i].fetchBufferSize=64
            system.cpu[i].fetchQueueSize=2
            system.cpu[i].decodeWidth=2
            system.cpu[i].renameWidth=2
            system.cpu[i].dispatchWidth=2
            system.cpu[i].issueWidth=2
            system.cpu[i].wbWidth=2
            system.cpu[i].fuPool=CustomFUPool()
            system.cpu[i].commitWidth=2
            system.cpu[i].squashWidth=2
            system.cpu[i].LQEntries=7
            system.cpu[i].SQEntries=7
            system.cpu[i].numPhysIntRegs=128
            system.cpu[i].numPhysFloatRegs=128
            system.cpu[i].numIQEntries=7
            system.cpu[i].numROBEntries=7
        else:
            print('Unsupported Execution Mode for O3CPU')

system.l2.size='256kB'
system.l2.assoc=8
system.l2.tag_latency=9
system.l2.data_latency=9
system.l2.response_latency=9
system.l2.mshrs=32
system.l2.prefetcher=BOPPrefetcher()

system.workload = SEWorkload.init_compatible(process.executable)

if args.wait_gdb:
    system.workload.wait_for_remote_gdb = True

root = Root(full_system=False, system=system)
Simulation.run(args, root, system, FutureClass)
