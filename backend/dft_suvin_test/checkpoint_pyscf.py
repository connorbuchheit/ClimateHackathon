import os
import numpy as np
from pyscf import scf

class CheckpointSCFWrapper:
    def __init__(self, mol, chkfile="scf_checkpoint.npz"):
        """
        Wrapper for PySCF RHF with checkpointing capability.
        
        Parameters:
            mol: PySCF Molecule object
            chkfile: Path to the checkpoint file
        """
        self.mol = mol
        self.chkfile = chkfile
        self.mf = scf.RHF(mol)
        self.mf.verbose = 4  # Set verbosity to debug level

    def save_checkpoint(self, dm, cycle):
        """
        Save the density matrix and cycle number to a checkpoint file.
        """
        print(f"Saving checkpoint at cycle {cycle}...")
        np.savez(self.chkfile, dm=dm, cycle=cycle)

    def load_checkpoint(self):
        """
        Load the density matrix and cycle number from a checkpoint file.
        """
        if not os.path.exists(self.chkfile):
            print("No checkpoint found. Starting from scratch.")
            return None, 0  # Return default values for first iteration
        
        print("Loading checkpoint...")
        data = np.load(self.chkfile)
        dm = data["dm"]
        cycle = data["cycle"]
        print(f"Checkpoint loaded: Starting from cycle {cycle}")
        return dm, cycle

    def kernel(self, max_cycle=10, conv_tol=1e-6):
        """
        Perform the SCF calculation with checkpointing.
        
        Parameters:
            max_cycle: Maximum number of SCF cycles
            conv_tol: Convergence tolerance for the density matrix
        """
        self.mf.conv_tol = conv_tol
        self.mf.max_cycle = max_cycle

        # Load checkpoint if available
        dm, start_cycle = self.load_checkpoint()
        if dm is not None:
            self.mf.init_guess = dm  # Set the density matrix from checkpoint
        else:
            # Initialize the density matrix if no checkpoint is available
            dm = self.mf.get_init_guess()

        # Initialize defaults for final results
        mo_energy, mo_coeff, mo_occ = None, None, None

        # Custom SCF loop with checkpointing
        for cycle in range(start_cycle, max_cycle):
            print(f"Starting SCF cycle {cycle}...")
            fock = self.mf.get_fock(dm=dm)  # Build Fock matrix
            mo_energy, mo_coeff = self.mf.eig(fock, self.mf.get_ovlp())  # Diagonalize Fock matrix
            dm_new = self.mf.make_rdm1(mo_coeff, mo_occ=self.mf.get_occ(mo_energy))  # Update density matrix

            # Check convergence
            norm_diff = np.linalg.norm(dm_new - dm) if dm is not None else np.inf
            print(f"Cycle {cycle}: norm_diff = {norm_diff}")
            if norm_diff < conv_tol:
                print("SCF converged.")
                self.mf.converged = True
                break

            # Save checkpoint
            self.save_checkpoint(dm_new, cycle)

            # Update density matrix for the next iteration
            dm = dm_new

        # Finalize the calculation
        if self.mf.converged:
            self.mf.mo_energy = mo_energy
            self.mf.mo_coeff = mo_coeff
            self.mf.mo_occ = self.mf.get_occ(mo_energy, mo_coeff)
            self.mf.e_tot = self.mf.energy_tot(dm)
            print(f"SCF Finished. Total Energy: {self.mf.e_tot:.6f} Hartree")
        else:
            print("SCF did not converge within the specified cycles.")
            self.mf.mo_energy = mo_energy
            self.mf.mo_coeff = mo_coeff
            self.mf.mo_occ = None  # Occupations are undefined if not converged
            self.mf.e_tot = None  # Energy is undefined if not converged
