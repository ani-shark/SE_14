import api from "./api";

export const getUserCourses = async (userId: number) => {
  const response = await api.get(`/week/dashboard/${userId}`);
  return response.data;
};

export const createWeek = async (name: string, course_id: number) => {
  const response = await api.post('/week/create', { name, course_id });
  return response.data;
};

export const getWeeks = async (course_id: number) => {
  const response = await api.get(`/week/all?course_id=${course_id}`);
  return response.data;
};

export const deleteWeek = async (id: number) => {
  await api.delete(`/week/${id}`);
};
