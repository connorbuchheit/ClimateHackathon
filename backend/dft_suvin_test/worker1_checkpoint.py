# worker1_checkpoint.py

from pyscf import gto
from checkpoint_pyscf import CheckpointSCFWrapper
from molecules import molecule_data

def run_first_half():
    # Get molecule definition from centralized file
    molecule_name = "H2O"  # Change the key to select a different molecule
    molecule = molecule_data[molecule_name]

    # Define the molecule
    mol = gto.Mole()
    mol.atom = molecule
    mol.basis = 'cc-pvtz'  # Use a complex basis set
    mol.build()

    # Initialize SCF wrapper with DFT and checkpointing
    scf_wrapper = CheckpointSCFWrapper(mol, chkfile=f"scf_checkpoint_{molecule_name}.npz")

    # Perform SCF calculation up to a few cycles
    result = scf_wrapper.kernel(max_cycle=10000)

    # Print results if available
    if result and "energy" in result:
        print(f"\nResults after first half for {molecule_name}:")
        print(f"  - Energy: {result['energy']} Hartrees")
        print(f"  - Elapsed Time: {result['time']:.2f} seconds")
        print(f"  - Average CPU Usage: {result['cpu_usage_percent']:.2f}%")

if __name__ == "__main__":
    run_first_half()
