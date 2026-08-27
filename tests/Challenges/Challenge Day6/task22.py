import asyncio
from playwright.async_api import async_playwright, expect

products = [
    "Combination Pliers",
    "Hammer",
    "Screwdriver",
    "Pliers",
    "Deepak"
]

# products = [
#     "Pliers",
#     "Combination Pliers",
#     "Bolt Cutters",
#     "Screwdriver",
#     "Adjustable Wrench",
#     "Long Nose Pliers",
#     "Slip Joint Pliers",
#     "Claw Hammer",
#     "Hammer",
#     "Chisels"
# ]

async def search_product(browser, product):

    page = await browser.new_page()

    try:
        await page.goto("https://practicesoftwaretesting.com/")
        await page.locator('[data-test="search-query"]').fill(product)
        await page.locator('[data-test="search-submit"]').click()
        await expect(page.locator('[data-test="product-name"]').filter(has_text=product).first).to_be_visible()
        print(f"{product} → PASS")

    except:
        print(f"{product} → FAIL - Product not found")

    await page.close()


async def main():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        tasks = []
        for product in products:
            tasks.append(search_product(browser, product))
        await asyncio.gather(*tasks)
        await browser.close()


asyncio.run(main())