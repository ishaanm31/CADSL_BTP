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

from importlib import reload
import spec06_benchmarks

# def get_processes(args):
#     """Interprets provided args and returns a list of processes"""

#     multiprocesses = []
#     inputs = []
#     outputs = []
#     errouts = []
#     pargs = []

#     workloads = args.cmd.split(";")
#     if args.input != "":
#         inputs = args.input.split(";")
#     if args.output != "":
#         outputs = args.output.split(";")
#     if args.errout != "":
#         errouts = args.errout.split(";")
#     if args.options != "":
#         pargs = args.options.split(";")

#     idx = 0
#     for wrkld in workloads:
#         process = Process(pid=100 + idx)
#         process.executable = wrkld
#         process.cwd = os.getcwd()
#         process.gid = os.getgid()

#         if args.env:
#             with open(args.env, "r") as f:
#                 process.env = [line.rstrip() for line in f]

#         if len(pargs) > idx:
#             process.cmd = [wrkld] + pargs[idx].split()
#         else:
#             process.cmd = [wrkld]

#         if len(inputs) > idx:
#             process.input = inputs[idx]
#         if len(outputs) > idx:
#             process.output = outputs[idx]
#         if len(errouts) > idx:
#             process.errout = errouts[idx]

#         multiprocesses.append(process)
#         idx += 1

#     if args.smt:
#         assert args.cpu_type == "DerivO3CPU"
#         return multiprocesses, idx
#     else:
#         return multiprocesses, 1


parser = argparse.ArgumentParser()
Options.addCommonOptions(parser)
Options.addSEOptions(parser)

parser.add_argument(
    "-b1", "--benchmark1",
    type=str,
    default="",
    help="The SPEC benchmark1 to be loaded."
)
parser.add_argument(
    "-b2", "--benchmark2",
    type=str,
    default="",
    help="The SPEC benchmark2 to be loaded."
)
parser.add_argument(
    "--benchmark1_stdout",
    type=str,
    default="",
    help="Absolute path for stdout redirection for the benchmark1."
)
parser.add_argument(
    "--benchmark2_stdout",
    type=str,
    default="",
    help="Absolute path for stdout redirection for the benchmark2."
)
parser.add_argument(
    "--benchmark1_stderr",
    type=str,
    default="",
    help="Absolute path for stderr redirection for the benchmark1."
)
parser.add_argument(
    "--benchmark2_stderr",
    type=str,
    default="",
    help="Absolute path for stderr redirection for the benchmark2."
)

if "--ruby" in sys.argv:
    Ruby.define_options(parser)

args = parser.parse_args()

# multiprocesses = []
numThreads = 1

