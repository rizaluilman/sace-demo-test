from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# Fungsi untuk mencatat pesan ke dalam file log
def log_message(message):
    # Membuka file log.txt dalam mode tambah ("a") dan menulis pesan ke dalamnya
    with open("log.txt", "a") as log_file:
        log_file.write(f"{message}\n")

# Fungsi untuk melakukan login dengan data yang salah (negatif)
def login_negative(driver):
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    log_message("Attempted login with invalid credentials.")
    time.sleep(2)

# Fungsi untuk memverifikasi pesan kesalahan login
def verify_login_failed(driver):
    try:
        error_message_element = driver.find_element(By.XPATH, "//h3[@data-test='error']")
        error_message = error_message_element.text
        assert "Username and password do not match any user in this service" in error_message, "Expected error message not found."
        log_message("Login failed as expected with invalid credentials.")
    except NoSuchElementException:
        log_message("Error message not displayed, test failed.")
    time.sleep(2)

# Fungsi untuk reload halaman browser
def reload_browser(driver):
    driver.refresh()  # Reload halaman browser
    log_message("Browser reloaded.")
    time.sleep(2)  # Menunggu sejenak setelah reload

# Fungsi untuk login dengan user problem_user
def login_problem_user(driver):
    driver.find_element(By.ID, "user-name").send_keys("problem_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    log_message("Logged in with problem_user.")
    time.sleep(2)

# Fungsi untuk memverifikasi bahwa login berhasil dengan problem_user
def verify_login_successful(driver):
    try:
        # Memeriksa apakah label "Products" muncul setelah login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_label"))
        )
        log_message("Login with problem_user was successful.")
    except TimeoutException:
        log_message("Login with problem_user failed.")

# Fungsi untuk menambahkan produk ke dalam keranjang dan menghitung total harga
def add_products_to_cart(driver):
    product_prices = []  # Membuat list untuk menyimpan harga setiap produk
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")  # Menemukan semua produk di halaman
    for product in products:
        # Menemukan elemen harga setiap produk dan mengambil nilai harga
        price_element = product.find_element(By.CLASS_NAME, "inventory_item_price")
        price = float(price_element.text.replace("$", ""))  # Mengonversi harga menjadi float
        product_prices.append(price)  # Menambahkan harga ke dalam list
        # Menemukan tombol "Add to Cart" dan mengkliknya
        product.find_element(By.CLASS_NAME, "btn_inventory").click()

    # Memeriksa apakah 6 produk telah ditambahkan ke dalam keranjang dengan memeriksa badge pada ikon keranjang
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == '6', f"Expected 6 items in the cart, but got {cart_count}."
    # Mencatat pesan bahwa semua produk berhasil ditambahkan ke keranjang
    log_message("All 6 products added to cart successfully.")
    time.sleep(2)  # Menunggu selama 2 detik
    return sum(product_prices)  # Mengembalikan total harga dari produk yang telah ditambahkan

# Fungsi untuk melanjutkan proses checkout dan memverifikasi total harga
def checkout(driver, expected_total):
    # Mengklik ikon keranjang untuk melihat isi keranjang
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Menunggu tombol checkout dapat diklik
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout_button"))
    )

    # Mengklik tombol checkout
    checkout_button = driver.find_element(By.CLASS_NAME, "checkout_button")
    checkout_button.click()

    # Mengisi informasi checkout
    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    # Mengklik tombol "continue" untuk melanjutkan
    driver.find_element(By.CLASS_NAME, "cart_button").click()

    # Mengambil semua harga dari produk di keranjang dan menghitung totalnya
    item_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    calculated_total = 0
    for price in item_prices:
        calculated_total += float(price.text.replace("$", ""))

    # Mencatat total harga yang dihitung
    log_message(f"Calculated total from cart items: {calculated_total}")

    # Mengambil subtotal yang ditampilkan di halaman checkout
    subtotal_element = driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
    subtotal_text = subtotal_element.text.replace("Item total: $", "")
    subtotal = float(subtotal_text)

    # Memverifikasi apakah total yang dihitung sesuai dengan subtotal yang ditampilkan
    assert calculated_total == subtotal, f"Calculated total {calculated_total} does not match displayed subtotal {subtotal}."
    log_message(f"Subtotal validated: {subtotal}")

    # Menyelesaikan proses checkout dengan mengklik tombol "finish"
    driver.find_element(By.CLASS_NAME, "cart_button").click()
    log_message("Checkout completed.")

