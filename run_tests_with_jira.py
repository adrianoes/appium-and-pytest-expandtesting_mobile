"""
Run Pytest tests and automatically create JIRA issues for failures
One bug per failed test with screenshots and logs attached

Usage:
    python run_tests_with_jira.py                    # Run all tests
    python run_tests_with_jira.py -k create_user     # Run tests matching 'create_user'
    python run_tests_with_jira.py -k "login or user" # Run tests matching 'login' or 'user'
"""

import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run pytest with HTML report generation"""
    print("\n" + "="*80)
    print("Running Pytest Tests...")
    print("="*80 + "\n")
    
    # Build pytest command
    pytest_cmd = ["pytest", "./tests", "-v", "--html=./reports/report.html"]
    
    # Check if -k option is provided
    if len(sys.argv) > 1:
        # Pass all arguments after the script name to pytest
        pytest_cmd.extend(sys.argv[1:])
        print(f"Filter applied: {' '.join(sys.argv[1:])}\n")
    
    # Run pytest
    result = subprocess.run(pytest_cmd, capture_output=False)
    
    return result.returncode

def create_jira_issues():
    """Run JIRA reporter to create issues for failures"""
    print("\n" + "="*80)
    print("Creating JIRA Issues for Failures...")
    print("="*80 + "\n")
    
    # Check if test results exist
    results_file = Path("test_artifacts/test_results.json")
    if not results_file.exists():
        print("⚠️  No test results found. Tests may not have run properly.")
        return 1
    
    # Run JIRA reporter
    result = subprocess.run(
        [sys.executable, "jira_reporter.py"],
        capture_output=False
    )
    
    return result.returncode

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("AUTOMATED TEST EXECUTION WITH JIRA INTEGRATION")
    print("="*80)
    
    # Step 1: Run tests
    test_exit_code = run_tests()
    
    # Step 2: Create JIRA issues (regardless of test outcome)
    jira_exit_code = create_jira_issues()
    
    # Final summary
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(f"Tests Exit Code: {test_exit_code} {'(PASSED)' if test_exit_code == 0 else '(FAILED)'}")
    print(f"JIRA Reporter Exit Code: {jira_exit_code} {'(SUCCESS)' if jira_exit_code == 0 else '(FAILED)'}")
    print("="*80 + "\n")
    
    # Exit with test exit code (so CI/CD knows if tests failed)
    sys.exit(test_exit_code)

if __name__ == '__main__':
    main()
