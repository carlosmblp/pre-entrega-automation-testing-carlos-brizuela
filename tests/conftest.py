import logging
import re
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver #Importamos la librería que permite controlar el navegador


logger = logging.getLogger(__name__)

# Ubicación de las capturas dentro del proyecto.
RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
CARPETA_CAPTURAS = RAIZ_PROYECTO / "reports" / "capturas"


@pytest.fixture
def navegador(request):
    logger.info("INICIO: %s", request.node.name)

    driver = webdriver.Chrome()
    #  navegador = webdriver.Chrome(
    #     service=Service(ChromeDriverManager().install())
    # )

    # Guardar el navegador para poder capturar también fallos de preparación.
    request.node._navegador = driver

    try:
        driver.maximize_window()
        logger.info("Chrome abierto")

        yield driver

    finally:
        logger.info("Cerrando Chrome")
        driver.quit()


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    # Obtener el resultado de la etapa que acaba de finalizar.
    reporte = yield

    if reporte.when == "call":
        logger.info(
            "RESULTADO: %s | %s",
            item.name,
            reporte.outcome.upper()
        )

    if reporte.failed:
        logger.error(
            "FALLO: %s | Etapa: %s\n%s",
            item.name,
            reporte.when,
            reporte.longreprtext
        )

        driver = getattr(item, "_navegador", None)

        # En teardown el navegador puede estar cerrado.
        if driver is not None and reporte.when in ("setup", "call"):
            try:
                CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)

                nombre_seguro = re.sub(r"[^a-zA-Z0-9_-]", "_", item.name)
                fecha = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

                archivo = CARPETA_CAPTURAS / (
                    f"{nombre_seguro}_{reporte.when}_{fecha}.png"
                )

                guardada = driver.save_screenshot(str(archivo))

                if guardada:
                    logger.info("Captura guardada: %s", archivo)
                else:
                    logger.error("Selenium no pudo guardar la captura")

            except Exception:
                # Un error de captura no debe ocultar el fallo original.
                logger.exception("No se pudo generar la captura")

    return reporte