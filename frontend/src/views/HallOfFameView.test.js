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
          position: 'Pitcher',
          mlbam_id: '2',
          year: 1980,
        },
        {
          bbref_id: 'b1',
          name: 'Alpha One',
          first_name: 'Alpha',
          last_name: 'One',
          position: 'Shortstop',
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
    expect(cells[0].text()).toBe('Alpha');
    expect(cells[1].text()).toBe('One');
    expect(cells[2].text()).toBe('Shortstop');

    // sort by year
    await wrapper.findAll('th')[4].trigger('click');
    await flushPromises();
    const sortedRows = wrapper.findAll('tbody tr');
    expect(sortedRows[0].text()).toContain('Beta');

    expect(sortedRows[0].html()).toContain('https://www.mlb.com/player/2');
    expect(sortedRows[0].html()).not.toContain('2.0');
  });

  it('sorts years numerically when reversing sort order', async () => {
    fetchHallOfFamePlayers.mockResolvedValue({
      players: [
        {
          bbref_id: 'm1',
          name: 'Minnie Miñoso',
          first_name: 'Minnie',
          last_name: 'Miñoso',
          position: 'Outfielder',
          mlbam_id: '3',
          year: '2022',
        },
        {
          bbref_id: 'f1',
          name: 'Future Star',
          first_name: 'Future',
          last_name: 'Star',
          position: 'Catcher',
          mlbam_id: '4',
          year: '2023',
        },
        {
          bbref_id: 'd1',
          name: 'Dick Allen',
          first_name: 'Dick',
          last_name: 'Allen',
          position: 'First Baseman',
          mlbam_id: '110157',
          year: '2025',
        }
      ],
    });

    const { default: HallOfFameView } = await import('./HallOfFameView.vue');
    const wrapper = mount(HallOfFameView);

    await flushPromises();

    // sort by year descending
    const yearHeader = wrapper.findAll('th')[4];
    await yearHeader.trigger('click');
    await flushPromises();
    await yearHeader.trigger('click');
    await flushPromises();
    const rows2 = wrapper.findAll('tbody tr');
    expect(rows2[0].text()).toContain('Dick');

    // sort by year ascending
    await yearHeader.trigger('click');
    await flushPromises();
    const rows3 = wrapper.findAll('tbody tr');
    const firstRowText = rows3[0].text();
    try {
      expect(firstRowText).toContain('Minnie');
    } catch (err) {
      console.error(`Expected Minnie, got rows3[0].text(): ${firstRowText}`);
      throw err;
    }

    // sort by year descending
    await yearHeader.trigger('click');
    await flushPromises();
    const rows4 = wrapper.findAll('tbody tr');
    expect(rows4[0].text()).toContain('Dick');

  });

  it('handles sorting across columns with accented names and missing ids', async () => {
    fetchHallOfFamePlayers.mockResolvedValue({
      players: [
        {
          bbref_id: 'm1',
          name: 'Minnie Miñoso',
          first_name: 'Minnie',
          last_name: 'Miñoso',
          position: 'Outfielder',
          mlbam_id: '123',
          year: '2022',
        },
        {
          bbref_id: 'z1',
          name: 'Zed Future',
          first_name: 'Zed',
          last_name: 'Future',
          position: 'Pitcher',
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
    expect(rows[0].text()).toContain('Zed');

    // sort by year ascending
    await headers[4].trigger('click');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows[0].text()).toContain('Minnie');

    // sort by mlbam_id descending
    await headers[3].trigger('click');
    await headers[3].trigger('click');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows[0].text()).toContain('Zed');

    // sort by first name descending
    await headers[0].trigger('click');
    await headers[0].trigger('click');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows[0].text()).toContain('Zed');
  });

  it('filters players by position and year', async () => {
    fetchHallOfFamePlayers.mockResolvedValue({
      players: [
        {
          bbref_id: 'p1',
          name: 'Pitcher One',
          first_name: 'Pitcher',
          last_name: 'One',
          position: 'Pitcher',
          mlbam_id: '10',
          year: 1990,
        },
        {
          bbref_id: 'c1',
          name: 'Catcher Two',
          first_name: 'Catcher',
          last_name: 'Two',
          position: 'Catcher',
          mlbam_id: '20',
          year: 2000,
        },
      ],
    });

    const { default: HallOfFameView } = await import('./HallOfFameView.vue');
    const wrapper = mount(HallOfFameView);

    await flushPromises();

    const positionSelect = wrapper.find('[data-test="position-filter"]');
    await positionSelect.setValue('Pitcher');
    await flushPromises();
    let rows = wrapper.findAll('tbody tr');
    expect(rows).toHaveLength(1);
    expect(rows[0].text()).toContain('Pitcher');

    const yearSelect = wrapper.find('[data-test="year-filter"]');
    await yearSelect.setValue('2000');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows).toHaveLength(0);

    await positionSelect.setValue('');
    await yearSelect.setValue('2000');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows).toHaveLength(1);
    expect(rows[0].text()).toContain('Catcher');

    await yearSelect.setValue('');
    await flushPromises();
    rows = wrapper.findAll('tbody tr');
    expect(rows).toHaveLength(2);
  });
});

