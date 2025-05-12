import axios from 'axios';
import { API_BASE_URL } from '../../../common/constants';

export const braFittingService = {
  getRecommendation: async (text) => {
    const response = await axios.post(`${API_BASE_URL}/recommendation`, {
      text: text 
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response?.data?.data;
  }
};