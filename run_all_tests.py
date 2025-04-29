#!/usr/bin/env python
"""
Helper script to run all unit tests with complete coverage reporting.
This script is simpler than run_unit_tests.py and runs all tests with detailed reports.
"""
import subprocess
import sys

def main():
    print("Running all unit tests with coverage...")
    
    # Run all test types with coverage
    cmd = [
        "pytest",
        "-m", "unit",             # Only run tests marked as unit tests
        "-v",                     # Verbose output
        "--cov=app",              # Coverage for app module
        "--cov-report=term",      # Terminal coverage report
        "--cov-report=html",      # HTML coverage report
        "tests/unit/"             # Path to unit tests
    ]
    
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(" ".join(cmd), shell=True)
    
    print("\nHTML coverage report generated in 'htmlcov' directory")
    print("Open htmlcov/index.html in a browser to view the detailed report")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
