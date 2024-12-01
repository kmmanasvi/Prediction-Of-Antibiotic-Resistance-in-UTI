import axios from "axios";

// const API_BASE_URL = "http://localhost:5000";

// export const fetchOptions = async () => {
//   const response = await axios.get(`${API_BASE_URL}/options`);
//   return response.data;
// };

export const fetchOptions = async () => {
  try {
    const response = await axios.get("http://localhost:5000/get-options");
    return response.data;
  } catch (error) {
    console.error("Error fetching options:", error.response || error);
    alert("Failed to fetch options. Please try again.");
    throw error;
  }
};


// export const predictResistance = async (data) => {
//   const response = await axios.post(`${API_BASE_URL}/predict`, data);
//   return response.data;
// };

export const predictResistance = async (data) => {
  try {
    const response = await axios.post("http://localhost:5000/predict", data);
    return response.data;
  } catch (error) {
    console.error("Error in prediction API call:", error.response || error);
    if (error.response) {
      alert(`Error: ${error.response.data.error || "Unknown error"}`);
    }
    throw error; // rethrow to be handled in the component
  }
};