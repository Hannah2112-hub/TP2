import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['src/tests/**/*.spec.ts'],
    setupFiles: ['src/mocks/vitest-setup.ts'],
    testTransformMode: {
      web: ['src/tests/**/*.spec.ts'],
    },
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov', 'json', 'cobertura'],
      reportsDirectory: './coverage',
      include: ['src/app/**/*.ts'],
      exclude: [
        'src/app/**/*.spec.ts',
        'src/app/**/*.d.ts',
        'src/main.ts',
        'src/main.server.ts',
        'src/server.ts',
        'src/app/app.ts',
        'src/app/app.config.ts',
        'src/app/app.config.server.ts',
        'src/app/app.routes.ts',
        'src/app/app.routes.server.ts',
        'src/app/guards/auth.guard.ts',
        'src/app/models/modelos.ts',
      ],
      thresholds: {
        global: {
          statements: 70,
          branches: 70,
          functions: 70,
          lines: 70,
        }
      }
    },
    reporters: ['verbose', 'json'],
    outputFile: {
      json: './test-results/results.json'
    }
  }
});
