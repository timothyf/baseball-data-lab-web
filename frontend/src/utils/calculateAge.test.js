import { describe, it, expect, vi } from 'vitest';
import calculateAge from './calculateAge.js';

describe('calculateAge', () => {
  it('computes age based on current date', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2024-05-01'));
    expect(calculateAge('2000-06-15')).toBe(23);
    expect(calculateAge('2000-04-15')).toBe(24);
    vi.useRealTimers();
  });

  it('returns null for invalid or missing date', () => {
    expect(calculateAge('invalid')).toBeNull();
    expect(calculateAge()).toBeNull();
  });
});
