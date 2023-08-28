import m5
from m5.objects import *
 
# These three directory paths are not currently used.
#gem5_dir = '<FULL_PATH_TO_YOUR_GEM5_INSTALL>'
#spec_dir = '<FULL_PATH_TO_YOUR_SPEC_CPU2006_INSTALL>'
#out_dir = '<FULL_PATH_TO_DESIRED_OUTPUT_DIRECTORY>'
 
#temp
#binary_dir = spec_dir
#data_dir = spec_dir

binary_base_dir = 'spec-x86-cpu-2006'
#400.perlbench
perlbench = Process() # Update June 7, 2017: This used to be LiveProcess()
perlbench.executable =  'perlbench'
# TEST CMDS
#perlbench.cmd = [perlbench.executable] + ['-I.', '-I./lib', 'attrs.pl']
# REF CMDS
# perlbench.cmd = [perlbench.executable] + ['-I./lib', 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']
# perlbench.cmd = [perlbench.executable]
#perlbench.cmd = [perlbench.executable] + ['-I./lib', 'diffmail.pl', '4', '800', '10', '17', '19', '300']
perlbench.cmd = [perlbench.executable] + ['splitmail.pl', '1600', '12', '26', '16', '4500']
#perlbench.output = out_dir+'perlbench.out'
 
#401.bzip2
bzip2 = Process() # Update June 7, 2017: This used to be LiveProcess()
bzip2.executable =  'bzip2'
# TEST CMDS
#bzip2.cmd = [bzip2.executable] + ['input.program', '5']
# REF CMDS
# bzip2.cmd = [bzip2.executable] + ['input.source', '280']
# bzip2.cmd = [bzip2.executable] + ['/home/piyush/gem5/MTP/spec-arm-cpu-2006/benchspec/CPU2006/401.bzip2/data/all/input/input.combined']
# bzip2.input = '/home/piyush/gem5/MTP/spec-arm-cpu-2006/benchspec/CPU2006/401.bzip2/data/all/input/input.program'
# bzip2.cmd = [bzip2.executable] + ['/home/piyush/gem5/MTP/spec-arm-cpu-2006/benchspec/CPU2006/401.bzip2/data/all/input/input.program'] + ['/home/piyush/gem5/MTP/spec-arm-cpu-2006/benchspec/CPU2006/401.bzip2/data/all/input/input.combined']
# bzip2.cmd = [bzip2.executable] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/401.bzip2/data/all/input/input.program'] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/401.bzip2/data/all/input/input.combined']
# bzip2.cmd = [bzip2.executable] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/401.bzip2/data/all/input/input.program'] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/401.bzip2/data/all/input/input.combined']
#bzip2.cmd = [bzip2.executable] + ['chicken.jpg', '30']
#bzip2.cmd = [bzip2.executable] + ['liberty.jpg', '30']
bzip2.cmd = [bzip2.executable] + ['input.program', 'input.combined']
#bzip2.cmd = [bzip2.executable] + ['text.html', '280']
#bzip2.cmd = [bzip2.executable] + ['input.combined', '200']
#bzip2.output = out_dir + 'bzip2.out'
 
#403.gcc
gcc = Process() # Update June 7, 2017: This used to be LiveProcess()
gcc.executable = 'gcc'
# TEST CMDS
#gcc.cmd = [gcc.executable] + ['cccp.i', '-o', 'cccp.s']
# REF CMDS
# gcc.cmd = [gcc.executable] + ['166.i', '-o', '166.s']
# gcc.cmd = [gcc.executable] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/403.gcc/data/ref/input/200.in'] + ['-o'] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/403.gcc/data/ref/output/200.s']
gcc.cmd = [gcc.executable] + ['200.in']
# gcc.input = '200.in'
# gcc.input = '/home/piyush/gem5/MTP/' + binary_base_dir + '/benchspec/CPU2006/403.gcc/data/ref/input/200.in'
#gcc.cmd = [gcc.executable] + ['200.i', '-o', '200.s']
#gcc.cmd = [gcc.executable] + ['c-typeck.i', '-o', 'c-typeck.s']
#gcc.cmd = [gcc.executable] + ['cp-decl.i', '-o', 'cp-decl.s']
#gcc.cmd = [gcc.executable] + ['expr.i', '-o', 'expr.s']
#gcc.cmd = [gcc.executable] + ['expr2.i', '-o', 'expr2.s']
#gcc.cmd = [gcc.executable] + ['g23.i', '-o', 'g23.s']
#gcc.cmd = [gcc.executable] + ['s04.i', '-o', 's04.s']
#gcc.cmd = [gcc.executable] + ['scilab.i', '-o', 'scilab.s']
#gcc.output = out_dir + 'gcc.out'
 
