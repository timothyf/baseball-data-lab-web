/**
 * Calculate current age in full years based on a birthdate.
 *
 * @param {string|Date} birthDate - Date of birth as a Date object or parseable string.
 * @returns {number|null} Age in years, or null if the date is invalid/missing.
 */
export function calculateAge(birthDate) {
  if (!birthDate) return null;
  const date = birthDate instanceof Date ? birthDate : new Date(birthDate);
  if (isNaN(date.getTime())) return null;

  const today = new Date();
  let age = today.getFullYear() - date.getFullYear();
  const monthDiff = today.getMonth() - date.getMonth();
  const dayDiff = today.getDate() - date.getDate();
  if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
    age--;
  }
  return age;
}

export default calculateAge;
