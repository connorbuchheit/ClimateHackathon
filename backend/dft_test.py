from pyscf import gto, dft
import time
import psutil

def compute_dft(molecule: str, basis: str = "cc-pvtz") -> dict:
    """
    Perform a DFT calculation on the given molecule using a complex basis set.
    :param molecule: String representation of the molecule (e.g., "H 0 0 0; O 0 0 1")
    :param basis: Basis set to use for the calculation (default: cc-pVTZ)
    :return: Dictionary containing energy, elapsed time, and CPU usage stats
    """
    try:
        # Build the molecule
        mol = gto.Mole()
        mol.build(atom=molecule, basis=basis)
        
        # Set up DFT method
        mf = dft.RKS(mol)
        mf.xc = 'b3lyp'  # Exchange-correlation functional
        
        # Monitor CPU usage and timing
        start_time = time.time()
        cpu_percent_before = psutil.cpu_percent(interval=None)

        energy = mf.kernel()  # Run the DFT calculation

        elapsed_time = time.time() - start_time
        cpu_percent_after = psutil.cpu_percent(interval=None)

        return {
            "energy": energy,
            "time": elapsed_time,
            "cpu_usage_percent": (cpu_percent_before + cpu_percent_after) / 2
        }
    except Exception as e:
        print(f"Error during DFT calculation: {e}")
        return {"error": str(e)}

def main():
    molecules = [
        "H 0 0 0; H 0 0 0.74",  # H2
        "O 0 0 0; H 0 0 0.96; H 0 0.76 0.58",  # H2O (water)
        "C 0 0 0; H 0 0 1; H 1 0 0; H 0 1 0",  # CH4 (methane)
        "C 0 0 0; O 0 0 1; H 1 0 0; H -1 0 0",  # CH2O (formaldehyde)
        "C 0 0 0; O 0 0 1; O 0 0 -1",  # CO2 (carbon dioxide)
    ]

    print(f"\nTesting all molecules with basis set: cc-pVTZ\n")
    for molecule in molecules:
        print(f"Testing molecule: {molecule}")
        result = compute_dft(molecule, basis="cc-pvtz")
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Energy: {result['energy']} Hartrees")
            print(f"Time: {result['time']} seconds")
            print(f"CPU Usage: {result['cpu_usage_percent']}%")

if __name__ == "__main__":
    main()