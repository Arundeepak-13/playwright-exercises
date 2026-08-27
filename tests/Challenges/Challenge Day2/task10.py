from playwright.sync_api import sync_playwright, expect

products_to_search = ["Hammer", "Pliers", "Combination Pliers"]

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for product_name in products_to_search:

        #Open application
        page.goto("https://practicesoftwaretesting.com/")
        page.wait_for_timeout(2000)
        print("\nApplication opened")


        #Verify search box
        search_box = page.get_by_role("textbox", name="search")
        expect(search_box).to_be_visible()
        print("Search box is visible")


        #Enter name of the product
        search_box.fill(product_name)
        print("Entered:", product_name)


        #Perform search
        search_button = page.get_by_role("button", name="search")
        expect(search_button).to_be_visible()
        search_button.click()


        # Wait for search results
        page.wait_for_timeout(2000)
        print("Search performed")


        #Get all display product
        product_links = page.locator("a[href^='/product/']")
        expect(product_links.first).to_be_visible()
        product_count = product_links.count()
        print("Number of search results:", product_count)
        assert product_count > 0, \
            "No search results displayed"
        print("Search results are displayed")



        #Extract all product names
        product_names = []
        for i in range(product_count):
            product = product_links.nth(i)
            name = product.locator("h5").inner_text().strip()
            product_names.append(name)
        print("Products found:")
        for name in product_names:
            print("-", name)

        #Verify the expected product appears in results
        expected_product = None
        for i in range(product_count):
            product = product_links.nth(i)
            name = product.locator("h5").inner_text().strip()
            if product_name.lower() in name.lower():
                expected_product = product
                break
        assert expected_product is not None, \
            f"{product_name} was not found in search results"
        print(product_name, "appears in search results")



        #Click expected product
        expect(expected_product).to_be_visible()
        expected_product.click()



        # Wait for product details page
        page.wait_for_timeout(2000)
        print("Product clicked")


        #Verify product details page
        product_heading = page.locator("h1")
        expect(product_heading).to_be_visible()
        actual_product_name = product_heading.inner_text().strip()
        print("Product details page:", actual_product_name)


        #Verify product name
        assert product_name.lower() in actual_product_name.lower(), \
            f"Wrong product details page opened. Expected: {product_name}"
        print("Product name verified successfully")



    browser.close()