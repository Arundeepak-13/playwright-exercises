from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://practicesoftwaretesting.com/"
PRODUCT_NAME = "Claw Hammer"


def test_product_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(BASE_URL)

        product = page.get_by_text(PRODUCT_NAME, exact=True)
        expect(product).to_be_visible()
        print("Product found:", PRODUCT_NAME)

        product_card = page.locator("a[href*='/product/']").filter(has=product).first
        expect(product_card).to_be_visible()
        print("Product card found")

        #nested element
        image = product_card.locator("img")
        expect(image).to_be_visible()
        print("Image found")

        #child element
        product_name = product_card.get_by_text(PRODUCT_NAME,exact=True)
        expect(product_name).to_be_visible()
        print("Product name found")

        # Parent name
        parent = product.locator("..")
        expect(parent).to_be_visible()
        print("Parent found")
        product_card.click()

        product_heading = page.get_by_role("heading",name=PRODUCT_NAME,exact=True)
        expect(product_heading).to_be_visible()
        print("Product page verified:", PRODUCT_NAME)

        #Add to cart
        add_to_cart = page.get_by_role("button",name="Add to cart",exact=True)
        expect(add_to_cart).to_be_visible()
        print("Add to Cart button found")

        add_to_cart.click()
        print("Product added to cart")

        cart = page.get_by_role("link", name="cart")
        expect(cart).to_contain_text("1")
        cart.click()

        cart_product = page.get_by_text(PRODUCT_NAME,exact=True)
        expect(cart_product).to_be_visible()
        print("Correct product found in cart:", PRODUCT_NAME)

        browser.close()