# pyscf_setup.py

from pyscf import gto

def setup_molecule():
    # Define the molecular geometry and basis set
    mol = gto.Mole()
    mol.atom = '''
    O  0.000000  0.000000  0.000000
    H  0.756968  0.585882  0.000000
    H -0.756968  0.585882  0.000000
    '''
    mol.basis = 'sto-3g'
    mol.build()
    return mol
