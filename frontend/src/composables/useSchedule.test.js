import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { effectScope } from 'vue';
import { setActivePinia, createPinia } from 'pinia';
let useSchedule;
let httpClient;
let invalidateScheduleCache;

describe('useSchedule caching', () => {
  beforeEach(async () => {
    vi.resetModules();
    setActivePinia(createPinia());
    vi.spyOn(console, 'error').mockImplementation(() => {});
    vi.spyOn(console, 'warn').mockImplementation(() => {});
    ({ default: httpClient } = await import('../services/httpClient.js'));
    ({ invalidateScheduleCache } = await import('../services/api.js'));
    invalidateScheduleCache();
    ({ useSchedule } = await import('./useSchedule.js'));
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('caches data for the same date', async () => {
    const mockGet = vi
      .spyOn(httpClient, 'get')
      .mockResolvedValue({ data: { dates: [] } });

    let fetchSchedule;
    const scope = effectScope();
    scope.run(() => {
      ({ fetchSchedule } = useSchedule());
    });

    await fetchSchedule('2024-01-01', { prefetch: false });
    expect(mockGet).toHaveBeenCalledTimes(1);

    await fetchSchedule('2024-01-01', { prefetch: false });
    expect(mockGet).toHaveBeenCalledTimes(1);

    scope.stop();
  });

  it('prefetches adjacent days into cache', async () => {
    const responses = {
      '2024-01-02': { id: 'main' },
      '2024-01-01': { id: 'prev' },
      '2024-01-03': { id: 'next' },
    };
    const mockGet = vi.spyOn(httpClient, 'get').mockImplementation((url) => {
      const u = new URL(url, 'http://example');
      const date = u.searchParams.get('date');
      return Promise.resolve({ data: responses[date] });
    });

    let fetchSchedule;
    const scope = effectScope();
    scope.run(() => {
      ({ fetchSchedule } = useSchedule());
    });

    await fetchSchedule('2024-01-02');
    expect(mockGet).toHaveBeenCalledTimes(3);

    mockGet.mockClear();
    await fetchSchedule('2024-01-01', { prefetch: false });
    await fetchSchedule('2024-01-03', { prefetch: false });
    expect(mockGet).toHaveBeenCalledTimes(0);

    scope.stop();
  });
});

