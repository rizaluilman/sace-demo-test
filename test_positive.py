from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# Fungsi untuk mencatat pesan ke dalam file log
def log_message(message):
    # Membuka file log.txt dalam mode tambah ("a") dan menulis pesan ke dalamnya
    with open("log.txt", "a") as log_file:
        log_file.write(f"{message}\n")

# Fungsi untuk melakukan login dengan data yang valid
def login_positive(driver):
    # Menemukan field input username berdasarkan ID dan mengisi username
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    # Menemukan field input password berdasarkan ID dan mengisi password
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    # Menemukan tombol login berdasarkan ID dan mengkliknya
    driver.find_element(By.ID, "login-button").click()
    # Mencatat pesan bahwa login berhasil
    log_message("Logged in successfully.")
    # Menunggu selama 2 detik untuk memastikan halaman sudah termuat
    time.sleep(2)

# Fungsi untuk memverifikasi apakah homepage telah termuat dengan benar
def verify_homepage(driver):
    try:
        # Menunggu hingga label "Products" muncul di halaman homepage
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product_label"))
        )
        # Mencatat pesan bahwa homepage berhasil termuat
        log_message("Homepage loaded successfully.")
    except NoSuchElementException:
        # Mencatat pesan jika homepage gagal termuat
        log_message("Login failed, homepage not loaded.")
    # Menunggu selama 2 detik
    time.sleep(2)

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

    # Melakukan langkah-langkah pengujian
    login_positive(driver)  # Melakukan login ke website
    verify_homepage(driver)  # Memverifikasi apakah homepage berhasil termuat
    total_price = add_products_to_cart(driver)  # Menambahkan produk ke keranjang dan menghitung total harga
    checkout(driver, total_price)  # Melanjutkan proses checkout dan memverifikasi harga
    verify_checkout_success(driver)  # Memverifikasi apakah checkout berhasil

    # Menutup sesi WebDriver
    driver.quit()

    log_message("Test completed.")  # Mencatat bahwa pengujian telah selesai