# #410.bwaves
# bwaves = Process() # Update June 7, 2017: This used to be LiveProcess()
# bwaves.executable = 'bwaves'
# # TEST CMDS
# #bwaves.cmd = [bwaves.executable]
# # REF CMDS
# bwaves.cmd = [bwaves.executable]
# #bwaves.output = out_dir + 'bwaves.out'
 
#416.gamess
gamess = Process() # Update June 7, 2017: This used to be LiveProcess()
gamess.executable = 'gamess'
# TEST CMDS
#gamess.cmd = [gamess.executable]
#gamess.input = 'exam29.config'
# REF CMDS
gamess.cmd = [gamess.executable]
gamess.input = 'cytosine.2.config'
#gamess.cmd = [gamess.executable]
#gamess.input = 'h2ocu2+.gradient.config'
#gamess.cmd = [gamess.executable]
#gamess.input = 'triazolium.config'
#gamess.output = out_dir + 'gamess.out'
 
#429.mcf
mcf = Process() # Update June 7, 2017: This used to be LiveProcess()
mcf.executable =  'mcf'
# TEST CMDS
mcf.cmd = [mcf.executable] + ['inp.in']
# REF CMDS
# mcf.cmd = [mcf.executable] + ['-o', '/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/429.mcf/data/ref/output/inp.out']
# mcf.cmd = [mcf.executable] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/429.mcf/data/ref/input/inp.in']
# mcf.cmd = [mcf.executable] + ['/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/429.mcf/data/ref/input/inp.in']
# mcf.cmd = [mcf.executable]
# mcf.input = '/home/piyush/gem5/MTP/' + binary_base_dir + '/benchspec/CPU2006/429.mcf/data/ref/input/inp.in'
#mcf.output = out_dir + 'mcf.out'
 
#433.milc
milc = Process() # Update June 7, 2017: This used to be LiveProcess()
milc.executable = 'milc'
# TEST CMDS
milc.cmd = [milc.executable]
milc.input = 'su3imp.in'
# REF CMDS
# milc.cmd = [milc.executable] + ['-o', '/home/piyush/gem5/MTP/spec-arm-cpu-2006/benchspec/CPU2006/433.milc/data/test/output/su3imp.out']
# milc.cmd = [milc.executable] + ['su3imp.in']
# milc.input = '/home/piyush/gem5/MTP/' + binary_base_dir + '/benchspec/CPU2006/433.milc/data/test/input/su3imp.in'
# milc.cmd = [milc.executable] + ['/home/piyush/gem5/MTP/spec-arm-cpu-2006/benchspec/CPU2006/433.milc/data/ref/input/su3imp.in']
#milc.output = out_dir + 'milc.out'
 
#434.zeusmp
zeusmp = Process() # Update June 7, 2017: This used to be LiveProcess()
zeusmp.executable = 'zeusmp'
# TEST CMDS
#zeusmp.cmd = [zeusmp.executable]
# REF CMDS
zeusmp.cmd = [zeusmp.executable]
#zeusmp.output = out_dir + 'zeusmp.out'
 
#435.gromacs
gromacs = Process() # Update June 7, 2017: This used to be LiveProcess()
gromacs.executable = 'gromacs'
# TEST CMDS
#gromacs.cmd = [gromacs.executable] + ['-silent','-deffnm', 'gromacs', '-nice','0']
# REF CMDS
gromacs.cmd = [gromacs.executable] + ['-silent','-deffnm', 'gromacs', '-nice','0']
#gromacs.output = out_dir + 'gromacs.out'
 
