# tests/test_ui_pages.py
from playwright.sync_api import Page, expect
from datetime import datetime
import test_report

def test_toggle_all_leds(page: Page):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page.goto("file:///C:/multiplay/tests/test-play.html")
    for i in range(1, 11):
        btn = page.locator(f"#btn{i}")
        led = page.locator(f"#led{i}")
        try:
            btn.click()
            expect(led).to_have_css("background-color", "rgb(0, 128, 0)")
            btn.click()
            expect(led).to_have_css("background-color", "rgb(128, 128, 128)")
            status = "Passed"
        except AssertionError:
            status = "Failed"
        test_report.all_results.append(["LED Page", f"LED {i}", status, ts])

def test_login_page(page: Page):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page.goto("file:///C:/multiplay/tests/test_login.html")
    try:
        page.fill("#username", "admin")
        page.fill("#password", "1234")
        page.click("button")
        expect(page.locator("#msg")).to_have_text("✅ Login Successful!")
        page.fill("#username", "user")
        page.fill("#password", "wrong")
        page.click("button")
        expect(page.locator("#msg")).to_have_text("❌ Invalid Credentials!")
        status = "Passed"
    except AssertionError:
        status = "Failed"
    test_report.all_results.append(["Login Page", "Login Test", status, ts])

def test_form_page(page: Page):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page.goto("file:///C:/multiplay/tests/test_form.html")
    try:
        page.fill("#name", "Reshma")
        page.fill("#age", "21")
        page.select_option("#gender", "Female")
        page.click("button")
        expect(page.locator("#output")).to_have_text("✅ Submitted: Reshma, Age: 21, Gender: Female")
        status = "Passed"
    except AssertionError:
        status = "Failed"
    test_report.all_results.append(["Form Page", "Form Test", status, ts])
