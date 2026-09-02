export class ApiError extends Error {
  constructor(public status: number, public message: string, public data?: any) {
    super(message);
    this.name = "ApiError";
  }
}

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  // In a real app, you'd get this from a secure cookie or context
  // For now we'll use localStorage just to get the architecture in place
  let token = null;
  if (typeof window !== "undefined") {
    token = localStorage.getItem("token");
  }

  const headers = new Headers(options.headers);
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  if (!headers.has("Content-Type") && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMessage = "An error occurred";
    let errorData = null;
    try {
      errorData = await response.json();
      if (Array.isArray(errorData.detail)) {
        errorMessage = errorData.detail.map((e: any) => `${e.loc?.join('.') || 'Field'}: ${e.msg}`).join(', ');
      } else {
        errorMessage = errorData.detail || errorData.message || errorMessage;
      }
      
      if (typeof errorMessage !== "string") {
        errorMessage = JSON.stringify(errorMessage);
      }
    } catch {
      errorMessage = response.statusText;
    }
    throw new ApiError(response.status, errorMessage, errorData);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const apiClient = {
  get: (endpoint: string, options?: RequestInit) => 
    fetchWithAuth(endpoint, { ...options, method: "GET" }),
  
  post: (endpoint: string, data?: any, options?: RequestInit) => 
    fetchWithAuth(endpoint, { 
      ...options, 
      method: "POST", 
      body: data instanceof FormData ? data : JSON.stringify(data) 
    }),
    
  put: (endpoint: string, data?: any, options?: RequestInit) => 
    fetchWithAuth(endpoint, { 
      ...options, 
      method: "PUT", 
      body: data instanceof FormData ? data : JSON.stringify(data) 
    }),
    
  delete: (endpoint: string, options?: RequestInit) => 
    fetchWithAuth(endpoint, { ...options, method: "DELETE" }),
};
