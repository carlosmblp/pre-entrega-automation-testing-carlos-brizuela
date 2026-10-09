import pytest

from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.funciones import iniciar_sesion


def test_login_exitoso(navegador):
    iniciar_sesion(navegador, "standard_user", "secret_sauce")

    espera = WebDriverWait(navegador, 10)

    # Esperar la redirección a la página de inventario.
    espera.until(
        lambda driver: urlparse(driver.current_url).path == "/inventory.html"
    )

    assert urlparse(navegador.current_url).path == "/inventory.html", (
        "El login no redirigió a la página de inventario"
    )

    # Esperar y validar el encabezado Products.
    titulo = espera.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    assert titulo.text == "Products", (
        f"Se esperaba 'Products', pero apareció '{titulo.text}'"
    )

    # Esperar y validar la marca Swag Labs.
    marca = espera.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "app_logo"))
    )

    assert marca.text == "Swag Labs", (
        f"Se esperaba 'Swag Labs', pero apareció '{marca.text}'"
    )

    # Ejecutar el test en la consola
    # .\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py::test_login_exitoso -v --html=reports/reporte.html --self-contained-html

def test_catalogo_productos(navegador):
    iniciar_sesion(navegador, "standard_user", "secret_sauce")

    espera = WebDriverWait(navegador, 10)

    # Verificar el título visible de la página de inventario.
    titulo = espera.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "title"))
    )

    assert titulo.text == "Products", (
        f"Se esperaba 'Products', pero apareció '{titulo.text}'"
    )

    # Esperar a que exista al menos un producto visible.
    productos = espera.until(
        EC.visibility_of_any_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )

    assert len(productos) > 0, "No hay productos visibles en el catálogo"

    # Obtener nombre y precio del primer producto visible.
    primer_producto = productos[0]

    nombre = primer_producto.find_element(
        By.CLASS_NAME, "inventory_item_name"
    )
    precio = primer_producto.find_element(
        By.CLASS_NAME, "inventory_item_price"
    )

    assert nombre.is_displayed(), "El nombre del producto no está visible"
    assert precio.is_displayed(), "El precio del producto no está visible"
    assert nombre.text.strip(), "El producto no tiene nombre"
    assert precio.text.strip(), "El producto no tiene precio"

    print(f"\nPrimer producto: {nombre.text} | Precio: {precio.text}")

    # Verificar que el botón del menú esté visible.
    menu = espera.until(
        EC.visibility_of_element_located(
            (By.ID, "react-burger-menu-btn")
        )
    )

    assert menu.is_displayed(), "El botón del menú no está visible"

    # Verificar que el selector de ordenamiento esté visible.
    filtro = espera.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "product_sort_container")
        )
    )

    assert filtro.is_displayed(), "El filtro no está visible"

    # Verificar que el enlace al carrito esté visible.
    carrito = espera.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )

    assert carrito.is_displayed(), "El enlace al carrito no está visible"

    #ejecución del test 
    #.\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py::test_catalogo_productos -v -s --html=reports/reporte.html --self-contained-html


def test_agregar_producto_al_carrito(navegador):
    iniciar_sesion(navegador, "standard_user", "secret_sauce")

    espera = WebDriverWait(navegador, 10)

    # Esperar los productos visibles y seleccionar el primero.
    productos = espera.until(
        EC.visibility_of_any_elements_located(
            (By.CLASS_NAME, "inventory_item")
        )
    )
    primer_producto = productos[0]

    # Guardar los datos para compararlos después en el carrito.
    nombre_producto = primer_producto.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text

    precio_producto = primer_producto.find_element(
        By.CLASS_NAME, "inventory_item_price"
    ).text

    # Obtener el contador inicial (sin indicador significa cero).
    indicadores = navegador.find_elements(
        By.CLASS_NAME, "shopping_cart_badge"
    )
    contador_inicial = int(indicadores[0].text) if indicadores else 0

    assert contador_inicial == 0, (
        "El carrito debe estar vacío al comenzar el test"
    )

    # Hacer clic en el botón del primer producto.
    boton_agregar = espera.until(
        EC.element_to_be_clickable(
            primer_producto.find_element(By.TAG_NAME, "button")
        )
    )

    assert boton_agregar.text == "Add to cart", (
        "El primer producto no está disponible para agregar"
    )
    boton_agregar.click()

    # Esperar a que el contador aumente en uno.
    contador_esperado = contador_inicial + 1

    espera.until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "shopping_cart_badge"),
            str(contador_esperado)
        )
    )

    contador_actual = navegador.find_element(
        By.CLASS_NAME, "shopping_cart_badge"
    ).text

    assert int(contador_actual) == contador_esperado, (
        "El contador del carrito no aumentó correctamente"
    )

    # Navegar al carrito.
    enlace_carrito = espera.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "shopping_cart_link")
        )
    )
    enlace_carrito.click()

    espera.until(
        lambda driver: urlparse(driver.current_url).path == "/cart.html"
    )

    assert urlparse(navegador.current_url).path == "/cart.html", (
        "No se abrió la página del carrito"
    )

    # Verificar que haya exactamente un producto visible.
    items_carrito = espera.until(
        EC.visibility_of_any_elements_located(
            (By.CLASS_NAME, "cart_item")
        )
    )

    assert len(items_carrito) == 1, (
        f"Se esperaba un producto, pero hay {len(items_carrito)}"
    )

    item = items_carrito[0]

    nombre_en_carrito = item.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text

    precio_en_carrito = item.find_element(
        By.CLASS_NAME, "inventory_item_price"
    ).text

    cantidad = item.find_element(
        By.CLASS_NAME, "cart_quantity"
    ).text

    assert nombre_en_carrito == nombre_producto, (
        "El producto del carrito no coincide con el agregado"
    )
    assert precio_en_carrito == precio_producto, (
        "El precio del carrito no coincide con el del catálogo"
    )
    assert cantidad == "1", "La cantidad del producto debe ser uno"

    print(
        f"\nProducto verificado en carrito: {nombre_en_carrito}"
        f" | Precio: {precio_en_carrito} | Cantidad: {cantidad}"
    )

    #ejecucion del test
    # .\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py::test_agregar_producto_al_carrito -v -s --html=reports/reporte.html --self-contained-html


    # EJECUCION DE LOS TRES TEST
    # .\.venv\Scripts\python.exe -m pytest -v -s --html=reports/reporte.html --self-contained-html
