import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000"; // ✅ Ensure correct backend URL

export const signIn = async (email: string) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/signin`, { email }, { withCredentials: true });

    console.log("Sign-in API Response:", response.data); // ✅ Debugging
    
    // ✅ Ensure response contains role
    if (!response.data.role) {
      console.error("Error: Role is missing from API response.");
      throw new Error("Invalid response. Missing role.");
    }

    return response.data; // ✅ Return role
  } catch (error) {
    console.error("Sign-in failed:", error);
    throw error;
  }
};
