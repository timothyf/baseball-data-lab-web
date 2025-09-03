import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || '/api';

const httpClient = axios.create({ baseURL });

httpClient.interceptors.request.use(
  (config) => {
    console.log(`Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

httpClient.interceptors.response.use(
  (response) => {
    console.log(`Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    const message = error.response
      ? `API Error: ${error.response.status} ${error.response.statusText}`
      : error.message;
    console.error(message);
    return Promise.reject(new Error(message));
  }
);

export default httpClient;
