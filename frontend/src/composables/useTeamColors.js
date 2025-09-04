import { computed, unref } from 'vue';
import teamColors from '../data/teamColors.json';

/**
 * Provides reactive CSS variables for a team's colors.
 *
 * Accepts a ref or value containing the team name and returns a computed
 * style object with `--color-primary`, `--color-secondary` and
 * `--color-accent` variables. Defaults match the site's theme and allow the
 * composable to be reused wherever team-based theming is needed.
 *
 * @param {import('vue').MaybeRef<string>} nameRef - team name or ref to it
 * @returns {import('vue').ComputedRef<Record<string, string>>}
 */
export function useTeamColors(nameRef) {
  return computed(() => {
    const name = unref(nameRef);
    const colors = teamColors[name] || [];
    return {
      '--color-primary': colors[0]?.hex || '#1e3a8a',
      '--color-secondary': colors[1]?.hex || '#1e40af',
      '--color-accent': colors[2]?.hex || '#fbbf24'
    };
  });
}
