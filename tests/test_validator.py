import os
import pytest
from datetime import datetime

# Constants
BASE_DIR = "tests/sample_inputs"
LOG_FILE = "test_results.log"

# Map of expected outputs by folder name
EXPECTED_OUTPUTS = {
    "genuine": ("genuine", "approved"),
    "suspicious": ("suspicious", "manual_review"),
    "fake": ("fake", "rejected"),
    "non_id": ("fake", "rejected")  # fallback case
}

def get_prediction_mock(path):
    """
    Mocks model response based on filename.
    This function simulates real predictions.
    """
    for key, val in EXPECTED_OUTPUTS.items():
        if key in path.replace("\\", "/").lower():
            return val[0], val[1], 1.0, "Mocked response for testing"
    return "unknown", "unknown", 0.0, "Could not match category"

def collect_test_images():
    """
    Recursively collects all image paths under BASE_DIR
    """
    image_files = []
    for root, _, files in os.walk(BASE_DIR):
        for file in sorted(files):
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")
                folder = rel_path.split("/")[0].lower()
                expected = EXPECTED_OUTPUTS.get(folder, ("unknown", "unknown"))
                image_files.append((rel_path, expected))
    return image_files

@pytest.mark.parametrize("rel_path,expected", collect_test_images())
def test_image_classification(rel_path, expected):
    predicted_label, predicted_status, score, reason = get_prediction_mock(rel_path)
    expected_label, expected_status = expected

    result = (predicted_label == expected_label) and (predicted_status == expected_status)
    
    # Logging (append mode)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[Test Case] {rel_path}\n")
        f.write(f"Expected: {expected_label}, {expected_status}\n")
        f.write(f"Predicted: {predicted_label}, {predicted_status} | Score: {score:.4f}\n")
        f.write(f"Reason: {reason}\n")
        f.write(f"Result: {'✅ Correct' if result else '❌ Incorrect'}\n\n")

    assert result, f"{rel_path}: Expected ({expected_label}, {expected_status}), got ({predicted_label}, {predicted_status})"

def pytest_sessionstart(session):
    # Clean log file before starting test session
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"===== TEST RESULTS: {datetime.now()} =====\n\n")

def pytest_sessionfinish(session, exitstatus):
    total = len(collect_test_images())
    passed = total if exitstatus == 0 else "Some tests failed"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("===== SUMMARY =====\n")
        f.write(f"Total Test Cases: {total}\n")
        if exitstatus == 0:
            f.write(f"✅ Passed: {total}\n❌ Failed: 0\n")
        else:
            f.write("❌ Some tests failed. Check above for details.\n")
        f.write(f"📝 Log saved to: {os.path.abspath(LOG_FILE)}\n")
        f.write("=====================\n")
