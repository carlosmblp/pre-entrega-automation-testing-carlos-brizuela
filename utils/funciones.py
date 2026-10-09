from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def iniciar_sesion(navegador, usuario, contrasena):
    navegador.get("https://www.saucedemo.com/")

    espera = WebDriverWait(navegador, 10)

    # Esperar a que el campo de usuario esté visible.
    campo_usuario = espera.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    campo_usuario.send_keys(usuario)

    navegador.find_element(By.ID, "password").send_keys(contrasena)

    # Esperar a que el botón esté disponible y hacer clic.
    boton_login = espera.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )
    boton_login.click()