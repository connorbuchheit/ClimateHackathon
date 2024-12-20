from pyscf import gto, dft

def compute_dft(molecule: str, basis: str = "sto-3g") -> float:
    """
    Perform a DFT calculation on the given molecule.
    :param molecule: String representation of the molecule (e.g., "H 0 0 0; H 0 0 0.74")
    :param basis: Basis set to use for the calculation
    :return: Computed energy value
    """
    mol = gto.Mole()
    mol.build(atom=molecule, basis=basis)
    mf = dft.RKS(mol)
    mf.xc = 'b3lyp'  # Exchange-correlation functional
    energy = mf.kernel()
    return energy