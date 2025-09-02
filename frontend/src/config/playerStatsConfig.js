export const standardHittingFields = ['team','atBats', 'runs','hits', 'totalBases', 'doubles', 'triples',
  'homeRuns', 'rbi', 'avg','baseOnBalls', 'intentionalWalks', 'strikeOuts', 'stolenBases', 'caughtStealing',
  'obp', 'slg', 'ops'];

export const advancedHittingFields = ['team','plateAppearances', 'totalBases', 'extraBaseHits', 'hitByPitch', 'sacBunts',
  'sacFlies','babip', 'gidp','gidpOpp', 'numberOfPitches', 'pitchesPerPlateAppearance',
  'reachedOnError', 'leftOnBase', 'walkOffs'];

export const standardPitchingFields = ['team', 'wins', 'losses', 'era', 'gamesPitched', 'gamesStarted', 'completeGames',
                                       'strikeOuts','shutouts','holds','saves','saveOpportunities', 'inningsPitched','hits',
                                      'runs','earnedRuns','homeRuns','numberOfPitches','hitBatsmen','baseOnBalls',
                                      'intentionalWalks','strikeOuts','avg','whip','groundOutsToAirouts'];

export const advancedPitchingFields = ['team','qualityStarts','gamesFinished', 'doubles', 'triples', 'gidp','gidpOpp',
  'wildPitches','balks','stolenBases','caughtStealing','pickoffs','strikePercentage',
  'pitchesPerInning','pitchesPerPlateAppearance'];

// Groups of related split codes used to display logical sections in the
// splits tables. Adding a new group here will automatically provide visual
// separation in the PlayerSplits component.
export const splitTypeGroups = [
  ['h', 'a'],          // Home/Away
  ['vl', 'vr'],        // vs. L / vs. R
  ['d', 'n'],          // Day/Night
  ['preas', 'posas'],  // Pre/Post All-Star
  ['val', 'vnl'],      // vs. AL / vs. NL
  ['r0', 'r123', 'ron'], // Base state
  ['ac', 'bc']         // Count leverage
];

export const battingSplitTypes = splitTypeGroups.flat();

export const pitchingSplitTypes = splitTypeGroups.flat();

export const splitTypeLabels = {
  h: 'Home',
  a: 'Away',
  vl: 'vs. L',
  vr: 'vs. R',
  d: 'Day',
  n: 'Night',
  preas: 'Pre AS',
  posas: 'Post AS',
  val: 'vs. AL',
  vnl: 'vs. NL',
  r0: 'Bases Empty',
  r123: 'Bases Loaded',
  ron: 'Runners on Base',
  ac: 'Ahead in Count',
  bc: 'Behind in Count'
};

export const fieldLabels = {
  atBats: 'AB',
  hits: 'H',
  doubles: '2B',
  triples: '3B',
  avg: 'AVG',
  runs: 'R',
  homeRuns: 'HR',
  rbi: 'RBI',
  inningsPitched: 'IP',
  era: 'ERA',
  strikeOuts: 'SO',
  wins: 'W',
  losses: 'L',
  team: 'Team',
  baseOnBalls: 'BB',
  intentionalWalks: 'IBB',
  stolenBases: 'SB',
  caughtStealing: 'CS',
  obp: 'OBP',
  slg: 'SLG',
  ops: 'OPS',
  totalBases: 'TB',
  extraBaseHits: 'XBH',
  plateAppearances: 'PA',
  hitByPitch: 'HBP',
  sacBunts: 'SAC B',
  sacFlies: 'SAC F',
  babip: 'BABIP',
  gidp: 'GIDP',
  gidpOpp: 'GIDPO',
  numberOfPitches: 'NP',
  pitchesPerPlateAppearance: 'P/PA',
  reachedOnError: 'ROE',
  leftOnBase: 'LOB',
  walkOffs: 'WO',
  qualityStarts: 'QS',
  gamesFinished: 'GF',
  wildPitches: 'WP',
  balks: 'BK',
  pickoffs: 'PK',
  strikePercentage: 'S%',
  pitchesPerInning: 'P/IP',
  gamesFinished: 'GF',
  gamesPitched: 'G',
  gamesStarted: 'GS',
  completeGames: 'CG',
  shutouts: 'SHO',
  holds: 'H',
  saves: 'SV',
  saveOpportunities: 'SVO',
  runs: 'R',
  earnedRuns: 'ER',
  numberOfPitches: 'NP',
  hitBatsmen: 'HB',
  whip: 'WHIP',
  groundOutsToAirouts: 'GO/AO'
};
