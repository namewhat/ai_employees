import axios from 'axios';

const api = axios.create({
    baseURL: '/api'
});

export const wordApi = {
    getRandomWord: async (type = null) => {
        const params = type ? { word_type: type } : {};
        const response = await api.get('/word/random', { params });
        return response.data;
    },

    getWords: async () => {
        const response = await api.get('/word/list');
        return response.data;
    },

    importWords: async (words) => {
        const response = await api.post('/word/import', words);
        return response.data;
    },

    deleteWord: async (id) => {
        const response = await api.delete(`/word/${id}`);
        return response.data;
    },

    getWordProgress: async (wordId) => {
        const response = await api.get(`/word/progress/${wordId}`);
        return response.data;
    }
}; 