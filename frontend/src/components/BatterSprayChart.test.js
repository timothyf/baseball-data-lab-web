// @vitest-environment jsdom
import { describe, it, expect, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';

vi.mock('chart.js/auto', () => ({ default: vi.fn(() => ({ destroy: vi.fn() })) }));

const fetchPlayerStatcastBatterData = vi.fn().mockResolvedValue({ results: [] });
vi.mock('../services/api.js', () => ({ fetchPlayerStatcastBatterData }));

describe('BatterSprayChart', () => {
  it('fetches current season data by default', async () => {
    const { default: Component } = await import('./BatterSprayChart.vue');
    const year = new Date().getFullYear();
    const today = new Date().toISOString().slice(0, 10);
    mount(Component, { props: { playerId: '1' } });
    await flushPromises();
    expect(fetchPlayerStatcastBatterData).toHaveBeenCalledWith('1', `${year}-03-01`, today);
  });
});
