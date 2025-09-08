// @vitest-environment jsdom
import { describe, it, expect, vi } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';

const DialogStub = { props: ['visible'], template: '<div></div>' };
const ProgressSpinnerStub = { template: '<div></div>' };

vi.mock('primevue/dialog', () => ({ default: DialogStub }));
vi.mock('primevue/progressspinner', () => ({ default: ProgressSpinnerStub }));

const fetchHallOfFamePlayers = vi.fn();

vi.mock('../services/api', () => ({
  fetchHallOfFamePlayers: (...args) => fetchHallOfFamePlayers(...args),
}));

describe('HallOfFameView', () => {
  it('fetches and displays players with sortable columns', async () => {
    fetchHallOfFamePlayers.mockResolvedValue({
      players: [
        {
          bbref_id: 'b2',
          name: 'Beta Two',
          first_name: 'Beta',
          last_name: 'Two',
          mlbam_id: '2',
          year: 1980,
        },
        {
          bbref_id: 'b1',
          name: 'Alpha One',
          first_name: 'Alpha',
          last_name: 'One',
          mlbam_id: '1',
          year: 1990,
        },
      ],
    });

    const { default: HallOfFameView } = await import('./HallOfFameView.vue');
    const wrapper = mount(HallOfFameView);

    let dialog = wrapper.findComponent(DialogStub);
    expect(dialog.props('visible')).toBe(true);

    await flushPromises();

    dialog = wrapper.findComponent(DialogStub);
    expect(dialog.props('visible')).toBe(false);

    const rows = wrapper.findAll('tbody tr');
    expect(rows).toHaveLength(2);
    const cells = rows[0].findAll('td');
    expect(cells[1].text()).toBe('Alpha');
    expect(cells[2].text()).toBe('One');

    // sort by year
    await wrapper.findAll('th')[4].trigger('click');
    await flushPromises();
    const sortedRows = wrapper.findAll('tbody tr');
    expect(sortedRows[0].text()).toContain('Beta Two');

    expect(sortedRows[0].html()).toContain('https://www.mlb.com/player/2');
    expect(sortedRows[0].html()).not.toContain('2.0');
  });

  it('sorts years numerically when reversing sort order', async () => {
    fetchHallOfFamePlayers.mockResolvedValue({
      players: [
        {
          bbref_id: 'm1',
          name: 'Minnie Minoso',
          first_name: 'Minnie',
          last_name: 'Minoso',
          mlbam_id: '3',
          year: '2022',
        },
        {
          bbref_id: 'f1',
          name: 'Future Star',
          first_name: 'Future',
          last_name: 'Star',
          mlbam_id: '4',
          year: '2025',
        },
      ],
    });

    const { default: HallOfFameView } = await import('./HallOfFameView.vue');
    const wrapper = mount(HallOfFameView);

    await flushPromises();

    const yearHeader = wrapper.findAll('th')[4];
    await yearHeader.trigger('click');
    await flushPromises();
    await yearHeader.trigger('click');
    await flushPromises();

    const rows = wrapper.findAll('tbody tr');
    expect(rows[0].text()).toContain('Future Star');
  });

  it('handles sorting across columns with accented names and missing ids', async () => {
    fetchHallOfFamePlayers.mockResolvedValue({
      players: [
        {
          bbref_id: 'm1',
          name: 'Minnie Miñoso',
          first_name: 'Minnie',
          last_name: 'Miñoso',
          mlbam_id: '123',
          year: '2022',
        },
        {
          bbref_id: 'z1',
          name: 'Zed Future',
          first_name: 'Zed',
          last_name: 'Future',
          mlbam_id: '999',
          year: '2025',
        },
      ],
    });

    const { default: HallOfFameView } = await import('./HallOfFameView.vue');
    const wrapper = mount(HallOfFameView);

    await flushPromises();

    const headers = wrapper.findAll('th');

    // sort by year descending
    await headers[4].trigger('click');
    await headers[4].trigger('click');
    await flushPromises();
    let rows = wrapper.findAll('tbody tr');
    expect(rows[0].text()).toContain('Zed Future');

    // sort by mlbam_id descending
    await headers[3].trigger('click');
    await headers[3].trigger('click');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows[0].text()).toContain('Zed Future');

    // sort by first name descending
    await headers[1].trigger('click');
    await headers[1].trigger('click');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows[0].text()).toContain('Zed Future');
  });
});

