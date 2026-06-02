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
      reporter: ['text', 'html', 'lcov', 'json'],
      reportsDirectory: './coverage',
      include: ['src/app/**/*.ts'],
      exclude: [
        'src/app/**/*.spec.ts',
        'src/app/**/*.d.ts',
        'src/main.ts',
        'src/main.server.ts',
        'src/server.ts',
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
