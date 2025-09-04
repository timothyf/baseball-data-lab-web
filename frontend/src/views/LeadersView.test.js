// @vitest-environment jsdom
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';

// simple stubs for PrimeVue components to avoid dependency on DOM APIs
const DataTableStub = {
  props: ['value'],
  template: '<div class="datatable"><div v-for="row in value" :key="row.playerFullName">{{ row.playerFullName }}</div><slot></slot></div>',
};
const ColumnStub = { template: '<div></div>' };
const TabViewStub = { template: '<div><slot></slot></div>' };
const TabPanelStub = { template: '<div><slot></slot></div>' };
const DialogStub = { template: '<div><slot></slot></div>' };
const DropdownStub = {
  props: ['modelValue'],
  emits: ['update:modelValue'],
  template: '<div></div>',
};
const ProgressSpinnerStub = { template: '<div></div>' };

// mock PrimeVue modules
vi.mock('primevue/datatable', () => ({ default: DataTableStub }));
vi.mock('primevue/column', () => ({ default: ColumnStub }));
vi.mock('primevue/tabview', () => ({ default: TabViewStub }));
vi.mock('primevue/tabpanel', () => ({ default: TabPanelStub }));
vi.mock('primevue/dialog', () => ({ default: DialogStub }));
vi.mock('primevue/dropdown', () => ({ default: DropdownStub }));
vi.mock('primevue/progressspinner', () => ({ default: ProgressSpinnerStub }));

// Stub the API module
const fetchBattingLeaders = vi.fn();
const fetchPitchingLeaders = vi.fn(() => Promise.resolve([]));
const fetchFieldingLeaders = vi.fn(() => Promise.resolve([]));

vi.mock('../services/api', () => ({
  fetchBattingLeaders: (...args) => fetchBattingLeaders(...args),
  fetchPitchingLeaders: (...args) => fetchPitchingLeaders(...args),
  fetchFieldingLeaders: (...args) => fetchFieldingLeaders(...args),
}));

// Helper to return different data based on league/team filter
function makeData(label) {
  return Promise.resolve([
    { rank: 1, playerFullName: label, teamAbbrev: 'T' },
  ]);
}

describe('LeadersView filtering', () => {
  beforeEach(() => {
    fetchBattingLeaders.mockImplementation(({ league_ids: leagueId, team_id: teamId } = {}) => {
      if (teamId) return makeData(`Team ${teamId} Player`);
      if (leagueId) return makeData(`League ${leagueId} Player`);
      return makeData('All Player');
    });
  });

  it('calls API with filters and updates table', async () => {
    const { default: LeadersView } = await import('./LeadersView.vue');
    const wrapper = mount(LeadersView);

    await flushPromises();

    expect(fetchBattingLeaders).toHaveBeenCalledTimes(1);
    expect(wrapper.html()).toContain('All Player');

    const dropdowns = wrapper.findAllComponents(DropdownStub);
    dropdowns[0].vm.$emit('update:modelValue', 103);
    await flushPromises();

    expect(fetchBattingLeaders).toHaveBeenCalledTimes(2);
    const leagueOpts = fetchBattingLeaders.mock.calls[1][0];
    expect(leagueOpts).toMatchObject({ league_ids: 103, team_id: null });
    expect(wrapper.html()).toContain('League 103 Player');

    dropdowns[1].vm.$emit('update:modelValue', 133);
    await flushPromises();

    expect(fetchBattingLeaders).toHaveBeenCalledTimes(3);
    const teamOpts = fetchBattingLeaders.mock.calls[2][0];
    expect(teamOpts).toMatchObject({ league_ids: 103, team_id: 133 });
    expect(wrapper.html()).toContain('Team 133 Player');
  });
});

describe('LeadersView sorting', () => {
  beforeEach(() => {
    fetchBattingLeaders.mockReset();
    fetchPitchingLeaders.mockResolvedValue([]);
    fetchFieldingLeaders.mockResolvedValue([]);
    fetchBattingLeaders.mockResolvedValue([
      { rank: 1, playerFullName: 'A', teamAbbrev: 'T' },
    ]);
  });

  it('sorts new columns in descending order first', async () => {
    const { default: LeadersView } = await import('./LeadersView.vue');
    const wrapper = mount(LeadersView);

    await flushPromises();

    fetchBattingLeaders.mockClear();

    const dt = wrapper.findAllComponents(DataTableStub)[0];
    dt.vm.$emit('sort', { sortField: 'avg', sortOrder: 1 });
    await flushPromises();

    expect(fetchBattingLeaders).toHaveBeenCalledTimes(1);
    const opts = fetchBattingLeaders.mock.calls[0][0];
    expect(opts).toMatchObject({ statType: 'avg', sortOrder: 'desc' });
  });
});

