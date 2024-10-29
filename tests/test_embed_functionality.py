from playwright.sync_api import Page, expect
import os

# Get the current working directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_name = "www/index.html"
full_path = "file://" + os.path.join(project_root, file_name)

def test_embed_code_generation(page: Page):
    # Step 1: Navigate to the index.html page
    page.goto(full_path)


    # Step 2: Fill the necessary fields
    page.fill('#code-area', 'Sample code')  # Fill the code area with sample code
    page.fill('#output-text', 'Sample output')  # Fill the output text area with sample output


    # Step 3: Click the Share button
    page.click('#share')  # Interacts with the button by its ID


    # Step 4: Wait for the embed code to appear in the textarea
    embed_code_display = page.locator('#embed-code')  # Ensure this matches your HTML structure
    expect(embed_code_display).to_be_visible()  # Ensure the embed code textarea is visible


    # Step 5: Verify that the embed code is correct
    # Generate the expected URL based on the inputs
    expected_url = page.evaluate("""location.origin + location.pathname + "student.html#" + btoa(JSON.stringify(["Sample code", "Sample output"]))""")
    # Construct the expected embed code
    expected_embed_code = f'<iframe src="{expected_url}" width="100%" height="800" frameborder="0" allowfullscreen></iframe>'

    # Assert that the displayed embed code matches the expected embed code
    expect(embed_code_display).to_have_value(expected_embed_code)