import asyncio
import time
from playwright.async_api import async_playwright, expect


products = [
    "Pliers",
    "Combination Pliers",
    "Bolt Cutters",
    "Hammer",
    "Claw Hammer"
]


async def validate_product(browser, product):
    page = await browser.new_page()
    await page.goto("https://practicesoftwaretesting.com/")
    search_box = page.locator('[data-test="search-query"]')
    await search_box.fill(product)
    await page.locator('[data-test="search-submit"]').click()
    product_name = page.locator('[data-test="product-name"]')
    await expect(product_name.filter(has_text=product).first).to_be_visible()
    print(f"{product} → PASS")
    await page.close()


# Sequential
async def sequential_test(browser):
    start = time.perf_counter()
    for product in products:
        await validate_product(browser, product)
    end = time.perf_counter()
    return end - start


#Parallel
async def parallel_test(browser):
    start = time.perf_counter()
    tasks = []
    for product in products:
        tasks.append(validate_product(browser, product))
    await asyncio.gather(*tasks)
    end = time.perf_counter()
    return end - start


async def main():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        print(" Sequential Execution ")
        sequential_time = await sequential_test(browser)
        print(f"Sequential execution: {sequential_time:.2f} seconds")


        print("\n Parallel Execution ")
        parallel_time = await parallel_test(browser)
        print(f"Parallel execution:   {parallel_time:.2f} seconds")


        #Compare both execution time
        if parallel_time < sequential_time:
            print("Parallel execution was faster")
        else:
            print("Sequential execution was faster")


        await browser.close()


asyncio.run(main())