#436.cactusADM
cactusADM = Process() # Update June 7, 2017: This used to be LiveProcess()
cactusADM.executable = 'cactusADM' 
# TEST CMDS
cactusADM.cmd = [cactusADM.executable] + ['benchADM.par']
# REF CMDS
# cactusADM.cmd = [cactusADM.executable] + ['/home/piyush/gem5/MTP/'] + [binary_base_dir] + ['/benchspec/CPU2006/436.cactusADM/data/ref/input/benchADM.par']
# cactusADM.cmd = [cactusADM.executable] + ['/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/436.cactusADM/data/ref/input/benchADM.par']
#cactusADM.output = out_dir + 'cactusADM.out'
 
#437.leslie3d
leslie3d = Process() # Update June 7, 2017: This used to be LiveProcess()
leslie3d.executable = 'leslie3d'
# TEST CMDS
#leslie3d.cmd = [leslie3d.executable]
#leslie3d.input = 'leslie3d.in'
# REF CMDS
leslie3d.cmd = [leslie3d.executable]
leslie3d.input = 'leslie3d.in'
#leslie3d.output = out_dir + 'leslie3d.out'
 
#444.namd
namd = Process() # Update June 7, 2017: This used to be LiveProcess()
namd.executable = 'namd'
# TEST CMDS
namd.cmd = [namd.executable] + ['--input', 'namd.input', '--iterations', '1']
# REF CMDS
# namd.cmd = [namd.executable] + ['--input', 'namd.input', '--output', 'namd.out', '--iterations', '38']
# namd.cmd = [namd.executable]
# namd.input = '/home/piyush/gem5/MTP/spec-arm-cpu-2006/benchspec/CPU2006/444.namd/data/all/input/namd.input'
# namd.cmd = [namd.executable] + ['--input', '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/444.namd/data/all/input/namd.input', '--iterations', '1']
#namd.output = out_dir + 'namd.out'
 
#445.gobmk
gobmk = Process() # Update June 7, 2017: This used to be LiveProcess()
gobmk.executable = 'gobmk'
# TEST CMDS
gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
#gobmk.input = 'dniwog.tst'
# REF CMDS
# gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp', '<', '13x13.tst']
gobmk.input = '13x13.tst'
#gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
# gobmk.input = '/home/piyush/gem5/MTP/' + binary_base_dir + '/benchspec/CPU2006/445.gobmk/data/ref/input/13x13.tst'
#gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
#gobmk.input = 'score2.tst'
#gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
#gobmk.input = 'trevorc.tst'
#gobmk.cmd = [gobmk.executable] + ['--quiet','--mode', 'gtp']
#gobmk.input = 'trevord.tst'
#gobmk.output = out_dir + 'gobmk.out'
 
#447.dealII
####### NOT WORKING #########
dealII = Process() # Update June 7, 2017: This used to be LiveProcess()
dealII.executable = 'dealII'
dealII.cmd = [dealII.executable]
# TEST CMDS
####### NOT WORKING #########
#dealII.cmd = [gobmk.executable]+['8']
# REF CMDS
####### NOT WORKING #########
#dealII.output = out_dir + 'dealII.out'
 
#450.soplex
soplex = Process() # Update June 7, 2017: This used to be LiveProcess()
soplex.executable = 'soplex'
# TEST CMDS
#soplex.cmd = [soplex.executable] + ['-m10000', 'test.mps']
# REF CMDS
soplex.cmd = [soplex.executable] + ['pds-50.mps']
#soplex.cmd = [soplex.executable] + ['-m3500', 'ref.mps']
#soplex.output = out_dir + 'soplex.out'
 
#453.povray
povray = Process() # Update June 7, 2017: This used to be LiveProcess()
povray.executable = 'povray'
# TEST CMDS
povray.cmd = [povray.executable] + ['SPEC-benchmark-ref.ini']
# REF CMDS
# povray.cmd = [povray.executable] + ['/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/453.povray/data/ref/input/SPEC-benchmark-ref.ini']
# povray.cmd = [povray.executable]
# povray.input = 'SPEC-benchmark-ref.ini'
#povray.output = out_dir + 'povray.out'
 
