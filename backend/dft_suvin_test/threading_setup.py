# threading_setup.py

import os

def enable_threading(num_threads):
    os.environ['OMP_NUM_THREADS'] = str(num_threads)
    os.environ['MKL_NUM_THREADS'] = str(num_threads)
    os.environ['OPENBLAS_NUM_THREADS'] = str(num_threads)
    os.environ['VECLIB_MAXIMUM_THREADS'] = str(num_threads)
    os.environ['NUMEXPR_NUM_THREADS'] = str(num_threads)
