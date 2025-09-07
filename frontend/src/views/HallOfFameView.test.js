// @vitest-environment jsdom
import { describe, it, expect, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';

const fetchHallOfFamePlayers = vi.fn();

vi.mock('../services/api', () => ({
  fetchHallOfFamePlayers: (...args) => fetchHallOfFamePlayers(...args),
}));

describe('HallOfFameView', () => {
  it('fetches and displays players with sortable columns', async () => {
    fetchHallOfFamePlayers.mockResolvedValue({
      players: [
        { bbref_id: 'b1', name: 'Alpha', mlbam_id: '1', year: 1990 },
        { bbref_id: 'b2', name: 'Beta', mlbam_id: '2', year: 1980 },
      ],
    });

    const { default: HallOfFameView } = await import('./HallOfFameView.vue');
    const wrapper = mount(HallOfFameView);

    await flushPromises();

    const rows = wrapper.findAll('tbody tr');
    expect(rows).toHaveLength(2);
    expect(wrapper.html()).toContain('Alpha');

    // sort by year
    await wrapper.findAll('th')[2].trigger('click');
    await flushPromises();
    const sortedRows = wrapper.findAll('tbody tr');
    expect(sortedRows[0].text()).toContain('Beta');

    expect(sortedRows[0].html()).toContain('https://www.mlb.com/player/2');
  });
});

