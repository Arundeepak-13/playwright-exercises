
from playwright.sync_api import sync_playwright


def test_amazon_strict_mode():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.amazon.in/",wait_until="domcontentloaded")
        print("Amazon opened")

        #search 
        search_box = page.locator("#twotabsearchtextbox")
        search_box.fill("iPhone")
        search_box.press("Enter")

        page.wait_for_load_state("domcontentloaded")
        print("Search completed")


        #find product
        product_card = page.locator('div[data-component-type="s-search-result"]').first
        print("Product card found")

        product_name = product_card.locator("h2").inner_text()

        print("Product:",product_name)


        #open product
        product_title = product_card.locator("h2")
        product_title.click()
        page.wait_for_load_state("domcontentloaded")
        print("Product page opened")

   
        #Broad Locator
        broad_locator = page.get_by_role("button")
        button_count = broad_locator.count()
        print("Broad button locator matched:",button_count,"elements")

        if button_count > 1:

            print()
            print("Strict Mode Problem!")
            print("The locator matches multiple buttons.")
            print("Playwright cannot identify one specific button.")

       #Find add to cart

        print()
        print("Searching for Add to Cart...")

        # Locator 1
        add_to_cart = page.locator("#add-to-cart-button")


        # Locator 2
        if add_to_cart.count() == 0:
            add_to_cart = page.locator('input[name="submit.add-to-cart"]')


        # Locator 3
        if add_to_cart.count() == 0:
            add_to_cart = page.get_by_role("button",name="Add to cart",exact=True)


        # Locator 4
        if add_to_cart.count() == 0:
            add_to_cart = page.locator('input[value="Add to Cart"]')

    
        #Verify add to cart 
        count = add_to_cart.count()
        print("Add to Cart locator matched:",count,"element(s)")
        if count == 0:
            raise Exception("Add to Cart button was not found")


        if count > 1:
            print("Multiple Add to Cart elements found.")
            add_to_cart = add_to_cart.first


        #click add to cart
        add_to_cart.click()
        print("Add to Cart clicked successfully")

       
        #open cart
        cart = page.locator("#nav-cart")
        cart_count = cart.count()
        print("Cart locator matched:",cart_count,"element(s)")


        if cart_count == 0:
            raise Exception("Cart link was not found")
        cart.click()
        page.wait_for_load_state("domcontentloaded")
        print("Cart opened")


        #Verify Product in cart
        cart_product = page.get_by_text(product_name,exact=False)
        if cart_product.count() > 0:
            print("Product added to cart successfully")
        else:
            print("Product name was not found exactly.")


            # Check whether cart contains an item
            cart_items = page.locator('[data-name="Active Items"]')
            if cart_items.count() > 0:
                print("Cart contains the product.")
            else:
                raise Exception("Product was not found in cart")


        browser.close()

