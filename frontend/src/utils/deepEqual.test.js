import { describe, it, expect } from 'vitest';
import deepEqual from './deepEqual.js';

describe('deepEqual', () => {
  it('treats objects with different key orders as equal', () => {
    const a = { foo: 1, bar: 2 };
    const b = { bar: 2, foo: 1 };
    expect(deepEqual(a, b)).toBe(true);
  });

  it('detects differences in values', () => {
    const a = { foo: 1, bar: 2 };
    const b = { bar: 2, foo: 2 };
    expect(deepEqual(a, b)).toBe(false);
  });
});
