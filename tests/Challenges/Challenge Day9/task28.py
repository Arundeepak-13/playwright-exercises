from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"
PRODUCT_NAME = "Claw Hammer"


def test_dom_relationships_and_add_to_cart():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(BASE_URL, wait_until="domcontentloaded")
            print("Application opened")

            
            product = page.get_by_text(PRODUCT_NAME,exact=True)

            expect(product).to_be_visible()
            print("Product found:", PRODUCT_NAME)

            
            product_card = page.locator("a[href*='/product/']").filter(has=product).first

            expect(product_card).to_be_visible()
            print("Product card found")

            
            image = product_card.locator("img")

            expect(image).to_be_visible()
            print("Image found")

           
            parent = product.locator("..")

            expect(parent).to_be_visible()
            print("Parent element found")

            
            children = product_card.locator(":scope > *")
            child_count = children.count()

            assert child_count > 0, "Product card has no child elements"

            print("Number of child elements:", child_count)

            
            sibling = product.locator(":scope ~ *").first

            if sibling.count() > 0:
                print("Sibling element found")

            
            nested_element = product_card.locator("img")

            expect(nested_element).to_be_visible()
            print("Nested element found")

            
            product_card.click()

            print("Product details page opened")

            
            product_heading = page.get_by_role("heading",name=PRODUCT_NAME,exact=True)

            expect(product_heading).to_be_visible()
            print("Product name verified:", PRODUCT_NAME)

            
            add_to_cart = page.get_by_role("button",name="Add to cart",exact=True)

            expect(add_to_cart).to_be_visible()
            print("Add to Cart button found")

            
            add_to_cart.click()

            print("Product added to cart")

            
            cart = page.get_by_role("link",name="cart")

            expect(cart).to_contain_text("1")
            print("Cart count verified: 1")

            
            expect(cart).to_be_visible()
            cart.click()

            print("Cart opened")

            
            cart_product = page.get_by_text(PRODUCT_NAME,exact=True)

            expect(cart_product).to_be_visible()
            print("Correct product found in cart:", PRODUCT_NAME)

        finally:
            browser.close()