import argparse
import os
import sys
import m5
import m5.util
from m5.objects import *
from Caches import *
import spec06_benchmarks

# m5.util.addToPath("../configs/")

# from common import Options

# m5.util.addToPath("../../")
# import devices

default_cpu_clock = "2GHz"
default_mem_size = "2GB"

def addOptions(parser):
    parser.add_argument(
        "--restore-from",
        type=str,
        default=None,
        help="Restore from checkpoint",
    )
    parser.add_argument(
        "--cpu-clock",
        type=str,
        default=default_cpu_clock,
        help="Big & Little CPU clock frequency",
    )
    parser.add_argument(
        "--mem-size",
        type=str,
        default=default_mem_size,
        help="System memory size",
    )
    parser.add_argument(
        "--l1i_size",
        help="L1 instruction cache size. Default: 32kB.",
    )
    parser.add_argument(
        "--l1d_size",
        help="L1 data cache size. Default: 32kB.",
    )
    parser.add_argument(
        "--l2_size",
        help="L2 cache size. Default: 2MB.",
    )
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
        "-P",
        "--param",
        action="append",
        default=[],
        help="Set a SimObject parameter relative to the root node. "
        "An extended Python multi range slicing syntax can be used "
        "for arrays. For example: "
        "'system.cpu[0,1,3:8:2].max_insts_all_threads = 42' "
        "sets max_insts_all_threads for cpus 0, 1, 3, 5 and 7 "
        "Direct parameters of the root object are not accessible, "
        "only parameters of its children.",
    )
    # Options.addCommonOptions(parser)
    # Options.addSEOptions(parser)
    return parser


def createSystem(options):
    system = System()

    # Set the clock frequency of the system (and all of its children)
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = options.cpu_clock
    system.clk_domain.voltage_domain = VoltageDomain()

    # Set up the system
    system.mem_mode = "timing"  # Use timing accesses
    system.mem_ranges = [AddrRange(options.mem_size)]  # Create an address range

    system.cpu = [DerivO3CPU(),MinorCPU()]
    # system.cpu = [ArmO3CPU(),ArmTimingSimpleCPU()]
    # system.cpu = DerivO3CPU()

    system.l2bus = [L2XBar() for i in range(2)]
    system.l2cache = [L2Cache(options) for i in range(2)]
    # system.l2bus = L2XBar()
    # system.l2cache = L2Cache(options)

    system.membus = SystemXBar()

    # system.cpu.icache = L1ICache(options)
    # system.cpu.dcache = L1DCache(options)
    # system.cpu.icache.connectCPU(system.cpu)
    # system.cpu.dcache.connectCPU(system.cpu)

    # system.cpu.icache.connectBus(system.l2bus)
    # system.cpu.dcache.connectBus(system.l2bus)

    # system.l2cache.connectCPUSideBus(system.l2bus)
    
    # system.l2cache.connectMemSideBus(system.membus)

    # system.cpu.createInterruptController()

    for i in range(2):
        system.cpu[i].icache = L1ICache(options)
        system.cpu[i].dcache = L1DCache(options)
        system.cpu[i].icache.connectCPU(system.cpu[i])
        system.cpu[i].dcache.connectCPU(system.cpu[i])
        # system.cpu[i].itb.walker.port = system.membus.cpu_side_ports

        system.cpu[i].icache.connectBus(system.l2bus[i])
        system.cpu[i].dcache.connectBus(system.l2bus[i])

        system.l2cache[i].connectCPUSideBus(system.l2bus[i])
        
        system.l2cache[i].connectMemSideBus(system.membus)

        system.cpu[i].createInterruptController()
        # system.cpu[i].interrupts[0].pio = system.membus.mem_side_ports
        # system.cpu[i].interrupts[0].int_requestor = system.membus.cpu_side_ports
        # system.cpu[i].interrupts[0].int_responder = system.membus.mem_side_ports

    # mmu1 = system.cpu[0].mmu
    # mmu2 = system.cpu[1].mmu
    
    # mmu1.release_se = True
    # mmu2.release_se = True
    # Create a DDR3 memory controller and connect it to the membus
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports

    # Connect the system up to the membus
    system.system_port = system.membus.cpu_side_ports

    return system


