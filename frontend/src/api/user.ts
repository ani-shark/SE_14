import api from "./api";

export const getUserCourses = async (userId: string) => {
    const token = localStorage.getItem("access_token");  
    if (!token) {
        throw new Error("Authorization token is missing");
    }

    const response = await api.get(`/week/user/courses`, {
        params: { user_id: userId },
        headers: {
            Authorization: `Bearer ${token}` 
        }
    });

    return response.data;
};
