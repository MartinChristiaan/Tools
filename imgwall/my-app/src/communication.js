import axios from 'axios';

const SERVER_URL = 'http://localhost:3333';

const api = {
  // updateWeight: (title, weight) => {
  //   return axios.put(`${SERVER_URL}/update_weight`, { title, weight });
  // },
  getItems: () => {
    return axios.get(`${SERVER_URL}/get_items`);
  },
  getImageGallery: (id) => {
    return axios.get(`${SERVER_URL}/get_gallery:` + id.toString());
  },
  updateImages: () => {
    return axios.get(`${SERVER_URL}/update`);
  },


};

export default api;
