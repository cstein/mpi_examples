import sys

def getMPIInformation(comm):
  """Return the rank and size of a processor"""
  size = comm.Get_size()
  rank = comm.Get_rank()

  return (rank,size)
