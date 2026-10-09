# Pre-entrega de Automatización QA

**Autor:** Carlos Mario Brizuela

## Propósito

Automatizar flujos básicos de SauceDemo utilizando Python, Selenium
WebDriver y Pytest: login, verificación del catálogo y agregado de un
producto al carrito.

Sitio utilizado: https://www.saucedemo.com/

## Tecnologías utilizadas

- Python.
- Selenium WebDriver.
- Pytest.
- pytest-html.
- Google Chrome.
- Git y GitHub para control de versiones.

## Estructura del proyecto

- `tests/test_saucedemo.py`: pruebas de login, catálogo y carrito.
- `tests/conftest.py`: fixture del navegador, logs y capturas ante fallos.
- `tests/test_evidencias.py`: prueba con fallo intencional para verificar capturas.
- `utils/funciones.py`: función auxiliar de login.
- `utils/__init__.py`: identifica el paquete de funciones auxiliares.
- `reports/reporte.html`: reporte de resultados generado por pytest-html.
- `reports/ejecucion.log`: log de la última ejecución.
- `reports/capturas/`: capturas automáticas ante fallos.
- `requirements.txt`: dependencias del proyecto.
- `pytest.ini`: configuración de las pruebas y los logs.
- `.gitignore`: archivos excluidos del control de versiones.

## Pruebas implementadas

### Login exitoso

- Abre la página de login.
- Ingresa el usuario `standard_user` y la contraseña `secret_sauce`.
- Utiliza esperas explícitas.
- Verifica la redirección a `/inventory.html`.
- Valida los textos visibles `Products` y `Swag Labs`.

### Verificación del catálogo

- Inicia sesión.
- Valida el título `Products`.
- Comprueba que exista al menos un producto visible.
- Obtiene y muestra en la terminal el nombre y precio del primero.
- Verifica la presencia del menú, el filtro de ordenamiento y el enlace al carrito.

### Agregado de un producto al carrito

- Inicia sesión y verifica que el carrito esté vacío.
- Guarda el nombre y precio del primer producto visible.
- Agrega ese producto al carrito.
- Verifica que el contador aumente de cero a uno.
- Navega a `/cart.html`.
- Comprueba que haya un único producto visible.
- Valida su nombre, precio y cantidad.

Cada prueba utiliza una sesión nueva de Chrome y realiza su propio login.
No depende de la ejecución ni del resultado de las demás.

## Requisitos previos

- Python instalado y disponible mediante el comando `py` en Windows.
- Google Chrome instalado.
- Acceso a Internet para instalar dependencias, acceder a SauceDemo
  y permitir la gestión del controlador de Chrome por Selenium.

Los comandos siguientes se ejecutan desde la raíz del proyecto,
donde se encuentran `requirements.txt` y `pytest.ini`.

## Instalación en Windows

Crear el entorno virtual:

```powershell
py -m venv .venv
```

Instalar las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se utiliza directamente el Python del entorno virtual, por lo que
no es necesario activarlo.

## Ejecutar las pruebas

Ejecutar las tres pruebas y generar un reporte HTML:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s --html=reports/reporte.html --self-contained-html
```

- `-v`: muestra los nombres y resultados de las pruebas.
- `-s`: permite ver en la terminal los datos mostrados con `print()`.
- `--html`: indica dónde guardar el reporte.
- `--self-contained-html`: genera un reporte HTML con sus recursos incorporados.

Abrir `reports/reporte.html` en el navegador para consultar los resultados.

### Ejecutar una prueba individual

Login:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py::test_login_exitoso -v
```

Catálogo:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py::test_catalogo_productos -v -s
```

Carrito:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py::test_agregar_producto_al_carrito -v -s
```

## Logs de ejecución

Los logs aparecen en la terminal y se guardan en `reports/ejecucion.log`.

Incluyen:

- Inicio de cada prueba.
- Apertura y cierre de Chrome.
- Resultado de la prueba.
- Detalle de los fallos.
- Ubicación de las capturas generadas o errores al capturarlas.

El archivo de log se reemplaza en cada ejecución.
Los mensajes mostrados con `print()` no se agregan automáticamente al log.

## Capturas automáticas ante fallos

Cuando una prueba falla durante su preparación o ejecución y Chrome
sigue disponible, se guarda una captura PNG en `reports/capturas/`.

El nombre incluye la prueba, la etapa, la fecha y la hora.
Las capturas son archivos separados del reporte HTML.

Si Chrome no llega a abrirse, no es posible obtener una captura.
Si todas las pruebas pasan, no se generan capturas nuevas.

### Comprobar el funcionamiento de las capturas

El archivo `tests/test_evidencias.py` contiene una prueba que abre SauceDemo
y provoca un fallo intencional con `assert False`.

Esta prueba está excluida de las ejecuciones habituales mediante
la siguiente configuración en `pytest.ini`:

```ini
addopts = --ignore=tests/test_evidencias.py
```

Para ejecutarla, anular esa opción solamente para esta ejecución:

```powershell
.\.venv\Scripts\python.exe -m pytest -o addopts="" tests/test_evidencias.py -v
```

El resultado esperado es `1 failed`, porque el fallo es intencional.

Verificar que:

1. Se haya creado un PNG en `reports/capturas/`.
2. El log registre el fallo y el mensaje `Captura guardada`.
3. La imagen muestre la página abierta al momento del fallo.

Después, ejecutar nuevamente las tres pruebas normales para dejar
actualizados el log y el reporte HTML:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s --html=reports/reporte.html --self-contained-html
```

## Resultado verificado

En la ejecución realizada durante el desarrollo, las tres pruebas
funcionales finalizaron correctamente: `3 passed in 12.94s`.

Este resultado corresponde a esa ejecución; futuras ejecuciones pueden
variar según el sitio, la conectividad y el entorno.