if args.benchmark1:
    print('Selected SPEC_CPU2006 benchmark1')
    if args.benchmark1 == 'perlbench':
        print('--> perlbench')
        process1 = spec06_benchmarks.perlbench
    elif args.benchmark1 == 'threads':
        print('--> threads')
        process1 = spec06_benchmarks.threads
    elif args.benchmark1 == 'bzip2':
        print('--> bzip2')
        process1 = spec06_benchmarks.bzip2
    elif args.benchmark1 == 'gcc':
        print('--> gcc')
        process1 = spec06_benchmarks.gcc
    elif args.benchmark1 == 'bwaves':
        print('--> bwaves')
        process1 = spec06_benchmarks.bwaves
    elif args.benchmark1 == 'gamess':
        print('--> gamess')
        process1 = spec06_benchmarks.gamess
    elif args.benchmark1 == 'mcf':
        print('--> mcf')
        process1 = spec06_benchmarks.mcf
    elif args.benchmark1 == 'milc':
        print('--> milc')
        process1 = spec06_benchmarks.milc
    elif args.benchmark1 == 'zeusmp':
        print('--> zeusmp')
        process1 = spec06_benchmarks.zeusmp
    elif args.benchmark1 == 'gromacs':
        print('--> gromacs')
        process1 = spec06_benchmarks.gromacs
    elif args.benchmark1 == 'cactusADM':
        print('--> cactusADM')
        process1 = spec06_benchmarks.cactusADM
    elif args.benchmark1 == 'leslie3d':
        print('--> leslie3d')
        process1 = spec06_benchmarks.leslie3d
    elif args.benchmark1 == 'namd':
        print('--> namd')
        process1 = spec06_benchmarks.namd
    elif args.benchmark1 == 'gobmk':
        print('--> gobmk')
        process1 = spec06_benchmarks.gobmk
    elif args.benchmark1 == 'dealII':
        print('--> dealII')
        process1 = spec06_benchmarks.dealII
    elif args.benchmark1 == 'soplex':
        print('--> soplex')
        process1 = spec06_benchmarks.soplex
    elif args.benchmark1 == 'povray':
        print('--> povray')
        process1 = spec06_benchmarks.povray
    elif args.benchmark1 == 'calculix':
        print('--> calculix')
        process1 = spec06_benchmarks.calculix
    elif args.benchmark1 == 'hmmer':
        print('--> hmmer')
        process1 = spec06_benchmarks.hmmer
    elif args.benchmark1 == 'sjeng':
        print('--> sjeng')
        process1 = spec06_benchmarks.sjeng
    elif args.benchmark1 == 'GemsFDTD':
        print('--> GemsFDTD')
        process1 = spec06_benchmarks.GemsFDTD
    elif args.benchmark1 == 'libquantum':
        print('--> libquantum')
        process1 = spec06_benchmarks.libquantum
    elif args.benchmark1 == 'h264ref':
        print('--> h264ref')
        process1 = spec06_benchmarks.h264ref
    elif args.benchmark1 == 'tonto':
        print('--> tonto')
        process1 = spec06_benchmarks.tonto
    elif args.benchmark1 == 'lbm':
        print('--> lbm')
        process1 = spec06_benchmarks.lbm
    elif args.benchmark1 == 'omnetpp':
        print('--> omnetpp')
        process1 = spec06_benchmarks.omnetpp
    elif args.benchmark1 == 'astar':
        print('--> astar')
        process1 = spec06_benchmarks.astar
    elif args.benchmark1 == 'wrf':
        print('--> wrf')
        process1 = spec06_benchmarks.wrf
    elif args.benchmark1 == 'sphinx3':
        print('--> sphinx3')
        process1 = spec06_benchmarks.sphinx3
    elif args.benchmark1 == 'Xalan':
        print('--> xalancbmk')
        process1 = spec06_benchmarks.Xalan
    elif args.benchmark1 == 'specrand_i':
        print('--> specrand_i')
        process1 = spec06_benchmarks.specrand_i
    elif args.benchmark1 == 'specrand_f':
        print('--> specrand_f')
        process1 = spec06_benchmarks.specrand_f
    else:
        print("No recognized SPEC2006 benchmark1 selected! Exiting.")
        sys.exit(1)
else:
    print("Need --benchmark1 switch to specify SPEC CPU2006 workload. Exiting!\n")
    sys.exit(1)

reload(spec06_benchmarks)

if args.benchmark2:
    print('Selected SPEC_CPU2006 benchmark2')
    if args.benchmark2 == 'perlbench':
        print('--> perlbench')
        process2 = spec06_benchmarks.perlbench
    elif args.benchmark2 == 'threads':
        print('--> threads')
        process2 = spec06_benchmarks.threads
    elif args.benchmark2 == 'bzip2':
        print('--> bzip2')
        process2 = spec06_benchmarks.bzip2
    elif args.benchmark2 == 'gcc':
        print('--> gcc')
        process2 = spec06_benchmarks.gcc
    elif args.benchmark2 == 'bwaves':
        print('--> bwaves')
        process2 = spec06_benchmarks.bwaves
    elif args.benchmark2 == 'gamess':
        print('--> gamess')
        process2 = spec06_benchmarks.gamess
    elif args.benchmark2 == 'mcf':
        print('--> mcf')
        process2 = spec06_benchmarks.mcf
    elif args.benchmark2 == 'milc':
        print('--> milc')
        process2 = spec06_benchmarks.milc
    elif args.benchmark2 == 'zeusmp':
        print('--> zeusmp')
        process2 = spec06_benchmarks.zeusmp
    elif args.benchmark2 == 'gromacs':
        print('--> gromacs')
        process2 = spec06_benchmarks.gromacs
    elif args.benchmark2 == 'cactusADM':
        print('--> cactusADM')
        process2 = spec06_benchmarks.cactusADM
    elif args.benchmark2 == 'leslie3d':
        print('--> leslie3d')
        process2 = spec06_benchmarks.leslie3d
    elif args.benchmark2 == 'namd':
        print('--> namd')
        process2 = spec06_benchmarks.namd
    elif args.benchmark2 == 'gobmk':
        print('--> gobmk')
        process2 = spec06_benchmarks.gobmk
    elif args.benchmark2 == 'dealII':
        print('--> dealII')
        process2 = spec06_benchmarks.dealII
    elif args.benchmark2 == 'soplex':
        print('--> soplex')
        process2 = spec06_benchmarks.soplex
    elif args.benchmark2 == 'povray':
        print('--> povray')
        process2 = spec06_benchmarks.povray
    elif args.benchmark2 == 'calculix':
        print('--> calculix')
        process2 = spec06_benchmarks.calculix
    elif args.benchmark2 == 'hmmer':
        print('--> hmmer')
        process2 = spec06_benchmarks.hmmer
    elif args.benchmark2 == 'sjeng':
        print('--> sjeng')
        process2 = spec06_benchmarks.sjeng
    elif args.benchmark2 == 'GemsFDTD':
        print('--> GemsFDTD')
        process2 = spec06_benchmarks.GemsFDTD
    elif args.benchmark2 == 'libquantum':
        print('--> libquantum')
        process2 = spec06_benchmarks.libquantum
    elif args.benchmark2 == 'h264ref':
        print('--> h264ref')
        process2 = spec06_benchmarks.h264ref
    elif args.benchmark2 == 'tonto':
        print('--> tonto')
        process2 = spec06_benchmarks.tonto
    elif args.benchmark2 == 'lbm':
        print('--> lbm')
        process2 = spec06_benchmarks.lbm
    elif args.benchmark2 == 'omnetpp':
        print('--> omnetpp')
        process2 = spec06_benchmarks.omnetpp
    elif args.benchmark2 == 'astar':
        print('--> astar')
        process2 = spec06_benchmarks.astar
    elif args.benchmark2 == 'wrf':
        print('--> wrf')
        process2 = spec06_benchmarks.wrf
    elif args.benchmark2 == 'sphinx3':
        print('--> sphinx3')
        process2 = spec06_benchmarks.sphinx3
    elif args.benchmark2 == 'Xalan':
        print('--> xalancbmk')
        process2 = spec06_benchmarks.Xalan
    elif args.benchmark2 == 'specrand_i':
        print('--> specrand_i')
        process2 = spec06_benchmarks.specrand_i
    elif args.benchmark2 == 'specrand_f':
        print('--> specrand_f')
        process2 = spec06_benchmarks.specrand_f
    else:
        print("No recognized SPEC2006 benchmark2 selected! Exiting.")
        sys.exit(1)
    process2.pid=101
