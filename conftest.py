import pytest
import os
import json
from datetime import datetime
from pathlib import Path
import base64

# Create directories for test artifacts
ARTIFACTS_DIR = Path("test_artifacts")
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
LOGS_DIR = ARTIFACTS_DIR / "logs"

for directory in [ARTIFACTS_DIR, SCREENSHOTS_DIR, VIDEOS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Store test results for JIRA reporting
test_results = []

def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    config.addinivalue_line(
        "markers", "jira: mark test to create JIRA issue on failure"
    )

# VIDEO RECORDING DISABLED - Not working reliably
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_setup(item):
#     """Start video recording before test execution"""
#     # Start video recording if driver fixture is available
#     if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
#         driver = item.funcargs['driver']
#         try:
#             # Start screen recording (max 180 seconds = 3 minutes for Android)
#             driver.start_recording_screen()
#             setattr(item, 'video_recording_started', True)
#             print(f"\n[VIDEO] Video recording started for: {item.name}")
#         except Exception as e:
#             print(f"\n[WARNING]  Could not start video recording: {e}")
#             setattr(item, 'video_recording_started', False)
#     
#     yield

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results and create artifacts on failure"""
    outcome = yield
    report = outcome.get_result()
    
    # Only process test call phase (not setup/teardown)
    if report.when == "call":
        test_info = {
            "name": item.nodeid,
            "test_name": item.name,
            "status": report.outcome,
            "duration": report.duration,
            "timestamp": datetime.now().isoformat(),
            "screenshot": None,
            "video": None,
            "log": None,
            "error_message": None,
            "error_traceback": None
        }
        
        if report.failed:
            # Capture error information
            if call.excinfo:
                test_info["error_message"] = str(call.excinfo.value)
                test_info["error_traceback"] = str(call.excinfo.traceback[0].source)  # Convert to string for JSON serialization
            
            # Try to capture screenshot and video from driver
            if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
                driver = item.funcargs['driver']
                
                # Capture screenshot
                try:
                    screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    screenshot_path = SCREENSHOTS_DIR / screenshot_name
                    driver.save_screenshot(str(screenshot_path))
                    test_info["screenshot"] = str(screenshot_path)
                    print(f"\n[SCREENSHOT] Saved: {screenshot_path}")
                except Exception as e:
                    print(f"\n[WARNING] Could not capture screenshot: {e}")
                
                # VIDEO RECORDING DISABLED - Not working reliably
                # # Stop and save video recording
                # if getattr(item, 'video_recording_started', False):
                #     try:
                #         video_data = driver.stop_recording_screen()
                #         video_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                #         video_path = VIDEOS_DIR / video_name
                #         
                #         # Decode base64 video data and save
                #         with open(video_path, 'wb') as f:
                #             f.write(base64.b64decode(video_data))
                #         
                #         test_info["video"] = str(video_path)
                #         print(f"[VIDEO] Saved: {video_path}")
                #     except Exception as e:
                #         print(f"[WARNING] Could not save video: {e}")
        # else:
            # VIDEO RECORDING DISABLED - Not working reliably
            # # Test passed - stop recording but don't save
            # if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            #     driver = item.funcargs['driver']
            #     if getattr(item, 'video_recording_started', False):
            #         try:
            #             driver.stop_recording_screen()
            #             print(f"\n[VIDEO] Recording stopped (test passed, not saved)")
            #         except Exception as e:
            #             pass  # Ignore errors when stopping video for passed tests
        
        # Save detailed log only for failures
        if report.failed:
            log_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_path = LOGS_DIR / log_name
            
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(f"Test: {item.nodeid}\n")
                f.write(f"Status: {report.outcome}\n")
                f.write(f"Duration: {report.duration}s\n")
                f.write(f"Timestamp: {datetime.now()}\n")
                f.write(f"\n{'='*80}\n")
                f.write(f"ERROR MESSAGE:\n")
                f.write(f"{'='*80}\n")
                f.write(f"{test_info['error_message']}\n")
                f.write(f"\n{'='*80}\n")
                f.write(f"TRACEBACK:\n")
                f.write(f"{'='*80}\n")
                if report.longrepr:
                    f.write(str(report.longrepr))
            
            test_info["log"] = str(log_path)
            print(f"[LOG] Saved: {log_path}")
        
        test_results.append(test_info)
        
        # Store in item for access in other hooks
        setattr(item, 'test_result', test_info)

def pytest_sessionfinish(session, exitstatus):
    """Save test results to JSON file at end of session"""
    results_file = ARTIFACTS_DIR / "test_results.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[RESULTS] Test results saved to: {results_file}")
    
    # Print summary
    total = len(test_results)
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    
    print(f"\n{'='*80}")
    print(f"Test Summary: {total} total | [OK] {passed} passed | [ERROR] {failed} failed")
    print(f"{'='*80}\n")
