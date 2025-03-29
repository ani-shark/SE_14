import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/", 
  withCredentials: true, 
});

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("access_token"); 
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;