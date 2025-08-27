import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { effectScope } from 'vue';
import { setActivePinia, createPinia } from 'pinia';

let useSchedule;

describe('useSchedule caching', () => {
  beforeEach(async () => {
    vi.resetModules();
    setActivePinia(createPinia());
    vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(console, 'warn').mockImplementation(() => {});
    ({ useSchedule } = await import('./useSchedule.js'));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('caches data for the same date', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue({ dates: [] })
    });
    global.fetch = mockFetch;

    let fetchSchedule;
    const scope = effectScope();
    scope.run(() => {
      ({ fetchSchedule } = useSchedule());
    });

    await fetchSchedule('2024-01-01', { prefetch: false });
    expect(mockFetch).toHaveBeenCalledTimes(1);

    await fetchSchedule('2024-01-01', { prefetch: false });
    expect(mockFetch).toHaveBeenCalledTimes(1);

    scope.stop();
  });

  it('prefetches adjacent days into cache', async () => {
    const responses = {
      '2024-01-02': { id: 'main' },
      '2024-01-01': { id: 'prev' },
      '2024-01-03': { id: 'next' }
    };
    const mockFetch = vi.fn((url) => {
      const u = new URL(url, 'http://example');
      const date = u.searchParams.get('date');
      return Promise.resolve({
        json: () => Promise.resolve(responses[date])
      });
    });
    global.fetch = mockFetch;

    let fetchSchedule;
    const scope = effectScope();
    scope.run(() => {
      ({ fetchSchedule } = useSchedule());
    });

    await fetchSchedule('2024-01-02');
    expect(mockFetch).toHaveBeenCalledTimes(3);

    mockFetch.mockClear();
    await fetchSchedule('2024-01-01', { prefetch: false });
    await fetchSchedule('2024-01-03', { prefetch: false });
    expect(mockFetch).toHaveBeenCalledTimes(0);

    scope.stop();
  });
});

