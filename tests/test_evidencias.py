def test_captura_de_fallo(navegador):
    navegador.get("https://www.saucedemo.com/")

    assert False, "Fallo intencional para verificar la captura automática"


    #ejecucuion de prueba ante fallo
    #.\.venv\Scripts\python.exe -m pytest tests/test_evidencias.py -v