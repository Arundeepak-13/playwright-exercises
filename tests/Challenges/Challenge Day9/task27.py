from playwright.sync_api import sync_playwright, expect
def find_add_to_cart(page):
    locators = [
        page.locator("#add-to-cart-button"),
        page.locator('input[name="submit.add-to-cart"]'),
        page.get_by_role("button", name="Add to cart", exact=True),
        page.locator('input[value="Add to Cart"]')
    ]
    for locator in locators:
        if locator.count() > 0:
            return locator.first
    raise Exception("Add to Cart button was not found")

def test_amazon_strict_mode():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.amazon.in/",wait_until="domcontentloaded")
        print("Amazon opened")

        search_box = page.locator("#twotabsearchtextbox")
        search_box.fill("iPhone")
        search_box.press("Enter")
        print("Search completed")
        
        product_card = page.locator('div[data-component-type="s-search-result"]').first
        print("Product card found")
        product_name = product_card.locator("h2").inner_text()
        print("Product:", product_name)

        product_title = product_card.locator("h2")
        product_title.click()
        print("Product page opened")

        broad_locator = page.get_by_role("button")
        button_count = broad_locator.count()
        print("Broad button locator matched:",button_count,"elements")

        if button_count > 1:
            print()
            print("Strict Mode Problem!")
            print("The locator matches multiple buttons.")
            print("Playwright cannot identify one specific button.")
        print()
        print("Searching for Add to Cart...")
        add_to_cart = find_add_to_cart(page)
        print("Add to Cart locator found")

        add_to_cart.click()
        print("Add to Cart clicked successfully")
        cart = page.locator("#nav-cart")
        expect(cart).to_be_visible()
        cart.click()
        print("Cart opened")

        cart_product = page.get_by_text(product_name,exact=False)
        expect(cart_product).to_be_visible()
        print("Product added to cart successfully")
        browser.close()