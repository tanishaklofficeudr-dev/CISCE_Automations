"""
conftest.py - Pytest Configuration & Hooks
============================================
Integrates the Excel Report Generator with pytest execution lifecycle.
"""

import os
import sys
import glob
import time
import json
from datetime import datetime
import shutil
import subprocess
import pytest

# Add project root to path so utils can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.report_generator import ExcelReportGenerator, TestResult

# Global report generator instance
report_generator = ExcelReportGenerator()


# ============================================================================
# VIDEO RECORDING CONFIGURATION
# ============================================================================
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Enable video recording for all tests."""
    os.makedirs("recordings", exist_ok=True)
    return {
        **browser_context_args,
        "record_video_dir": "recordings",
        "record_video_size": {"width": 1280, "height": 720},
    }



def pytest_sessionstart(session):
    """Record session start time and preserve allure history for trend analysis."""
    report_generator.set_start_time()

    # Auto-copy allure history for trend analysis (no manual step needed)
    allure_report_history = os.path.join("allure-report", "history")
    allure_results_history = os.path.join("allure-results", "history")

    if os.path.exists(allure_report_history):
        os.makedirs(allure_results_history, exist_ok=True)
        for item in os.listdir(allure_report_history):
            src = os.path.join(allure_report_history, item)
            dst = os.path.join(allure_results_history, item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)

    # Create executor.json with timestamp for trend chart x-axis labels
    os.makedirs("allure-results", exist_ok=True)
    timestamp = datetime.now().strftime("%d-%b-%Y %H:%M")
    executor_data = {
        "name": "Local Machine",
        "type": "local",
        "buildName": timestamp,
        "buildOrder": int(datetime.now().timestamp()),
        "reportName": f"Test Run - {timestamp}"
    }
    with open(os.path.join("allure-results", "executor.json"), "w") as f:
        json.dump(executor_data, f, indent=2)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture results from each test after the 'call' phase.
    Extracts test ID, status, error info, screenshot, and timing.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Extract test case ID from parametrize marker
        test_id = _extract_test_id(item)
        test_name = item.name
        browser_name = _get_browser_name(item)
        execution_time = report.duration

        if report.passed:
            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                status="PASS",
                error_message="",
                screenshot_path="",
                execution_time=execution_time,
                browser_name=browser_name,
            )
        elif report.failed:
            error_message = _extract_error_message(report)
            screenshot_path = _find_screenshot_for_test(test_id)

            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                error_message=error_message,
                screenshot_path=screenshot_path,
                execution_time=execution_time,
                browser_name=browser_name,
            )
        else:
            result = TestResult(
                test_id=test_id,
                test_name=test_name,
                status="FAIL",
                error_message=f"SKIPPED: {report.longrepr}",
                screenshot_path="",
                execution_time=execution_time,
                browser_name=browser_name,
            )

        report_generator.add_result(result)


def pytest_sessionfinish(session, exitstatus):
    """Generate the Excel report and Allure report after all tests complete."""
    report_generator.set_end_time()

    if report_generator.results:
        report_generator.generate_report()
    else:
        print("\n[Excel Report] No test results collected. Skipping report generation.")

    # Auto-generate Allure report if allure-results exists
    allure_results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allure-results")
    if os.path.exists(allure_results_dir) and os.listdir(allure_results_dir):
        try:
            subprocess.run(
                ["allure", "generate", "allure-results", "--clean", "-o", "allure-report"],
                capture_output=True, text=True, timeout=30, shell=True
            )
            print("\n" + "=" * 60)
            print("  ALLURE REPORT GENERATED SUCCESSFULLY")
            print("  View: allure open allure-report --port 9090")
            print("=" * 60 + "\n")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("\n[Allure] Could not auto-generate report. Run manually: allure generate allure-results --clean -o allure-report")


def _extract_test_id(item):
    """Extract test case ID from parametrized test name."""
    if "[" in item.name and "]" in item.name:
        param_value = item.name.split("[")[1].rstrip("]")
        # Handle 'chromium-SCH007' format
        if "-" in param_value:
            return param_value.split("-", 1)[1]
        return param_value
    return item.name


def _get_browser_name(item):
    """Extract browser name from test configuration."""
    if "[" in item.name and "-" in item.name:
        param_value = item.name.split("[")[1].rstrip("]")
        if "-" in param_value:
            return param_value.split("-", 1)[0]
    try:
        browser = item.config.getoption("--browser", default=None)
        if browser:
            if isinstance(browser, list):
                return browser[0] if browser else "chromium"
            return browser
    except (ValueError, AttributeError):
        pass
    return "chromium"


def _extract_error_message(report):
    """Extract a clean error message from a failed test report."""
    if report.longrepr:
        longrepr_str = str(report.longrepr)
        lines = longrepr_str.strip().split("\n")
        # Find lines starting with E (pytest error lines)
        e_lines = [l.strip()[2:].strip() for l in lines if l.strip().startswith("E ")]
        if e_lines:
            return e_lines[0][:500]
        # Fallback
        error_lines = [l for l in lines if l.strip() and not l.startswith(" ")]
        if error_lines:
            return error_lines[-1].strip()[:500]
        return longrepr_str[-500:]
    return "Unknown error"


def _find_screenshot_for_test(test_id):
    """Find the most recent screenshot for a given test ID."""
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        return ""
    pattern = os.path.join(screenshot_dir, f"{test_id}_*.png")
    matching_files = glob.glob(pattern)
    if matching_files:
        matching_files.sort(reverse=True)
        return matching_files[0]
    return ""
