const noop = () => {};

const logger = import.meta.env.PROD
  ? { info: noop, warn: noop, error: noop }
  : {
      info: (...args) => console.info(...args),
      warn: (...args) => console.warn(...args),
      error: (...args) => console.error(...args),
    };

export default logger;
