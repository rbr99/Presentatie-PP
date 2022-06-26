from mpi4py import MPI
import numpy

def collatzloop(x):
    n=0
    while x != 1:
        n += 1
        if x % 2 == 0:
            x = x//2
        else:
            x = 3*x + 1
    return n

def main():
    # 1 miljoen iteraties op 14 nodes dus 1000000/14 = 71428
    Ondergrens = (my_rank) * 71428 + 1
    v = numpy.arange(Ondergrens, (my_rank + 1) * 71428 + 1, dtype='i')
    if my_rank == 0:
        world_comm.send(v, dest = (my_rank + 1) % world_size)
        collatzloop(len(v))
    if my_rank > 0:
        data = world_comm.recv(source = (my_rank - 1) % world_size)
        world_comm.send(v, dest = (my_rank + 1) % world_size)
        collatzloop(len(v))
    if my_rank == 0:
        data = world_comm.recv(source = world_size - 1)
        collatzloop(len(v))
        
    if (my_rank == 0):
        assert data[1] == 0
        assert data[4] == 2
        assert data[27] == 111

if __name__ == '__main__':

    world_comm = MPI.COMM_WORLD
    world_size = world_comm.Get_size()
    my_rank = world_comm.Get_rank()

    start = MPI.Wtime()
    main()
    einde = MPI.Wtime()

    if (my_rank < 13):
        print("Node", my_rank, "uitgevoerde berekeningen na", einde - start, "seconden.")
    else:
        print("De gehele functie is uitgevoerd in", einde - start, "seconden.")
