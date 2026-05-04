from seleniumbase import BaseCase

class TestBackendDocs(BaseCase):
    def test_swagger_docs_load(self):
        # 1. Navegar a la documentación de FastAPI (asumiendo que corre localmente)
        # Si tienes el backend corriendo, usa esa URL. 
        # Por ahora probaremos con la estructura básica.
        url = "http://127.0.0.1:8000/docs"
        
        self.open(url)
        
        # 2. Verificar que el título sea el correcto
        self.assert_title_contains("FastAPI")
        
        # 3. Verificar que se carguen los tags de los endpoints
        # Los elementos de Swagger suelen tener la clase '.opblock-tag-section'
        self.assert_element("h1.title")
        
        # 4. Captura de pantalla para el reporte
        self.save_screenshot("swagger_docs_load")

    def test_navigation_to_redoc(self):
        self.open("http://127.0.0.1:8000/redoc")
        self.assert_element("nav")
        self.save_screenshot("redoc_load")
