import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:4200',
    // Genera videos automáticamente
    video: true,
    // Genera capturas en fallos
    screenshotOnRunFailure: true,
    // Carpeta de capturas
    screenshotsFolder: 'cypress/screenshots',
    // Carpeta de videos
    videosFolder: 'cypress/videos',
    // Timeout de comandos
    defaultCommandTimeout: 10000,
    // Timeout de carga de página
    pageLoadTimeout: 30000,
    supportFile: false,
    // Reporter para exportar resultados
    reporter: 'mochawesome',
    reporterOptions: {
      reportDir: 'cypress/reports',
      overwrite: false,
      html: true,
      json: true,
      reportFilename: 'cypress-report',
      timestamp: 'mmddyyyy_HHMMss'
    },
    setupNodeEvents(on, config) {
      // Evento para capturar logs de ejecución
      on('task', {
        log(message) {
          console.log(message);
          return null;
        }
      });
    },
  },
  // Variables de entorno
  env: {
    API_URL: 'http://127.0.0.1:8000/api',
    ADMIN_EMAIL: 'admin@uni.edu',
    ADMIN_PASSWORD: 'admin123'
  }
});
