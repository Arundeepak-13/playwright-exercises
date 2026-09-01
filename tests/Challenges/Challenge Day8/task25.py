import pytest
from playwright.async_api import async_playwright, expect


BASE_URL = "https://practicesoftwaretesting.com"


@pytest.mark.asyncio
async def test_browser_history_navigation():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
  
        #Start from Home Page
        await page.goto(BASE_URL)
        await expect(page).to_have_url(BASE_URL + "/")
        await expect(page.locator("[data-test='product-name']").first).to_be_visible()


        #Click product 1
        product1 = page.locator("[data-test='product-name']").nth(0)
        product1_name = await product1.inner_text()
        await product1.click()
        product1_heading = page.locator("[data-test='product-name']")
        await expect(product1_heading).to_be_visible()
        await expect(product1_heading).to_have_text(product1_name)
        product1_url = page.url
        print("Product 1:", product1_name)
        print("Product 1 URL:", product1_url)


        #Go Back to Home
        await page.go_back()
        await expect(page).to_have_url(BASE_URL + "/")
        await expect(page.locator("[data-test='product-name']").first).to_be_visible()
        print("BACK → Home:", page.url)


        #Click Product 2
        product2 = page.locator("[data-test='product-name']").nth(1)
        product2_name = await product2.inner_text()
        await product2.click()
        product2_heading = page.locator("[data-test='product-name']")
        await expect(product2_heading).to_be_visible()
        await expect(product2_heading).to_have_text(product2_name)
        product2_url = page.url
        print("Product 2:", product2_name)
        print("Product 2 URL:", product2_url)


        # BONUS — Refresh Product 2
        await page.reload()
        await expect(page).to_have_url(product2_url)
        await expect(page.locator("[data-test='product-name']")).to_have_text(product2_name)
        print("Product 2 after refresh:", page.url)


        #Navigate another section
        await page.get_by_text("Categories").click()
        await page.get_by_text("Power Tools",exact=True).click()
        power_tools_url = page.url
        await expect(page).to_have_url(f"{BASE_URL}/category/power-tools")
        await expect(page.get_by_role("heading",name="Category: Power Tools")).to_be_visible()
        print("Section:", power_tools_url)


        # Back -> Power Tools -> Product 2
        await page.go_back()
        await expect(page).to_have_url(product2_url)
        await expect(page.locator("[data-test='product-name']")).to_have_text(product2_name)
        print("BACK 1 → Product 2:", page.url)

  
        # Back -> Product 2 -> Home
        await page.go_back()
        await expect(page).to_have_url(BASE_URL + "/")
        await expect(page.locator("[data-test='product-name']").first).to_be_visible()
        print("BACK 2 → Home:", page.url)


        # Back -> Home -> Browser Start
        await page.go_back()
        await expect(page).to_have_url("about:blank")
        print("BACK 3 → Browser Start:", page.url)

    
        # Forward -> Browser Start -> Home
        await page.go_forward()
        await expect(page).to_have_url(BASE_URL + "/")
        await expect(page.locator("[data-test='product-name']").first).to_be_visible()
        print("FORWARD 1 → Home:", page.url)


        # Forward -> Home -> Product 2
        await page.go_forward()
        await expect(page).to_have_url(product2_url)
        await expect(page.locator("[data-test='product-name']")).to_have_text(product2_name)
        print("FORWARD 2 → Product 2:", page.url)


        #Forward ->  Product 2 -> Power Tools
        await page.go_forward()
        await expect(page).to_have_url(f"{BASE_URL}/category/power-tools")
        await expect(page.get_by_role("heading",name="Category: Power Tools")).to_be_visible()
        print("FORWARD 3 → Power Tools:", page.url)
        await browser.close()