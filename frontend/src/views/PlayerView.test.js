// @vitest-environment jsdom
import { describe, it, expect, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';

// Stub components used by PlayerView
const PlayerStatsStub = { template: '<div></div>' };
const PlayerSplitsStub = { template: '<div></div>' };
const PlayerGameLogStub = { template: '<div class="gamelog">Game Log Content</div>' };
const LoadingDialogStub = { template: '<div></div>' };
const TabViewStub = { template: '<div><slot></slot></div>' };
const TabPanelStub = { template: '<div><slot></slot></div>' };

vi.mock('../components/PlayerStats.vue', () => ({ default: PlayerStatsStub }));
vi.mock('../components/PlayerSplits.vue', () => ({ default: PlayerSplitsStub }));
vi.mock('../components/PlayerGameLog.vue', () => ({ default: PlayerGameLogStub }));
vi.mock('../components/LoadingDialog.vue', () => ({ default: LoadingDialogStub }));
vi.mock('primevue/tabview', () => ({ default: TabViewStub }));
vi.mock('primevue/tabpanel', () => ({ default: TabPanelStub }));

// Mock API calls
const fetchPlayer = vi.fn();
const fetchPlayerSplits = vi.fn();
const fetchPlayerGameLog = vi.fn();

vi.mock('../services/api.js', () => ({
  fetchPlayer: (...args) => fetchPlayer(...args),
  fetchPlayerSplits: (...args) => fetchPlayerSplits(...args),
  fetchPlayerGameLog: (...args) => fetchPlayerGameLog(...args),
}));

describe('PlayerView game log tab', () => {
  it('shows Game Log tab when data available', async () => {
    fetchPlayer.mockResolvedValue({ name: 'Test', team_name: 'Team', position: 'Pitcher' });
    fetchPlayerSplits.mockResolvedValue({});
    fetchPlayerGameLog.mockResolvedValue({ stats: [{ splits: [{}] }] });

    const { default: PlayerView } = await import('./PlayerView.vue');
    const wrapper = mount(PlayerView, { props: { id: '1' } });
    await flushPromises();

    expect(wrapper.find('.gamelog').exists()).toBe(true);
  });

  it('hides Game Log tab when no data', async () => {
    fetchPlayer.mockResolvedValue({ name: 'Test', team_name: 'Team', position: 'Pitcher' });
    fetchPlayerSplits.mockResolvedValue({});
    fetchPlayerGameLog.mockResolvedValue({ stats: [{ splits: [] }] });

    const { default: PlayerView } = await import('./PlayerView.vue');
    const wrapper = mount(PlayerView, { props: { id: '1' } });
    await flushPromises();

    expect(wrapper.find('.gamelog').exists()).toBe(false);
  });
});