#454.calculix
calculix = Process() # Update June 7, 2017: This used to be LiveProcess()
calculix.executable = 'calculix'
# TEST CMDS
#calculix.cmd = [calculix.executable] + ['-i', 'beampic']
# REF CMDS
# calculix.cmd = [calculix.executable] + ['-i', '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/454.calculix/data/ref/input/hyperviscoplastic']
calculix.cmd = [calculix.executable] + ['hyperviscoplastic']
#calculix.output = out_dir + 'calculix.out' 
 
#456.hmmer
hmmer = Process() # Update June 7, 2017: This used to be LiveProcess()
hmmer.executable = 'hmmer'
# TEST CMDS
#hmmer.cmd = [hmmer.executable] + ['--fixed', '0', '--mean', '325', '--num', '45000', '--sd', '200', '--seed', '0', 'bombesin.hmm']
# REF CMDS
hmmer.cmd = [hmmer.executable] + ['nph3.hmm']
# hmmer.cmd = [hmmer.executable] + ['/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/456.hmmer/data/ref/input/nph3.mm', '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/456.hmmer/data/ref/input/swiss41']
# hmmer.cmd = [hmmer.executable]
# hmmer.input = '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/456.hmmer/data/ref/input/nph3.mm' + '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/456.hmmer/data/ref/input/swiss41'
#hmmer.cmd = [hmmer.executable] + ['--fixed', '0', '--mean', '500', '--num', '500000', '--sd', '350', '--seed', '0', 'retro.hmm']
#hmmer.output = out_dir + 'hmmer.out'
 
#458.sjeng
sjeng = Process() # Update June 7, 2017: This used to be LiveProcess()
sjeng.executable = 'sjeng' 
# TEST CMDS
#sjeng.cmd = [sjeng.executable] + ['test.txt']
# REF CMDS
# sjeng.cmd = [sjeng.executable] + ['/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/458.sjeng/data/ref/input/ref.txt']
sjeng.cmd = [sjeng.executable] + ['ref.txt']
#sjeng.output = out_dir + 'sjeng.out'
 
#459.GemsFDTD
GemsFDTD = Process() # Update June 7, 2017: This used to be LiveProcess()
GemsFDTD.executable = 'GemsFDTD' 
# TEST CMDS
#GemsFDTD.cmd = [GemsFDTD.executable]
# REF CMDS
GemsFDTD.cmd = [GemsFDTD.executable]
#GemsFDTD.output = out_dir + 'GemsFDTD.out'
 
#462.libquantum
libquantum = Process() # Update June 7, 2017: This used to be LiveProcess()
libquantum.executable = 'libquantum'
# TEST CMDS
#libquantum.cmd = [libquantum.executable] + ['33','5']
# REF CMDS [UPDATE 10/2/2015]: Sparsh Mittal has pointed out the correct input for libquantum should be 1397 and 8, not 1297 and 8. Thanks!
libquantum.cmd = [libquantum.executable] + ['1397','8']
#libquantum.output = out_dir + 'libquantum.out' 
 
#464.h264ref
h264ref = Process() # Update June 7, 2017: This used to be LiveProcess()
h264ref.executable = 'h264ref'
# TEST CMDS
#h264ref.cmd = [h264ref.executable] + ['-d', 'foreman_test_encoder_baseline.cfg']
# REF CMDS
# h264ref.cmd = [h264ref.executable] + ['-d', '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/464.h264ref/data/train/input/foreman_train_encoder_baseline.cfg']
h264ref.cmd = [h264ref.executable]
#h264ref.cmd = [h264ref.executable] + ['-d', 'foreman_ref_encoder_main.cfg']
#h264ref.cmd = [h264ref.executable] + ['-d', 'sss_encoder_main.cfg']
#h264ref.output = out_dir + 'h264ref.out'
 
#465.tonto
tonto = Process() # Update June 7, 2017: This used to be LiveProcess()
tonto.executable = 'tonto'
# TEST CMDS
#tonto.cmd = [tonto.executable]
# REF CMDS
tonto.cmd = [tonto.executable]
#tonto.output = out_dir + 'tonto.out'
 