def build(options):
    m5.ticks.fixGlobalFrequency()

    system = createSystem(options)

    root = Root(full_system=False)

    root.system = system

    if options.benchmark:
        print('Selected SPEC_CPU2006 benchmark')
        if options.benchmark == 'perlbench':
            print('--> perlbench')
            process = spec06_benchmarks.perlbench
        elif options.benchmark == 'hello':
            print('--> hello')
            process = spec06_benchmarks.hello
        elif options.benchmark == 'bzip2':
            print('--> bzip2')
            process = spec06_benchmarks.bzip2
        elif options.benchmark == 'gcc':
            print('--> gcc')
            process = spec06_benchmarks.gcc
        elif options.benchmark == 'bwaves':
            print('--> bwaves')
            process = spec06_benchmarks.bwaves
        elif options.benchmark == 'gamess':
            print('--> gamess')
            process = spec06_benchmarks.gamess
        elif options.benchmark == 'mcf':
            print('--> mcf')
            process = spec06_benchmarks.mcf
        elif options.benchmark == 'milc':
            print('--> milc')
            process = spec06_benchmarks.milc
        elif options.benchmark == 'zeusmp':
            print('--> zeusmp')
            process = spec06_benchmarks.zeusmp
        elif options.benchmark == 'gromacs':
            print('--> gromacs')
            process = spec06_benchmarks.gromacs
        elif options.benchmark == 'cactusADM':
            print('--> cactusADM')
            process = spec06_benchmarks.cactusADM
        elif options.benchmark == 'leslie3d':
            print('--> leslie3d')
            process = spec06_benchmarks.leslie3d
        elif options.benchmark == 'namd':
            print('--> namd')
            process = spec06_benchmarks.namd
        elif options.benchmark == 'gobmk':
            print('--> gobmk')
            process = spec06_benchmarks.gobmk
        elif options.benchmark == 'dealII':
            print('--> dealII')
            process = spec06_benchmarks.dealII
        elif options.benchmark == 'soplex':
            print('--> soplex')
            process = spec06_benchmarks.soplex
        elif options.benchmark == 'povray':
            print('--> povray')
            process = spec06_benchmarks.povray
        elif options.benchmark == 'calculix':
            print('--> calculix')
            process = spec06_benchmarks.calculix
        elif options.benchmark == 'hmmer':
            print('--> hmmer')
            process = spec06_benchmarks.hmmer
        elif options.benchmark == 'sjeng':
            print('--> sjeng')
            process = spec06_benchmarks.sjeng
        elif options.benchmark == 'GemsFDTD':
            print('--> GemsFDTD')
            process = spec06_benchmarks.GemsFDTD
        elif options.benchmark == 'libquantum':
            print('--> libquantum')
            process = spec06_benchmarks.libquantum
        elif options.benchmark == 'h264ref':
            print('--> h264ref')
            process = spec06_benchmarks.h264ref
        elif options.benchmark == 'tonto':
            print('--> tonto')
            process = spec06_benchmarks.tonto
        elif options.benchmark == 'lbm':
            print('--> lbm')
            process = spec06_benchmarks.lbm
        elif options.benchmark == 'omnetpp':
            print('--> omnetpp')
            process = spec06_benchmarks.omnetpp
        elif options.benchmark == 'astar':
            print('--> astar')
            process = spec06_benchmarks.astar
        elif options.benchmark == 'wrf':
            print('--> wrf')
            process = spec06_benchmarks.wrf
        elif options.benchmark == 'sphinx3':
            print('--> sphinx3')
            process = spec06_benchmarks.sphinx3
        elif options.benchmark == 'xalancbmk':
            print('--> xalancbmk')
            process = spec06_benchmarks.xalancbmk
        elif options.benchmark == 'specrand_i':
            print('--> specrand_i')
            process = spec06_benchmarks.specrand_i
        elif options.benchmark == 'specrand_f':
            print('--> specrand_f')
            process = spec06_benchmarks.specrand_f
        else:
            print("No recognized SPEC2006 benchmark selected! Exiting.")
            sys.exit(1)
    else:
        print("Need --benchmark switch to specify SPEC CPU2006 workload. Exiting!\n")
        sys.exit(1)
    
    # Set process stdout/stderr
    if options.benchmark_stdout:
        process.output = options.benchmark_stdout
        print("Process stdout file: " + process.output)
    if options.benchmark_stderr:
        process.errout = options.benchmark_stderr
        print("Process stderr file: " + process.errout)
    
    for i in range(2): 
        system.cpu[i].workload = process
        system.cpu[i].createThreads()
        print(process.cmd)
    # system.cpu.workload = process 
    # system.cpu.createThreads()
    # print(process.cmd)

    system.workload = SEWorkload.init_compatible(process.executable)
    return root


def instantiate(options, checkpoint_dir=None):
    # Get and load from the chkpt or simpoint checkpoint
    if options.restore_from:
        if checkpoint_dir and not os.path.isabs(options.restore_from):
            cpt = os.path.join(checkpoint_dir, options.restore_from)
        else:
            cpt = options.restore_from

        m5.util.inform("Restoring from checkpoint %s", cpt)
        m5.instantiate(cpt)
    else:
        m5.instantiate()


def run(checkpoint_dir=m5.options.outdir):
    # start simulation (and drop checkpoints when requested)
    while True:
        event = m5.simulate()
        exit_msg = event.getCause()
        if exit_msg == "checkpoint":
            print("Dropping checkpoint at tick %d" % m5.curTick())
            cpt_dir = os.path.join(checkpoint_dir, "cpt.%d" % m5.curTick())
            m5.checkpoint(cpt_dir)
            print("Checkpoint done.")
        else:
            print(exit_msg, " @ ", m5.curTick())
            break

    sys.exit(event.getCode())


def main():
    parser = argparse.ArgumentParser(
        description="Generic ARM big.LITTLE configuration (SE Mode)"
    )
    addOptions(parser)
    options = parser.parse_args()
    root = build(options)
    root.apply_config(options.param)
    instantiate(options)
    run()


if __name__ == "__m5_main__":
    main()