import api from "./api";

export const signIn = async (email: string) => {
  try {
    const response = await api.post("/auth/signin", { email });

    console.log("Sign-in API Response:", response.data);

    if (!response.data.id || !response.data.role) {
      console.error("Invalid response structure:", response.data);
      throw new Error("Invalid response from server.");
    }

    localStorage.setItem("user_id", response.data.id);
    localStorage.setItem("user_role", response.data.role);
    localStorage.setItem("user_email", response.data.email);
    localStorage.setItem("access_token", response.data.access_token);
    localStorage.setItem("refresh_token", response.data.refresh_token);

    return response.data;
  } catch (error) {
    console.error("Sign-in failed:", error);
    throw error;
  }
};