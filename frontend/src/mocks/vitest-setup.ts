import '@angular/compiler';
import { beforeAll, afterAll, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import {
  BrowserTestingModule,
  platformBrowserTesting,
} from '@angular/platform-browser/testing';
import { server } from './server';

beforeAll(() => {
  TestBed.initTestEnvironment(
    BrowserTestingModule,
    platformBrowserTesting(),
  );
  server.listen({ onUnhandledRequest: 'warn' });
});

afterEach(() => server.resetHandlers());

afterAll(() => {
  server.close();
  TestBed.resetTestEnvironment();
});
