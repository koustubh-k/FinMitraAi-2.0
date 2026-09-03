/**
 * Application environment configuration
 * Centralizes access to environment variables such as API URLs.
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const config = {
  apiUrl: API_BASE_URL,
  healthEndpoint: `${API_BASE_URL}/health`,
  rootEndpoint: `${API_BASE_URL}/`,
};

export default config;
