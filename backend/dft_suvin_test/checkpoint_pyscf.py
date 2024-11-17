# checkpoint_pyscf.py

import os
import time
import psutil
import numpy as np
from pyscf import dft

class CheckpointSCFWrapper:
    def __init__(self, mol, chkfile="scf_checkpoint.npz", xc_functional='b3lyp'):
        """
        Wrapper for PySCF DFT calculations with checkpointing and monitoring.

        Parameters:
            mol: PySCF Molecule object
            chkfile: Path to the checkpoint file
            xc_functional: Exchange-correlation functional (default: 'b3lyp')
        """
        self.mol = mol
        self.chkfile = chkfile
        self.mf = dft.RKS(mol)
        self.mf.xc = xc_functional  # Set the exchange-correlation functional
        self.mf.verbose = 4  # Set verbosity to debug level
        self.converged = False  # Track convergence status

        # Load checkpoint if available
        dm, cycle = self.load_checkpoint()
        if dm is not None:
            self.mf.dm = dm  # Set the density matrix from checkpoint
            self.start_cycle = cycle
        else:
            self.start_cycle = 0

        # Set up the callback function for checkpointing
        self.mf.callback = self.checkpoint_callback

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

    def checkpoint_callback(self, envs):
        """
        Callback function called at the end of each SCF cycle.
        Saves the current density matrix and cycle number.
        """
        dm = envs['dm']
        cycle = envs['cycle']
        self.save_checkpoint(dm, cycle)

    def kernel(self, max_cycle=50, conv_tol=1e-6):
        """
        Perform the DFT calculation with checkpointing and monitoring.

        Parameters:
            max_cycle: Maximum number of SCF cycles
            conv_tol: Convergence tolerance for the density matrix
        Returns:
            A dictionary containing energy, elapsed time, and CPU usage stats
        """
        self.mf.conv_tol = conv_tol
        self.mf.max_cycle = max_cycle
        self.mf.init_guess = 'chkfile' if os.path.exists(self.chkfile) else 'minao'

        # Monitor CPU usage and timing
        start_time = time.time()
        cpu_percent_before = psutil.cpu_percent(interval=None)

        # Run the SCF calculation
        try:
            energy = self.mf.kernel()
            self.converged = self.mf.converged
        except Exception as e:
            print(f"Error during SCF calculation: {e}")
            self.converged = False
            energy = None

        cpu_percent_after = psutil.cpu_percent(interval=None)
        elapsed_time = time.time() - start_time

        if self.converged:
            print(f"SCF Finished. Total Energy: {energy:.6f} Hartree")
            return {
                "energy": energy,
                "time": elapsed_time,
                "cpu_usage_percent": (cpu_percent_before + cpu_percent_after) / 2
            }
        else:
            print("SCF did not converge within the specified cycles.")
            return {
                "energy": None,
                "time": elapsed_time,
                "cpu_usage_percent": (cpu_percent_before + cpu_percent_after) / 2,
                "error": "SCF did not converge"
            }
