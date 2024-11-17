# worker2.py

from threading_setup import enable_threading
from pyscf_setup import setup_molecule
from custom_scf import CheckpointSCF

def run_second_half():
    enable_threading(4)  # Use 4 threads (adjust as needed)
    mol = setup_molecule()
    mf = CheckpointSCF(mol)
    mf.max_cycle = 10
    mf.conv_tol = 1e-6
    mf.verbose = 4
    mf.scf()

if __name__ == '__main__':
    run_second_half()