# Fungsi untuk memverifikasi kesalahan pada saat input data checkout
def verify_checkout_error(driver):
    # Klik ikon keranjang
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Menunggu tombol checkout dapat diklik
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout_button"))
    )

    # Mengklik tombol checkout
    checkout_button = driver.find_element(By.CLASS_NAME, "checkout_button")
    checkout_button.click()

    # Mengisi field last name
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    # Memeriksa apakah first name berubah menjadi "Doe" setelah mengisi last name
    first_name = driver.find_element(By.ID, "first-name").get_attribute("value")
    assert first_name == "Doe", f"First name did not change as expected. Found: {first_name}"
    log_message("Checkout input error occurred as expected.")
    
    time.sleep(2)  # Menunggu selama 2 detik

# Fungsi untuk memverifikasi apakah item total tidak sesuai
def verify_incorrect_item_total(driver, expected_total):
    # Klik ikon keranjang untuk melihat isi keranjang
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    # Menunggu tombol checkout dapat diklik
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "checkout_button"))
    )

    # Mengklik tombol checkout
    checkout_button = driver.find_element(By.CLASS_NAME, "checkout_button")
    checkout_button.click()

    # Mengambil subtotal yang ditampilkan di halaman checkout
    subtotal_element = driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
    subtotal_text = subtotal_element.text.replace("Item total: $", "")
    subtotal = float(subtotal_text)

    # Memverifikasi bahwa subtotal tidak sesuai dengan yang diharapkan
    assert subtotal != expected_total, f"Item total is correct. Found: {subtotal}"
    log_message(f"Incorrect item total verified: {subtotal} (expected: {expected_total})")

    time.sleep(2)  # Menunggu selama 2 detik

# Fungsi untuk memverifikasi apakah checkout berhasil
def verify_checkout_success(driver):
    try:
        # Memeriksa apakah pesan sukses muncul setelah checkout
        success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert success_message == "THANK YOU FOR YOUR ORDER", "Checkout not successful."
        log_message("Checkout successful.")
    except NoSuchElementException:
        log_message("Checkout failed.")
    time.sleep(2)  # Menunggu selama 2 detik

if __name__ == "__main__":
    # Menginisialisasi WebDriver Chrome
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    # Membuka halaman login dari website
    driver.get("https://www.saucedemo.com/v1/index.html")

    # Menghapus isi file log sebelum memulai tes baru
    open("log.txt", "w").close()

    # Melakukan langkah-langkah pengujian negatif
    login_negative(driver)  # Mencoba login dengan kredensial yang salah
    verify_login_failed(driver)  # Memverifikasi bahwa login gagal
    reload_browser(driver)  # Reload halaman browser setelah login gagal
    login_problem_user(driver)  # Login dengan problem_user
    verify_login_successful(driver)  # Memverifikasi bahwa login berhasil
    total_price = add_products_to_cart(driver)  # Menambahkan 6 produk ke keranjang
    checkout(driver, total_price)  # Checkout dan isi data
    verify_checkout_error(driver)  # Verifikasi error saat mengisi data checkout (last name berubah jadi first name)
    verify_incorrect_item_total(driver, expected_total=100.0)  # Verifikasi total item tidak sesuai
    verify_checkout_success(driver)  # Verifikasi checkout berhasil (meskipun total item tidak sesuai)
    # Menutup sesi WebDriver
    driver.quit()

    log_message("Negative test completed.")  # Mencatat bahwa pengujian negatif telah selesai