else:
    print("Need --benchmark2 switch to specify SPEC CPU2006 workload. Exiting!\n")
    sys.exit(1)

# Set process1 stdout/stderr
if args.benchmark1_stdout:
    process1.output = args.benchmark1_stdout
    print("Process 1 stdout file: " + process1.output)
if args.benchmark1_stderr:
    process1.errout = args.benchmark1_stderr
    print("Process 1 stderr file: " + process1.errout)

# Set process2 stdout/stderr
if args.benchmark2_stdout:
    process2.output = args.benchmark2_stdout
    print("Process 2 stdout file: " + process2.output)
if args.benchmark2_stderr:
    process2.errout = args.benchmark2_stderr
    print("Process 2 stderr file: " + process2.errout)

# process1 = Process()
# #process1.pid=100
# process1.executable =  'bzip2'
# process1.cmd = [process1.executable] + ['input.program', 'input.combined']
# process1.output = args.benchmark1_stdout
# process1.errout = args.benchmark1_stderr

# process2 = Process()
# #process2.pid=101
# process2.executable =  'bzip2'
# process2.cmd = [process2.executable] + ['input.program', 'input.combined']
# process2.output = args.benchmark2_stdout
# process2.errout = args.benchmark2_stderr

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
# np = 2
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
# for i in range(np): 
#     system.cpu[i].workload = process
#     system.cpu[i].createThreads()
#     print(process.cmd)

system.cpu[0].workload = process1
system.cpu[0].createThreads()
print(process1.cmd)

system.cpu[1].workload = process2
system.cpu[1].createThreads()
print(process2.cmd)

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

    # system.cpu[0].interrupts[0].pio = system.membus.mem_side_ports
    # system.cpu[0].interrupts[0].int_requestor = system.membus.cpu_side_ports
    # system.cpu[0].interrupts[0].int_responder = system.membus.mem_side_ports
    # system.cpu[1].interrupts[0].pio = system.membus.mem_side_ports
    # system.cpu[1].interrupts[0].int_requestor = system.membus.cpu_side_ports
    # system.cpu[1].interrupts[0].int_responder = system.membus.mem_side_ports
    system.system_port = system.membus.cpu_side_ports
    CacheConfig.config_cache(args, system)
    MemConfig.config_mem(args, system)
    config_filesystem(system, args)

system.workload = SEWorkload.init_compatible(process1.executable)

if args.wait_gdb:
    system.workload.wait_for_remote_gdb = True

root = Root(full_system=False, system=system)
Simulation.run(args, root, system, FutureClass)
