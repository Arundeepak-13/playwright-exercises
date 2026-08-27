from playwright.sync_api import sync_playwright


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("Cheapest Product")

    #  OPEN PRODUCT LISTING
  
    page.goto("https://practicesoftwaretesting.com/")
    page.wait_for_load_state("networkidle")

    print("Product listing opened")
    page.locator('[data-test="product-name"]').first.wait_for(state="visible",timeout=15000)
    product_names = page.locator('[data-test="product-name"]')
    product_prices = page.locator('[data-test="product-price"]')
    product_count = product_names.count()
    print("Products displayed:", product_count)
    assert product_count > 0, "No products displayed"

  
    #COLLECT PRODUCTS
    available_products = []
    print("Available Products")

    for i in range(product_count):
        name = product_names.nth(i).inner_text().strip()
        price_text = product_prices.nth(i).inner_text().strip()
        price = float(price_text.replace("$", "").replace(",", "").strip())
        available_products.append({"name": name,"price": price,"index": i})
        print(f"Available: {name} - ${price:.2f}")
    assert len(available_products) > 0, \
        "No available products found"



    #FIND CHEAPEST
    cheapest = available_products[0]
    for product in available_products:
        if product["price"] < cheapest["price"]:
            cheapest = product

    print("CHEAPEST AVAILABLE PRODUCT")
    print("Name :", cheapest["name"])
    print("Price:", f"${cheapest['price']:.2f}")


  
    #OPEN CHEAPEST PRODUCT
    page.locator('[data-test="product-name"]').nth(cheapest["index"]).click()
    page.wait_for_load_state("networkidle")
    print()
    print("Cheapest product opened")


    #VERIFY PRODUCT NAME
    product_page_name = page.locator('[data-test="product-name"]').inner_text().strip()
    print("Product page name:",product_page_name)
    assert product_page_name == cheapest["name"], \
        "Product name does not match"
    print("Product name matches")



    #VERIFY PRODUCT PRICE
    expected_price = f"${cheapest['price']:.2f}"
    price_locator = page.get_by_text(expected_price,exact=True)
    assert price_locator.count() > 0, \
        "Product page price not found"
    product_page_price_text = (price_locator.first.inner_text().strip())
    print("Product page price:",product_page_price_text)
    product_page_price = float(product_page_price_text.replace("$", "").replace(",", "").strip())
    assert product_page_price == cheapest["price"], \
        "Product price does not match"
    print("Product price matches")



    # ADD TO CART
    add_to_cart = page.get_by_text("Add to cart",exact=True)
    if add_to_cart.count() == 0:
        add_to_cart = page.get_by_role("button",name="Add to cart",exact=True)
    assert add_to_cart.count() > 0, \
        "Add to Cart button not found"
    assert add_to_cart.first.is_visible(), \
        "Add to Cart button is not visible"
    add_to_cart.first.click()
    print("Product added to cart")



    #OPEN CART
    page.locator('[data-test="nav-cart"]').click()
    page.wait_for_load_state("networkidle")
    print("Cart opened")

   
    #VERIFY CHEAPEST PRODUCT IN CART
    cart_body = page.locator("body").inner_text()
    print()
    print("Checking cart for:")
    print(cheapest["name"])
    assert cheapest["name"] in cart_body, \
        "Cheapest product is not present in cart"
    print(
        "Correct product is present in cart:",
        cheapest["name"]
    )



    #VERIFY CART PRICE
    cart_price_text = f"${cheapest['price']:.2f}"
    assert cart_price_text in cart_body, \
        "Correct product price is not present in cart"
    print(
        "Correct price is present in cart:",
        cart_price_text
    )


    # BONUS - MOST EXPENSIVE
    print("BONUS - MOST EXPENSIVE PRODUCT")
    most_expensive = available_products[0]
    for product in available_products:
        if product["price"] > most_expensive["price"]:
             most_expensive = product


    print("Most expensive product:",most_expensive["name"])
    print("Price:",f"${most_expensive['price']:.2f}")


    browser.close()