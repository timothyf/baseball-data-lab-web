import equal from 'fast-deep-equal';

/**
 * Deeply compares two values for equality.
 *
 * @param {*} a - First value to compare.
 * @param {*} b - Second value to compare.
 * @returns {boolean} True if the values are deeply equal, otherwise false.
 */
export function deepEqual(a, b) {
  return equal(a, b);
}

export default deepEqual;
