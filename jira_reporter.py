"""
JIRA Reporter for Pytest
Creates JIRA issues for failed test cases with screenshots, videos, and logs
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JIRA Configuration
JIRA_CONFIG = {
    'base_url': os.getenv('JIRA_BASE_URL'),
    'email': os.getenv('JIRA_EMAIL'),
    'api_token': os.getenv('JIRA_API_SECRET') or os.getenv('JIRA_API_TOKEN'),  # Support both names
    'project_key': os.getenv('JIRA_PROJECT_KEY'),
    'issue_type': os.getenv('JIRA_ISSUE_TYPE', 'Bug')
}

# Paths
ARTIFACTS_DIR = Path('test_artifacts')
RESULTS_FILE = ARTIFACTS_DIR / 'test_results.json'
REPORTS_DIR = Path('reports')

class JiraReporter:
    def __init__(self):
        self.validate_config()
        self.auth = self._get_auth()
        self.created_issues = []
        
    def validate_config(self):
        """Validate JIRA configuration"""
        missing = [key for key, value in JIRA_CONFIG.items() if not value]
        
        if missing:
            print('[WARNING]  JIRA integration disabled - Missing configuration:')
            for key in missing:
                print(f'   - JIRA_{key.upper()}')
            print('   Please configure these variables in .env file')
            sys.exit(0)
        
        print('[OK] JIRA configuration validated')
    
    def _get_auth(self):
        """Get basic auth header"""
        credentials = f"{JIRA_CONFIG['email']}:{JIRA_CONFIG['api_token']}"
        return base64.b64encode(credentials.encode()).decode()
    
    def test_connection(self):
        """Test JIRA connection and project access"""
        print('\n[LINK] Testing JIRA connection...')
        
        try:
            # Test project access
            response = requests.get(
                f"{JIRA_CONFIG['base_url']}/rest/api/2/project/{JIRA_CONFIG['project_key']}",
                headers={
                    'Authorization': f"Basic {self.auth}",
                    'Accept': 'application/json'
                }
            )
            response.raise_for_status()
            project = response.json()
            print(f"[OK] Project found: {project['name']}")
            
            # Verify issue type
            issue_types_response = requests.get(
                f"{JIRA_CONFIG['base_url']}/rest/api/2/project/{JIRA_CONFIG['project_key']}",
                headers={
                    'Authorization': f"Basic {self.auth}",
                    'Accept': 'application/json'
                }
            )
            issue_types_response.raise_for_status()
            available_types = [it['name'] for it in issue_types_response.json()['issueTypes']]
            
            if JIRA_CONFIG['issue_type'] not in available_types:
                print(f"[ERROR] Issue type '{JIRA_CONFIG['issue_type']}' not found!")
                print(f"   Available types: {', '.join(available_types)}")
                sys.exit(1)
            
            print(f"[OK] Issue type '{JIRA_CONFIG['issue_type']}' is valid\n")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f'[ERROR] JIRA connection failed: {e}')
            if hasattr(e.response, 'json'):
                print(f'   Details: {e.response.json()}')
            sys.exit(1)
    
    def load_test_results(self):
        """Load test results from JSON file"""
        if not RESULTS_FILE.exists():
            print(f'[ERROR] Test results file not found: {RESULTS_FILE}')
            print('   Run tests first with: pytest ./tests -v --html=./reports/report.html')
            sys.exit(1)
        
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def attach_file(self, issue_key, file_path):
        """Attach file to JIRA issue"""
        if not Path(file_path).exists():
            return False
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (Path(file_path).name, f)}
                response = requests.post(
                    f"{JIRA_CONFIG['base_url']}/rest/api/2/issue/{issue_key}/attachments",
                    headers={
                        'Authorization': f"Basic {self.auth}",
                        'X-Atlassian-Token': 'no-check'
                    },
                    files=files
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"   [WARNING]  Could not attach {Path(file_path).name}: {e}")
            return False
    
    def create_issue_for_failure(self, test_result):
        """Create JIRA issue for a failed test"""
        test_name = test_result['test_name']
        error_msg = test_result.get('error_message', 'No error message')
        
        # Truncate error message for summary and remove newlines (JIRA doesn't allow newlines in summary)
        error_preview = error_msg[:100] + '...' if len(error_msg) > 100 else error_msg
        error_preview = error_preview.replace('\n', ' ').replace('\r', ' ')
        
        summary = f"[Automated Test Failure] {test_name} - {error_preview}"
        
        # Build description
        description = f"*Automated Test Failure Report*\n\n"
        description += f"*Test Name:* {test_name}\n"
        description += f"*Full Path:* {test_result['name']}\n"
        description += f"*Status:* [ERROR] FAILED\n"
        description += f"*Duration:* {test_result['duration']:.2f}s\n"
        description += f"*Timestamp:* {test_result['timestamp']}\n\n"
        description += f"----\n\n"
        description += f"*Error Message:*\n"
        description += f"{{code}}\n{error_msg}\n{{code}}\n\n"
        
        if test_result.get('error_traceback'):
            description += f"*Source Location:*\n"
            description += f"{{code}}\n{test_result['error_traceback']}\n{{code}}\n\n"
        
        description += f"----\n\n"
        description += f"*Attachments:*\n"
        if test_result.get('screenshot'):
            description += f"- [SCREENSHOT] Screenshot: {Path(test_result['screenshot']).name}\n"
        if test_result.get('video'):
            description += f"- [VIDEO] Video Recording: {Path(test_result['video']).name}\n"
        if test_result.get('log'):
            description += f"- [LOG] Detailed Log: {Path(test_result['log']).name}\n"
        
        # Check for HTML report
        html_report = REPORTS_DIR / 'report.html'
        if html_report.exists():
            description += f"- HTML Report: report.html\n"
        
        description += f"\n----\n\n"
        description += f"*Environment:*\n"
        description += f"- API: https://practice.expandtesting.com/notes/api\n"
        description += f"- Framework: Pytest + Appium\n"
        description += f"- Platform: Android (Pixel 4 API 29)\n"
        description += f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        # Create issue
        issue_data = {
            'fields': {
                'project': {
                    'key': JIRA_CONFIG['project_key']
                },
                'summary': summary,
                'description': description,
                'issuetype': {
                    'name': JIRA_CONFIG['issue_type']
                },
                'labels': ['automated-test', 'pytest', 'appium', 'api-test', 'mobile-test']
            }
        }
        
        try:
            print(f"\n[LOG] Creating issue for: {test_name}")
            
            response = requests.post(
                f"{JIRA_CONFIG['base_url']}/rest/api/2/issue",
                headers={
                    'Authorization': f"Basic {self.auth}",
                    'Content-Type': 'application/json'
                },
                json=issue_data
            )
            response.raise_for_status()
            
            issue_key = response.json()['key']
            issue_url = f"{JIRA_CONFIG['base_url']}/browse/{issue_key}"
            
            print(f"   [OK] Issue created: {issue_key}")
            
            # Attach files
            print(f"   [ATTACHED] Attaching files...")
            attachments = 0
            
            if test_result.get('screenshot'):
                if self.attach_file(issue_key, test_result['screenshot']):
                    attachments += 1
            
            if test_result.get('log'):
                if self.attach_file(issue_key, test_result['log']):
                    attachments += 1
            
            if test_result.get('video'):
                if self.attach_file(issue_key, test_result['video']):
                    attachments += 1
            
            # Attach HTML report
            if html_report.exists():
                if self.attach_file(issue_key, str(html_report)):
                    attachments += 1
            
            print(f"   [OK] {attachments} file(s) attached")
            print(f"   [LINK] Issue URL: {issue_url}\n")
            
            return {
                'success': True,
                'test': test_name,
                'key': issue_key,
                'url': issue_url
            }
            
        except requests.exceptions.RequestException as e:
            error_detail = e.response.json() if hasattr(e, 'response') else str(e)
            print(f"   [ERROR] Failed to create issue: {error_detail}\n")
            return {
                'success': False,
                'test': test_name,
                'error': error_detail
            }
    
    def process_results(self):
        """Process test results and create JIRA issues for failures"""
        print('\n[SEARCH] Processing test results...\n')
        
        results = self.load_test_results()
        
        # Count results
        total = len(results)
        passed = sum(1 for r in results if r['status'] == 'passed')
        failed = sum(1 for r in results if r['status'] == 'failed')
        
        print(f"[RESULTS] Test Results Summary:")
        print(f"   Total Tests: {total}")
        print(f"   [OK] Passed: {passed}")
        print(f"   [ERROR] Failed: {failed}\n")
        
        if failed == 0:
            print('[OK] All tests passed! No JIRA issues needed.\n')
            return
        
        # Create issues for failures
        print(f'[ALERT] Creating JIRA issues for {failed} failed test(s)...')
        
        failed_tests = [r for r in results if r['status'] == 'failed']
        
        for test in failed_tests:
            issue_result = self.create_issue_for_failure(test)
            self.created_issues.append(issue_result)
        
        # Summary
        success_count = sum(1 for i in self.created_issues if i['success'])
        failure_count = sum(1 for i in self.created_issues if not i['success'])
        
        print(f"\n{'='*80}")
        print(f"[RESULTS] JIRA Reporter Summary:")
        print(f"   Issues Created: {success_count}")
        print(f"   Failed: {failure_count}")
        print(f"{'='*80}\n")
        
        if success_count > 0:
            print("[OK] Successfully created issues:")
            for issue in self.created_issues:
                if issue['success']:
                    print(f"   - {issue['key']}: {issue['test']}")
                    print(f"     {issue['url']}")
        
        if failure_count > 0:
            print("\n[ERROR] Failed to create issues:")
            for issue in self.created_issues:
                if not issue['success']:
                    print(f"   - {issue['test']}")
            sys.exit(1)

def main():
    """Main execution"""
    print('\n' + '='*80)
    print('JIRA Reporter for Pytest - Appium Mobile Tests')
    print('='*80)
    
    reporter = JiraReporter()
    reporter.test_connection()
    reporter.process_results()
    
    print('[OK] JIRA reporting completed!\n')

if __name__ == '__main__':
    main()
