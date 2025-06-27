#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Write results directly to file
with open('minimal_test_results.txt', 'w') as f:
    f.write("FINREXENT MINIMAL TEST RESULTS\n")
    f.write("=" * 50 + "\n")
    f.write(f"Test started at: {datetime.now()}\n\n")
    
    try:
        f.write("1. Testing Python environment...\n")
        f.write(f"   Python version: {sys.version}\n")
        f.write(f"   Python executable: {sys.executable}\n")
        f.write("   ✓ Python environment OK\n")
        
        f.write("2. Testing basic imports...\n")
        import pandas as pd
        f.write(f"   ✓ Pandas version: {pd.__version__}\n")
        
        import numpy as np
        f.write(f"   ✓ NumPy version: {np.__version__}\n")
        
        f.write("3. Testing basic calculations...\n")
        # Test pandas
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        f.write(f"   ✓ Created DataFrame with shape: {df.shape}\n")
        
        # Test numpy
        arr = np.array([1, 2, 3, 4, 5])
        f.write(f"   ✓ Created NumPy array with mean: {arr.mean():.2f}\n")
        
        f.write("4. Testing file operations...\n")
        test_file = "test_output.txt"
        with open(test_file, 'w') as tf:
            tf.write("Test successful!")
        f.write("   ✓ File write test passed\n")
        
        with open(test_file, 'r') as tf:
            content = tf.read()
        f.write(f"   ✓ File read test passed: '{content}'\n")
        
        # Clean up
        os.remove(test_file)
        f.write("   ✓ File cleanup passed\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("✅ ALL MINIMAL TESTS PASSED!\n")
        f.write("✅ Python environment is working!\n")
        f.write("✅ Basic packages are functional!\n")
        f.write("✅ Ready for development!\n")
        f.write("=" * 50 + "\n")
        
    except Exception as e:
        f.write(f"\n❌ ERROR: {str(e)}\n")
        import traceback
        f.write(traceback.format_exc())

print("Minimal test completed. Check minimal_test_results.txt for results.") 