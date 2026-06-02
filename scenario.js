const { chromium } = require('playwright');

module.exports = async function() {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    try {
        // Navegar a la página principal del backend o frontend según corresponda
        console.log("Iniciando escenario de GreenFrame...");
        await page.goto('http://localhost:3000');
        
        // Simular tiempo de interacción o carga de datos (al menos 10 segundos para estabilizar métricas)
        await page.waitForTimeout(3000);
        
        // Simular navegación a health o api endpoints
        await page.goto('http://localhost:3000/api/health');
        await page.waitForTimeout(3000);
        
        // Navegar al dashboard de impacto ambiental
        await page.goto('http://localhost:3000/environmental-impact');
        await page.waitForTimeout(5000);
        
        console.log("Escenario completado.");
    } catch (e) {
        console.error("Error en el escenario:", e);
    } finally {
        await browser.close();
    }
};
