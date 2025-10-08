# conftest.py
import pytest
from pathlib import Path
from datetime import datetime
import test_report

@pytest.fixture(scope="session", autouse=True)
def generate_report_at_end():
    # Run tests, then generate report
    yield
    test_report.generate_pdf_report()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # capture the test result, and if failed, try to take a screenshot from 'page' fixture
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = reports_dir / f"{item.name}_{ts}.png"
            # sync API - page.screenshot is allowed in Playwright sync API
            page.screenshot(path=str(screenshot_path))
            # add an entry to the report (so PDF lists it)
            test_report.all_results.append([item.location[0], f"Screenshot saved: {screenshot_path}", "FAIL", ts])
