import os, re, json, glob, html
from datetime import datetime
from utils.report_generator import ExcelReportGenerator, TestResult

# Map school_id to descriptive test case names
TEST_CASE_NAMES = {
    "SCH001": "Complete preliminary form submission for School 001",
    "SCH002": "Complete preliminary form submission for School 002",
    "SCH003": "Login with invalid credentials shows error",
    "SCH004": "Complete preliminary form submission for School 004",
    "SCH005": "Complete preliminary form submission for School 005",
}


def extract_json_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'data-jsonblob="([^"]*)"', content)
    if not match:
        raise ValueError("Could not find test data in HTML report.")
    json_str = html.unescape(match.group(1))
    return json.loads(json_str)


def find_screenshot_for_test(test_id):
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        return ""
    pattern = os.path.join(screenshot_dir, f"{test_id}_*.png")
    matching_files = glob.glob(pattern)
    if matching_files:
        matching_files.sort(reverse=True)
        return matching_files[0]
    return ""


def extract_error_summary(log_text):
    if not log_text:
        return ""
    lines = log_text.split("\n")
    error_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("E "):
            clean = stripped[2:].strip()
            if "::" not in clean and clean:
                error_lines.append(clean)
    if error_lines:
        return error_lines[0][:500]
    for line in lines:
        if "Error:" in line or "Exception:" in line:
            return line.strip()[:500]
    return "Test failed - see detailed log"


def parse_duration_to_seconds(duration_str):
    try:
        parts = duration_str.split(":")
        if len(parts) == 3:
            h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
            return h * 3600 + m * 60 + s
        elif len(parts) == 2:
            m, s = int(parts[0]), int(parts[1])
            return m * 60 + s
    except (ValueError, IndexError):
        pass
    return 0.0


def get_test_case_name(test_id, fallback_name):
    return TEST_CASE_NAMES.get(test_id, fallback_name)


def main():
    html_path = "reports/report.html"
    if not os.path.exists(html_path):
        print(f"ERROR: HTML report not found at '{html_path}'")
        return

    print("Parsing HTML report...")
    data = extract_json_from_html(html_path)
    tests = data.get("tests", {})
    print(f"Found {len(tests)} test(s) in report.")

    generator = ExcelReportGenerator()
    generator.set_start_time()

    for test_node_id, test_results in tests.items():
        for result_entry in test_results:
            test_id = "UNKNOWN"
            browser_name = "chromium"

            bracket_match = re.search(r'\[([^\]]+)\]', test_node_id)
            if bracket_match:
                param_value = bracket_match.group(1)
                if "-" in param_value:
                    parts = param_value.split("-", 1)
                    browser_name = parts[0]
                    test_id = parts[1]
                else:
                    test_id = param_value
            else:
                test_id = test_node_id.split("::")[-1]

            raw_name = test_node_id.split("::")[-1] if "::" in test_node_id else test_node_id
            test_name = get_test_case_name(test_id, raw_name)

            status_raw = result_entry.get("result", "").lower()
            status = "PASS" if status_raw == "passed" else "FAIL"

            duration_str = result_entry.get("duration", "00:00:00")
            execution_time = parse_duration_to_seconds(duration_str)

            error_message = ""
            screenshot_path = ""
            if status == "FAIL":
                log_text = result_entry.get("log", "")
                error_message = extract_error_summary(log_text)
                screenshot_path = find_screenshot_for_test(test_id)

            test_result = TestResult(
                test_id=test_id,
                test_name=test_name,
                status=status,
                error_message=error_message,
                screenshot_path=screenshot_path,
                execution_time=execution_time,
                browser_name=browser_name,
            )
            generator.add_result(test_result)

    generator.set_end_time()

    if generator.results:
        report_path = generator.generate_report()
        print(f"\nDone! Report saved to: {os.path.abspath(report_path)}")
    else:
        print("\nNo test results found in the HTML report.")


if __name__ == "__main__":
    main()
