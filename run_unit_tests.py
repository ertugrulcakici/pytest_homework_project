#!/usr/bin/env python
"""
Script to run all unit tests with coverage reporting.
"""
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run unit tests with coverage.")
    parser.add_argument(
        "--html", action="store_true", help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--service",
        type=str,
        choices=["user", "item", "basket", "token", "equivalence", "boundary", "assert", "all"],
        default="all",
        help="Specific service or testing technique to test",
    )

    args = parser.parse_args()

    # Base command, -xvs for xfail, verbose, and showlocals.
    # Xfail is used to mark tests that are expected to fail.
    # Verbose for detailed output, and showlocals to show local variables in failures.
    cmd = ["pytest", "-xvs", "-m", "unit"]  # Always run only unit tests

    # Add coverage options
    cmd.extend(["--cov=app", "--cov-report=term"])
    # term is for terminal output, html is for HTML report
    if args.html:
        cmd.append("--cov-report=html")
        print("HTML coverage report will be generated in 'htmlcov' directory")

    # Add test path based on service or testing technique
    if args.service == "all":
        cmd.append("tests/unit/")
    elif args.service == "user":
        cmd.append("tests/unit/test_user_service.py")
    elif args.service == "item":
        cmd.append("tests/unit/test_item_service.py")
    elif args.service == "basket":
        cmd.append("tests/unit/test_basket_service.py")
    elif args.service == "token":
        cmd.append("tests/unit/test_token_service.py")
    elif args.service == "equivalence":
        cmd.append("tests/unit/test_equivalence_partitioning.py")
    elif args.service == "boundary":
        cmd.append("tests/unit/test_boundary_value_analysis.py")
    elif args.service == "assert":
        cmd.append("tests/unit/test_assert_methods.py")

    # Print the command being run
    print(f"Running: {' '.join(cmd)}")

    # Run the command
    result = subprocess.run(" ".join(cmd), shell=True)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
