import axios from "axios";

const api = axios.create({
  baseURL: "https://digital-twin-latest.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
