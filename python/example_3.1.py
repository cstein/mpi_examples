"""
EXAMPLE 3.1
CONVERTED FROM THE BOOK TO PYTHON BY CASPER STEINMANN
USING MPI BY GROPP ET AL.

USE AT YOUR OWN RISK
"""
from numpy import pi
from mpi4py import MPI

from mpiutil import  getMPIInformation

comm = MPI.COMM_WORLD
(rank,size) = getMPIInformation(comm)

def f(x):
    return 4.0 / (1.0 + x*x)

while True:
    if rank == 0:
        print
        print "Number of intervals [0 exits]:"
        input = raw_input()
        try:
            n = int(input)
        except:
            print "Error: '%s' is not a valid interval." % (input)
            continue
    else:
        n = 0

    n = comm.bcast(n,root=0)

    if n > 0:
        # define intervals and make the appropriate sub-divisions
        h = 1.0/n
        temp_sum = 0.0
        for i in range(rank+1, n, size):
            x = h * (float(i) - 0.5)
            temp_sum = temp_sum + f(x)

        # sum up integral from this rank
        mypi = h * temp_sum

        # global sum
        ourpi = comm.reduce(mypi,MPI.SUM,root=0)

        # print the result if we are the master
        if rank == 0:
            print "pi is %16.9f, error is %16.9f" % (ourpi, ourpi-pi)
    else:
        break
