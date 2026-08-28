import random

import pytest
from playwright.async_api import async_playwright, expect


BASE_URL = "https://practicesoftwaretesting.com"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"


# TEST 1 — PRODUCT SEARCH
@pytest.mark.asyncio
async def test_product_search():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(BASE_URL)

            # Search for Hammer
            search_box = page.get_by_placeholder("Search")
            await search_box.fill("Hammer")
            await page.get_by_role("button",name="Search").click()

            # Verify Hammer appears
            await expect(page.get_by_text("Hammer",exact=True).first).to_be_visible()
            print("Product Search: PASS")

        finally:
            await context.close()
            await browser.close()



# TEST 2 — PRODUCT DETAILS

@pytest.mark.asyncio
async def test_product_details():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(BASE_URL)

            # Search for Hammer
            await page.get_by_placeholder("Search").fill("Hammer")
            await page.get_by_role("button",name="Search").click()


            # Open Thor Hammer
            product = page.get_by_role("link",name="Thor Hammer",exact=False)
            await expect(product).to_be_visible()
            await product.click()

            # Verify product name
            await expect(page.get_by_role("heading",name="Thor Hammer",exact=True)).to_be_visible()

            # Verify price
            await expect(page.get_by_text("$11.14",exact=True)).to_be_visible()

            # Verify description
            await expect(page.get_by_text("The legendary Thor Hammer combines premium craftsmanship",exact=False)).to_be_visible()

            # Verify Add to Cart button
            await expect(page.get_by_role("button",name="Add to cart",exact=True)).to_be_visible()
            print("Product Details: PASS")

        finally:
            await context.close()
            await browser.close()



# TEST 3 — CATEGORY
@pytest.mark.asyncio
async def test_product_category():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(BASE_URL)

            # Open Categories
            await page.locator('button[data-test="nav-categories"]').click()

            print("Category menu is displayed")

            # Select Power Tools
            power_tools = page.locator('a[data-test="nav-power-tools"]')

            # Verify category option is visible
            await expect(power_tools).to_be_visible()
            await power_tools.click()

            # Verify Power Tools URL
            await expect(page).to_have_url(f"{BASE_URL}/category/power-tools")
            print("Selected category: Power Tools")

            # Get products
            products = page.locator(".card")

            # Verify products are displayed
            await expect(products.first).to_be_visible()

            product_count = await products.count()

            assert product_count > 0, \
                "No products are displayed"

            print("Number of Power Tools products:",product_count)

            # Verify all displayed products
            for i in range(product_count):
                product = products.nth(i)
                await expect(product).to_be_visible()
                product_name = await product.locator("h5").inner_text()
                print("Power Tools product:",product_name)

            print("Category validation: PASS")

        finally:
            await context.close()
            await browser.close()


# TEST 4 — REGISTRATION

@pytest.mark.asyncio
async def test_registration():

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:

            # Open registration page
            await page.goto(REGISTER_URL)

            await expect(page.locator('[data-test="register-form"]')).to_be_visible()

            # Generate unique email using random integer
            random_number = random.randint(
                100000,
                999999
            )

            unique_email = (f"testuser_{random_number}@gmail.com")

            print("Registration email:",unique_email)

            # Fill registration details

            await page.locator('[data-test="first-name"]').fill("arun")

            await page.locator('[data-test="last-name"]').fill("deepak")

            await page.locator('[data-test="dob"]').fill("2003-03-13")

            await page.locator('[data-test="country"]').select_option("IN")

            await page.locator('[data-test="postal_code"]').fill("630606")

            await page.locator('[data-test="house_number"]').fill("32-e")

            # Wait for address lookup
            address_lookup = page.get_by_text("Looking up your address...")

            if await address_lookup.is_visible():
                await address_lookup.wait_for(
                    state="hidden"
                )

            await page.locator('[data-test="street"]').fill("pookkara street")

            await page.locator('[data-test="city"]').fill("manamadurai")

            await page.locator('[data-test="state"]').fill("tamilnadu")

            await page.locator('[data-test="phone"]').fill("8870618311")

            await page.locator('[data-test="email"]').fill(unique_email)

            await page.locator('[data-test="password"]').fill("Volleyball*1303")

            # Click Register
            await page.locator('[data-test="register-submit"]').click()

            # Verify successful registration
            await expect(page).to_have_url(LOGIN_URL)

            print("Registration: PASS")

        finally:
            await context.close()
            await browser.close()