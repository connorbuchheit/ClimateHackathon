from pyscf import gto
from checkpoint_pyscf import CheckpointSCFWrapper

def run_first_half():
    # Define the water molecule
    mol = gto.Mole()
    mol.atom = '''
    O  0.000000  0.000000  0.000000
    H  0.756968  0.585882  0.000000
    H -0.756968  0.585882  0.000000
    '''
    mol.basis = 'sto-3g'
    mol.build()

    # Initialize SCF wrapper
    scf_wrapper = CheckpointSCFWrapper(mol, chkfile="scf_checkpoint_worker1.npz")

    # Perform SCF calculation up to a few cycles
    scf_wrapper.kernel(max_cycle=4)

if __name__ == "__main__":
    run_first_half()
