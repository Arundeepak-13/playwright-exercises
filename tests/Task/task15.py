from playwright.sync_api import sync_playwright


BASE_URL = "https://practicesoftwaretesting.com/"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

  
    # Scenario A - Valid Search
    print("Scenario A - Valid Search")
    page.goto(BASE_URL)
    search_box = page.locator('[data-test="search-query"]')
    search_box.fill("Combination Pliers")
    search_box.press("Enter")
    page.wait_for_load_state("networkidle")


    # Get product from search results
    product = page.locator('[data-test="product-name"]').filter(has_text="Combination Pliers")


    # Verify search results are displayed
    assert product.is_visible()
    print("Search results are displayed")


    # Verify expected product is present
    assert product.count() > 0
    print("Combination Pliers is present")


    # Verify product name
    product_name = product.first.inner_text().strip()
    assert product_name == "Combination Pliers"
    print("Product name matches search:", product_name)


    # Click product
    product.first.click()
    page.wait_for_load_state("networkidle")


    # Verify correct product page
    product_page_name = page.locator('[data-test="product-name"]').inner_text().strip()
    assert product_page_name == "Combination Pliers"
    print("Correct product page opened")



    # Scenario B - Partial Search
    print("Scenario B - Partial Search")
    page.goto(BASE_URL)
    search_text = "pliers"
    search_box = page.locator('[data-test="search-query"]')
    search_box.fill(search_text)
    search_box.press("Enter")
    page.wait_for_load_state("networkidle")



    # Get all product names
    products = page.locator('[data-test="product-name"]')
    count = products.count()
    print("Number of products found:", count)



    # Verify results are displayed
    assert count > 0
    print("Search results are displayed")


    # Verify every product contains searched text
    for i in range(count):
        product_name = products.nth(i).inner_text().strip()
        print("Product:", product_name)
        assert search_text.lower() in product_name.lower(), (
            f"Product '{product_name}' does not contain "
            f"'{search_text}'"
        )
    print("All displayed products contain 'pliers'")




    # Scenario C - Invalid Search
    print("Scenario C - Invalid Search")


    page.goto(BASE_URL)
    invalid_product = "XYZNonExistingProduct123"
    search_box = page.locator('[data-test="search-query"]')
    search_box.fill(invalid_product)
    search_box.press("Enter")
    page.wait_for_load_state("networkidle")



    # Verify no products are displayed
    products = page.locator('[data-test="product-name"]')
    assert products.count() == 0
    print("No products are displayed")


    # Verify no-results message
    no_results = page.get_by_text("There are no products found.",exact=True)
    assert no_results.is_visible()
    print("No-results message is displayed")




    # Bonus - Data Driven Search
    print("Bonus - Data Driven Search")
    search_data = [
        ("Combination Pliers", "Combination Pliers"),
        ("Bolt Cutters", "Bolt Cutters"),
        ("Hammer", "Hammer"),
        ("Screwdriver", "Screwdriver"),
        ("Wrench", "Wrench")
    ]
    for search_term, expected_product in search_data:
        print("\nSearching for:", search_term)
        page.goto(BASE_URL)
        search_box = page.locator('[data-test="search-query"]')
        search_box.fill(search_term)
        search_box.press("Enter")
        page.wait_for_load_state("networkidle")



        # Get all search results
        products = page.locator('[data-test="product-name"]')
        count = products.count()


        # Verify search results exist
        assert count > 0, (f"No products found for '{search_term}'")
        found = False

        # Check every displayed product
        for i in range(count):
            actual_name = products.nth(i).inner_text().strip()
            print("Product:", actual_name)

            # Check expected product is present
            if expected_product.lower() in actual_name.lower():
                found = True
                print("Expected:", expected_product)
                print("Actual:", actual_name)


                # Click the matching product
                products.nth(i).click()
                page.wait_for_load_state("networkidle")


                # Verify product page
                product_page_name = page.locator(
                    '[data-test="product-name"]'
                ).inner_text().strip()
                assert expected_product.lower() in product_page_name.lower()
                print("Correct product page opened")
                break
        assert found, (
            f"Expected product '{expected_product}' "
            f"was not found in search results"
        )


    browser.close()