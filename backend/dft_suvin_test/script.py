from pyscf import gto, scf

def run_basic_pyscf():
    # Define the water molecule
    mol = gto.Mole()
    mol.atom = '''
    O  0.000000  0.000000  0.000000
    H  0.756968  0.585882  0.000000
    H -0.756968  0.585882  0.000000
    '''
    mol.basis = 'sto-3g'  # Basic STO-3G basis set
    mol.build()

    # Perform Hartree-Fock calculation
    mf = scf.RHF(mol)
    print("Starting Hartree-Fock calculation...")
    energy = mf.kernel()
    print(f"Final Total Energy: {energy:.6f} Hartree")

if __name__ == "__main__":
    run_basic_pyscf()