#470.lbm
lbm = Process() # Update June 7, 2017: This used to be LiveProcess()
lbm.executable = 'lbm'
# TEST CMDS
#lbm.cmd = [lbm.executable] + ['20', 'reference.dat', '0', '1', '100_100_130_cf_a.of']
# REF CMDS
# lbm.cmd = [lbm.executable] + ['3000', 'reference.dat', '0', '0', '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/470.lbm/data/ref/input/100_100_130_ldc.of']
lbm.cmd = [lbm.executable] + ['3000', 'reference.dat', '0', '0', '100_100_130_ldc.of']
#lbm.output = out_dir + 'lbm.out'
 
#471.omnetpp
omnetpp = Process() # Update June 7, 2017: This used to be LiveProcess()
omnetpp.executable = 'omnetpp' 
# TEST CMDS
#omnetpp.cmd = [omnetpp.executable] + ['omnetpp.ini']
# REF CMDS
omnetpp.cmd = [omnetpp.executable]
# omnetpp.cmd = [omnetpp.executable] + ['/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/471.omnetpp/data/ref/input/omnetpp.ini']
#omnetpp.output = out_dir + 'omnetpp.out'
 
#473.astar
astar = Process() # Update June 7, 2017: This used to be LiveProcess()
astar.executable = 'astar'
# TEST CMDS
#astar.cmd = [astar.executable] + ['lake.cfg']
# REF CMDS
# astar.cmd = [astar.executable] + ['/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/473.astar/data/ref/input/BigLakes2048.cfg']
astar.cmd = [astar.executable] + ['BigLakes2048.cfg']
#astar.output = out_dir + 'astar.out'
 
#481.wrf
wrf = Process() # Update June 7, 2017: This used to be LiveProcess()
wrf.executable = 'wrf'
# TEST CMDS
#wrf.cmd = [wrf.executable]
# REF CMDS
wrf.cmd = [wrf.executable]
#wrf.output = out_dir + 'wrf.out'
 
#482.sphinx3
sphinx3 = Process() # Update June 7, 2017: This used to be LiveProcess()
sphinx3.executable = 'sphinx_livepretend' 
# TEST CMDS
sphinx3.cmd = [sphinx3.executable] + ['ctlfile', '.', 'args.an4']
# REF CMDS
# sphinx3.cmd = [sphinx3.executable] + ['ctlfile', '.', '/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/482.sphinx3/data/ref/input/args.an4']
#sphinx3.output = out_dir + 'sphinx3.out'
 
#483.xalancbmk
######## NOT WORKING ###########
Xalan = Process() # Update June 7, 2017: This used to be LiveProcess()
# xalancbmk.executable = 'xalancbmk'
Xalan.executable = 'Xalan'
# TEST CMDS
######## NOT WORKING ###########
# Xalan.cmd = [Xalan.executable] + ['-v','/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/483.xalancbmk/data/ref/input/t5.xml','/home/piyush/gem5/MTP/spec-x86-cpu-2006/benchspec/CPU2006/483.xalancbmk/data/ref/input/xalanc.xsl']
Xalan.cmd = [Xalan.executable] + ['-v','t5.xml','xalanc.xsl']
# REF CMDS
######## NOT WORKING ###########
#xalancbmk.output = out_dir + 'xalancbmk.out'
 
# #998.specrand
# specrand_i = Process() # Update June 7, 2017: This used to be LiveProcess()
# specrand_i.executable = 'specrand'
# # TEST CMDS
# #specrand_i.cmd = [specrand_i.executable] + ['324342', '24239']
# # REF CMDS
# specrand_i.cmd = [specrand_i.executable] + ['1255432124', '234923']
# #specrand_i.output = out_dir + 'specrand_i.out'
 
#999.specrand
specrand_f = Process() # Update June 7, 2017: This used to be LiveProcess()
specrand_f.executable = 'specrand'
# TEST CMDS
#specrand_f.cmd = [specrand_f.executable] + ['324342', '24239']
# REF CMDS
specrand_f.cmd = [specrand_f.executable] + ['1255432124', '234923']
#specrand_f.output = out_dir + 'specrand_f.out'

# binary = '../tests/test-progs/hello/bin/arm/linux/hello'
# hello = Process()
# hello.executable = 'hello'
# # hello.cmd = [binary]
# hello.cmd = [hello.executable]