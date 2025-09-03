import { isRef } from 'vue';

/**
 * Generic helper to fetch and cache data via a Pinia store.
 *
 * @param {Object} options
 * @param {Function} options.getter - Function returning cached data from the store
 * @param {Function} options.setter - Function writing data to the store
 * @param {Function} options.fetcher - Async function fetching fresh data
 * @param {Function|import('vue').Ref} options.assign - Ref to update or callback
 *        receiving fetched data
 * @param {boolean} [options.force=false] - If true, always fetch fresh data
 */
export async function useCachedFetch({
  getter,
  setter,
  fetcher,
  assign,
  force = false,
}) {
  const deepEqual = (a, b) => JSON.stringify(a) === JSON.stringify(b);

  const cached = getter();
  if (cached && !force) {
    if (typeof assign === 'function') assign(cached);
    else if (isRef(assign)) assign.value = cached;
  }

  const fetchAndUpdate = async () => {
    const data = await fetcher();
    const oldData = getter();
    if (!deepEqual(data, oldData)) setter(data);
    if (typeof assign === 'function') assign(data);
    else if (isRef(assign)) assign.value = data;
  };

  if (cached && !force) {
    fetchAndUpdate();
    return;
  }
  await fetchAndUpdate();
}
