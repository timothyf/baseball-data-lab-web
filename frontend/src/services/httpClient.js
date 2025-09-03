import axios from 'axios';
import logger from '../utils/logger';

const baseURL = import.meta.env.VITE_API_BASE_URL || '/api';

const httpClient = axios.create({ baseURL });

httpClient.interceptors.request.use(
  (config) => {
    logger.info(
      `Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`,
    );
    return config;
  },
  (error) => {
    logger.error('Request error:', error);
    return Promise.reject(error);
  },
);

httpClient.interceptors.response.use(
  (response) => {
    logger.info(`Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    const message = error.response
      ? `API Error: ${error.response.status} ${error.response.statusText}`
      : error.message;
    logger.error(message);
    return Promise.reject(new Error(message));
  },
);

export default httpClient;
