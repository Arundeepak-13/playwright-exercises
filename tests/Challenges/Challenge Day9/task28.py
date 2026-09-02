from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"
PRODUCT_NAME = "Claw Hammer"


def test_dom_relationships_and_add_to_cart():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Open application
            page.goto(BASE_URL, wait_until="domcontentloaded")
            print("Application opened")

            # Find product
            product = page.get_by_text(PRODUCT_NAME,exact=True)

            expect(product).to_be_visible()
            print("Product found:", PRODUCT_NAME)

            # Find product card
            product_card = product.locator(
                "xpath=ancestor::a[contains(@href, '/product/')]"
            ).first

            expect(product_card).to_be_visible()
            print("Product card found")

            # Find image inside product card
            image = product_card.locator("img")

            expect(image).to_be_visible()
            print("Image found")

            # Parent element
            parent = product.locator("..")

            expect(parent).to_be_visible()
            print("Parent element found")

            # Child elements
            children = product_card.locator(":scope > *")

            child_count = children.count()

            print("Number of child elements:", child_count)

            assert child_count > 0

            # Sibling element
            sibling = product.locator(
                "xpath=following-sibling::*"
            ).first

            if sibling.count() > 0:
                print("Sibling element found")

            # Nested element
            nested_element = product_card.locator("img")

            expect(nested_element).to_be_visible()
            print("Nested element found")

            # Open product details
            product_card.click()

            print("Product details page opened")

            # Verify product heading
            product_heading = page.get_by_role(
                "heading",
                name=PRODUCT_NAME,
                exact=True
            )

            expect(product_heading).to_be_visible()

            print("Product name verified:", PRODUCT_NAME)

            # Find Add to Cart relative to product heading
            add_to_cart = product_heading.locator(
                "xpath=following::button[normalize-space()='Add to cart'][1]"
            )

            expect(add_to_cart).to_be_visible()

            print("Add to Cart button found")

            # Add product to cart
            add_to_cart.click()

            print("Product added to cart")

            # Open cart
            cart = page.get_by_role(
                "link",
                name="Cart"
            )

            expect(cart).to_be_visible()

            cart.click()

            print("Cart opened")

            # Verify correct product
            cart_product = page.get_by_text(
                PRODUCT_NAME,
                exact=True
            )

            expect(cart_product).to_be_visible()

            print(
                "Correct product found in cart:",
                PRODUCT_NAME
            )

        finally:
            browser.close()