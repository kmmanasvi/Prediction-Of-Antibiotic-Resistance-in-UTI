import axios from "axios";

// export const fetchOptions = async () => {
//   try {
//     const response = await axios.get("http://localhost:5000/get-options");
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching options:", error.response || error);
//     alert("Failed to fetch options. Please try again.");
//     throw error;
//   }
// };

export const fetchOptions = async (bacteria, exposureLevel) => {
  try {
    const response = await axios.get("http://localhost:5000/get-options", {
      params: { bacteria, exposure_level: exposureLevel },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching options:", error.response || error);
    alert("Failed to fetch options. Please try again.");
    throw error;
  }
};


export const fetchAntibioticsByBacteria = async (bacteria) => {
  const response = await fetch("http://localhost:5000/get-options", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ bacteria }),
  });
  return response.json();
};


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