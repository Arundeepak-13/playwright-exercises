import pytest
from pathlib import Path
from playwright.async_api import async_playwright, expect

PROJECT_ROOT = Path(__file__).resolve().parents[3]
TEST_DATA = PROJECT_ROOT / "test-data"
WHATSAPP_PROFILE = PROJECT_ROOT / "whatsapp-profile"


#Parameterized test
@pytest.mark.parametrize(
    "file_name",
    [
        "valid.jpg",
        "Git.pdf",
        "valid.txt"
    ]
)
@pytest.mark.asyncio
async def test_whatsapp_file_upload(file_name):

    async with async_playwright() as p:


        context = await p.chromium.launch_persistent_context(user_data_dir=WHATSAPP_PROFILE,headless=False)
        page = await context.new_page()
        await page.goto("https://web.whatsapp.com")
        await page.wait_for_timeout(10000)
        await page.get_by_text("Deep",exact=True).click()
        await page.wait_for_timeout(3000)



        print(f"Uploading: {file_name}")
        file_path = TEST_DATA / file_name
        assert file_path.exists(), (f"File not found: {file_path}")
        await page.get_by_role("button",name="Attach").click()
        await page.wait_for_timeout(1000)


        if file_name.endswith(".jpg"):
            await page.get_by_text("Photos & videos",exact=True).click()
        else:
            await page.get_by_text("Document",exact=True).click()
        await page.wait_for_timeout(1000)



        file_input = page.locator("input[type='file']").last
        await file_input.set_input_files(file_path)
        print(f"{file_name} selected")
        await page.wait_for_timeout(3000)

    
        send_button = page.get_by_role("button",name="Send 1 selected")
        await expect(send_button).to_be_visible(timeout=10000)
        await send_button.click()
        await page.wait_for_timeout(5000)
        print(f"{file_name} sent successfully")
        await context.close()

