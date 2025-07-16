#!/usr/bin/env python3
"""
Test runner for VEPmcp with different test modes.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"✗ Command not found: {cmd[0]}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test runner for VEPmcp")
    parser.add_argument(
        "--mode",
        choices=["unit", "integration", "all", "ci", "lint", "type"],
        default="all",
        help="Test mode to run",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage reporting")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")

    args = parser.parse_args()

    # Base directory
    base_dir = Path(__file__).parent

    # Common pytest arguments
    pytest_args = ["python", "-m", "pytest", "tests/"]

    if args.verbose:
        pytest_args.append("-v")

    if args.fail_fast:
        pytest_args.append("-x")

    if args.coverage:
        pytest_args.extend(["--cov=vep_mcp", "--cov-report=term-missing"])

    success = True

    if args.mode == "unit":
        # Run unit tests only (exclude integration tests)
        cmd = pytest_args + ["-m", "not integration"]
        success = run_command(cmd, "Unit Tests")

    elif args.mode == "integration":
        # Run integration tests only
        cmd = pytest_args + ["-m", "integration"]
        success = run_command(cmd, "Integration Tests (requires internet)")

    elif args.mode == "all":
        # Run all tests
        cmd = pytest_args.copy()
        success = run_command(cmd, "All Tests")

    elif args.mode == "lint":
        # Run linting
        commands = [
            (["python", "-m", "ruff", "check", "vep_mcp/"], "Ruff Linting"),
            (["python", "-m", "ruff", "format", "--check", "vep_mcp/"], "Ruff Format Check"),
        ]

        for cmd, desc in commands:
            if not run_command(cmd, desc):
                success = False
                if args.fail_fast:
                    break

    elif args.mode == "type":
        # Run type checking
        cmd = ["python", "-m", "mypy", "vep_mcp/"]
        success = run_command(cmd, "Type Checking")

    elif args.mode == "ci":
        # Run full CI pipeline
        commands = [
            (["python", "-m", "ruff", "check", "vep_mcp/"], "Linting"),
            (["python", "-m", "mypy", "vep_mcp/"], "Type Checking"),
            (pytest_args + ["-m", "not integration"], "Unit Tests"),
        ]

        for cmd, desc in commands:
            if not run_command(cmd, desc):
                success = False
                if args.fail_fast:
                    break

    # Summary
    print(f"\n{'='*60}")
    if success:
        print("✓ All operations completed successfully!")
        sys.exit(0)
    else:
        print("✗ Some operations failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
