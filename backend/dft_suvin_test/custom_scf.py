import numpy as np
import os
from pyscf import scf

print("Imported scf module:", scf)
print("scf module location:", getattr(scf, '__file__', 'Builtin or Shadowed'))

class CheckpointSCF(scf.RHF):
    def __init__(self, mol, chkfile='scf_checkpoint.npz'):
        super(CheckpointSCF, self).__init__(mol)
        self.chkfile = chkfile  # Set the checkpoint file

    def scf(self, dm0=None):
        # Build the molecule and set up SCF
        self.build()
        self.dump_flags()
        self.converged = False

        # Initial density matrix
        if dm0 is None:
            dm = self.get_init_guess()
        else:
            dm = dm0

        # Check if there's a checkpoint to load
        if os.path.exists(self.chkfile):
            print("Loading checkpoint...")
            data = np.load(self.chkfile)
            dm = data['dm']
            last_cycle = data['cycle']
            print(f"Resuming from cycle {last_cycle}")
        else:
            last_cycle = 0

        for cycle in range(last_cycle + 1, self.max_cycle + 1):
            # Build Fock matrix
            fock = self.get_fock(dm=dm)
            # Diagonalize Fock matrix
            eigvals, eigvecs = self.eig(fock, self.get_ovlp())
            # Compute new density matrix
            dm_new = self.make_rdm1(eigvecs)
            # Check convergence
            norm_dm = np.linalg.norm(dm_new - dm)
            self.logger.info(f"Cycle {cycle}, norm_dm = {norm_dm}")
            if norm_dm < self.conv_tol:
                print("SCF converged")
                self.converged = True
                break
            # Save checkpoint halfway through iteration
            if cycle == last_cycle + 1:
                print("Checkpointing halfway through iteration")
                np.savez(self.chkfile, dm=dm_new, cycle=cycle)
                print("Checkpoint saved. Exiting to simulate transfer to another worker.")
                return None  # Exit early to simulate transfer
            dm = dm_new

        self.mo_energy = eigvals
        self.mo_coeff = eigvecs
        self.mo_occ = self.get_occ(eigvals, eigvecs, dm)
        self.e_tot = self.energy_tot(dm)
        return self.e_tot
