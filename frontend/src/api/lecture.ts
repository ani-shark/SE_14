import api from './api';

export const getLectures = async (week_id: number) => {
  const response = await api.get(`/lecture/${week_id}`);
  return response.data;
};
