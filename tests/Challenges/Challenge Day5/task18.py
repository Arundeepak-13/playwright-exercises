from playwright.sync_api import sync_playwright, expect


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Open product listing
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_timeout(1000)

    # Wait until products are visible
    page.locator('[data-test="product-name"]').first.wait_for(state="visible",timeout=1000)

    print("Product listing opened")

    all_products = []
    page_number = 1

    while True:

        # Get products on current page
        products = page.locator('[data-test="product-name"]')
        current_products = []


        for i in range(products.count()):
            product_name = products.nth(i).inner_text().strip()
            current_products.append(product_name)
        print(f"Page {page_number}: {len(current_products)} products")


        for product in current_products:
            print(f"  - {product}")


        # Verify products are displayed
        assert len(current_products) > 0, \
            f"No products found on page {page_number}"


        # Check duplicate products
        duplicate_products = set(current_products) & set(all_products)
        assert not duplicate_products, \
            f"Duplicate products found: {duplicate_products}"


        # Store products
        all_products.extend(current_products)


        # Find Next button
        next_button = page.locator('[data-test="pagination-next"]')


        # Stop if Next button doesn't exist
        if next_button.count() == 0:
            print("No Next button found. Pagination completed.")
            break


        # Check parent for disabled state
        next_parent = next_button.locator("..")

        parent_class = next_parent.get_attribute("class")

        if "disabled" in parent_class:
            print("Next button is disabled. Pagination completed.")
            break


        # Save first product before clicking Next
        first_product = current_products[0]


        # Click Next
        next_button.click()


        # Get first product on the new page
        first_product_locator = page.locator('[data-test="product-name"]').first


        # Wait until first product changes
        expect(first_product_locator).not_to_have_text(first_product,timeout=1000)


        # Get products from next page
        new_products_locator = page.locator('[data-test="product-name"]')
        new_products = []


        for i in range(new_products_locator.count()):
            product_name = new_products_locator.nth(i).inner_text().strip()
            new_products.append(product_name)


        # Verify next page is different
        assert new_products != current_products, \
            f"Page {page_number + 1} contains the same products"
        page_number += 1


    # Final validation
    total_products = len(all_products)
    unique_products = len(set(all_products))

    assert total_products == unique_products, \
        "Duplicate products exist across pages"



    print(f"Total pages: {page_number}")
    print(f"Total products: {total_products}")
    print(f"Total unique products: {unique_products}")

    browser.close()