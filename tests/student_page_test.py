"""
Tests for the student view of the application

These are the end-to-end UI tests for student.html
"""

from playwright.sync_api import Page, expect
import pytest


@pytest.fixture(scope="function", autouse=True)
def before_each(page: Page):
    """Load the page before each test"""
    page.clock.install()
    page.goto("http://localhost:8000/student.html")


def test_student_input(page: Page):
    """Confirm that output text is visible"""

    textarea_locator = page.locator("#target-text")
    assert textarea_locator.is_visible()


def test_python_runs(page: Page):
    """
    Test that basic python code can execute
    """

    # 0. Insert name so page unlocks
    page.locator("#student-name").fill("Student1")
    page.locator("#start-button").click()

    textarea_locator = page.locator("#code-area")
    textarea_locator.fill('print("Hello, world!")')

    # 2. Click Run Button
    page.locator("#run-button").click()

    # 3. Assert desired output is
    expect(page.locator("#code-output")).to_have_text("Hello, world!", timeout=20000)


def test_check_output_correct(page: Page):
    """
    Test that the check output functionality works when the result of running the code
    matches the target output.
    """

    # 1. Put code in code area
    page.locator("#student-name").fill("Student1")
    page.locator("#start-button").click()

    codearea_locator = page.locator("#code-area")
    codearea_locator.fill("print('Hello World!')")

    # 2. Put code in Desired output
    targettext_locator = page.locator("#target-text")
    targettext_locator.evaluate("element => element.removeAttribute('disabled')")
    targettext_locator.fill("Hello World!")

    # 3. Click Run Button
    page.locator("#run-button").click()

    # 4. Check Output
    expect(page.locator("#check-code-result")).to_contain_text(
        "Correct   ✔", timeout=20000
    )


def test_check_output_incorrect(page: Page):
    """
    Test that the check output functionality works when the result of running the code
    does not match the target output.
    """

    # 1. Put code in code area
    page.locator("#student-name").fill("Student1")
    page.locator("#start-button").click()

    codearea_locator = page.locator("#code-area")
    codearea_locator.fill("print('Hello Word')")

    # 2. Put code in Desired output
    targettext_locator = page.locator("#target-text")
    targettext_locator.evaluate("element => element.removeAttribute('disabled')")
    targettext_locator.fill("Hello World!")

    # 3. Click Run Button
    page.locator("#run-button").click()

    # 4. Check Output
    expect(page.locator("#check-code-result")).to_contain_text(
        "Does not match target output   ❌", timeout=20000
    )


def test_error_message_displayed(page: Page):
    """
    Test that an error message is displayed when there is an execution error.
    """
    page.locator("#student-name").fill("Student1")
    page.locator("#start-button").click()

    textarea_locator = page.locator("#code-area")
    textarea_locator.fill("print('Hello world'")  # Missing closing parenthesis

    page.locator("#run-button").click()

    # Use expect to wait until the error message appears
    error_locator = page.locator("#code-output")
    expect(error_locator).to_contain_text("Error:", timeout=20000)


def test_results_page(page: Page):
    """
    Test student page switches between coding view and stats view.
    """

    # 1. switch to stats view
    page.locator("#student-name").fill("Student1")
    page.locator("#start-button").click()

    page.locator("#switch").click()

    # 2. check that stats is on page
    expect(page.locator("#students-started")).to_have_text("1/10", timeout=20000)


def test_timer(page: Page):
    """
    Test that the timer runs when a name is entered && start-button is clicked
    and stops when the correct output is found
    """

    expect(page.locator("#timer_val")).to_have_text("00:00:00")
    page.clock.run_for(5000)
    start_time = page.locator("#timer_val").inner_text()
    expect(page.locator("#timer_val")).to_have_text(start_time)

    page.locator("#student-name").fill("Student1")
    page.locator("#start-button").click()
    # Check timer after 13 seconds
    page.clock.run_for(11000)
    expect(page.locator("#timer_val")).to_have_text("00:00:13")

    # Check timer after 1 minute
    page.clock.run_for(46000)
    expect(page.locator("#timer_val")).to_have_text("00:01:00")

    # Check that timer stops when correct answer is found

    codearea_locator = page.locator("#code-area")
    codearea_locator.fill("print('Hello World')")

    targettext_locator = page.locator("#target-text")
    targettext_locator.evaluate("element => element.removeAttribute('disabled')")
    targettext_locator.fill("Hello World!")
    page.locator("#run-button").click()

    prev_time = page.locator("#timer_val")
    page.clock.run_for(5000)
    expect(page.locator("#timer_val")).to_have_text(prev_time.inner_text())


def test_infinite_loop_error_message(page: Page):
    """
    Test that an infinite loop is detected and feedback is given to the user.
    """
    # 0. Insert name so page unlocks
    page.locator("#student-name").fill("Student1")
    page.locator("#start-button").click()

    textarea_locator = page.locator("#code-area")
    textarea_locator.fill(
        """
    while True:
        pass
    """
    )

    page.locator("#run-button").click()

    # Wait for the error message to appear in the output
    error_locator = page.locator("#code-output")

    # Use expect to check if the error message appears
    expect(error_locator).to_contain_text(
        "Error: Execution timed out. Possible infinite loop detected.", timeout=21000
    )
