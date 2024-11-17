# worker2_checkpoint.py

from pyscf import gto
from checkpoint_pyscf import CheckpointSCFWrapper
from molecules import molecule_data

def run_second_half():
    # Get molecule definition from centralized file
    molecule_name = "H2O"  # Ensure this matches the molecule in worker1
    molecule = molecule_data[molecule_name]

    # Define the molecule
    mol = gto.Mole()
    mol.atom = molecule
    mol.basis = 'cc-pvtz'  # Use the same basis set as in worker1
    mol.build()

    # Initialize SCF wrapper with DFT and checkpointing
    scf_wrapper = CheckpointSCFWrapper(mol, chkfile=f"scf_checkpoint_{molecule_name}.npz")

    # Continue SCF calculation from checkpoint
    result = scf_wrapper.kernel(max_cycle=100)  # Set higher max_cycle to allow convergence

    # Print results if available
    if result and "energy" in result:
        print(f"\nFinal Results for {molecule_name}:")
        print(f"  - Energy: {result['energy']} Hartrees")
        print(f"  - Elapsed Time: {result['time']:.2f} seconds")
        print(f"  - Average CPU Usage: {result['cpu_usage_percent']:.2f}%")

if __name__ == "__main__":
    run_second_half()
