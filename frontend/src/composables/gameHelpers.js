// Utility functions for formatting game data

function formatTime(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleTimeString(undefined, {
    hour: 'numeric',
    minute: '2-digit'
  });
}

export function gameTime(game) {
  if (game?.status?.abstractGameState === 'Live') return 'LIVE';
  if (game?.status?.detailedState === 'Final') return 'Final';
  return formatTime(game.gameDate);
}

export function teamAbbrev(team) {
  return team?.abbreviation || team?.teamCode || team?.name || '';
}

export function shortName(name) {
  if (!name) return '';
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}. ${parts.slice(1).join(' ')}`;
  }
  return name;
}

