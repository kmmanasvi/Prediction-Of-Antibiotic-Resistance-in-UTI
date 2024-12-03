import React, { useEffect, useState } from "react";
import { fetchOptions, predictResistance } from "../api";
import BacteriaCheckbox from "../components/BacteriaCheckbox";
import AntibioticsCheckbox from "../components/AntibioticsCheckbox";
import MICInput from "../components/MICInput";

const Home = () => {
  const [bacteriaList, setBacteriaList] = useState([]);
  const [antibioticsList, setAntibioticsList] = useState([]);
  const [selectedBacteria, setSelectedBacteria] = useState([]);
  const [selectedAntibiotics, setSelectedAntibiotics] = useState([]);
  const [micValue, setMicValue] = useState("");
  const [prediction, setPrediction] = useState(null);

  // New State for Patient Details
  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [patientGender, setPatientGender] = useState("");

  useEffect(() => {
    fetchOptions().then((data) => {
      setBacteriaList(data.bacteria);
      setAntibioticsList(data.antibiotics);
    });
  }, []);

  const handleSubmit = async () => {
    if (!micValue || selectedBacteria.length === 0 || selectedAntibiotics.length === 0) {
      alert("Please fill in all fields.");
      return;
    }

    // Sanitize input data
    const data = {
      mic_value: micValue.trim(),
      bacteria: selectedBacteria[0].trim(),
      antibiotic: selectedAntibiotics[0].trim(),
    };

    console.log("Sending sanitized data:", data); // Log sanitized data

    try {
      const result = await predictResistance(data);
      console.log("Prediction result:", result); // Log the result from the backend
      setPrediction(result); // Update state with the result
    } catch (error) {
      console.error("Error during prediction:", error);
      alert("Failed to get prediction. Please try again.");
    }
  };

  return (
    <div className="p-8 space-y-4">
      {/* Patient Details Section */}
      <div className="p-4 border rounded shadow">
        <h2 className="font-bold text-lg">Patient Details</h2>
        <div className="space-y-2">
          <div>
            <label className="block font-semibold">Name</label>
            <input
              type="text"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              placeholder="Enter patient's name"
              className="w-full p-2 border rounded"
            />
          </div>
          <div>
            <label className="block font-semibold">Age</label>
            <input
              type="number"
              value={patientAge}
              onChange={(e) => setPatientAge(e.target.value)}
              placeholder="Enter patient's age"
              className="w-full p-2 border rounded"
            />
          </div>
          <div>
            <label className="block font-semibold">Gender</label>
            <select
              value={patientGender}
              onChange={(e) => setPatientGender(e.target.value)}
              className="w-full p-2 border rounded"
            >
              <option value="">Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>
        </div>
      </div>

      {/* Bacteria Checkbox */}
      <BacteriaCheckbox
        bacteriaList={bacteriaList}
        selectedBacteria={selectedBacteria}
        setSelectedBacteria={setSelectedBacteria}
      />

      {/* Antibiotics Checkbox */}
      <AntibioticsCheckbox
        antibioticsList={antibioticsList}
        selectedAntibiotics={selectedAntibiotics}
        setSelectedAntibiotics={setSelectedAntibiotics}
      />

      {/* MIC Input */}
      <MICInput micValue={micValue} setMicValue={setMicValue} />

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
      >
        Predict
      </button>

      {/* Prediction Result */}
{prediction && (
  <div className="p-4 border rounded shadow">
    <h2 className="font-bold text-lg">Prediction Result</h2>
    <p>
      <strong>Primary Antibiotic ({selectedAntibiotics[0]}):</strong> {prediction.interpretation}
    </p>
    {/* <h3 className="font-semibold text-md mt-2">Other Interpretations for this Bacteria:</h3> */}

    {/* Segregating Resistant and Sensitive */}
    {Object.entries(prediction.other_interpretations).length > 0 && (
      <div>
        {/* Resistant Antibiotics */}
        {Object.entries(prediction.other_interpretations).filter(([, interpretation]) => interpretation === "Resistant").length > 0 && (
          <div className="mt-4">
            <h4 className="font-semibold ">You may be resistant to:</h4>
            <ul className="list-disc ml-5">
              {Object.entries(prediction.other_interpretations)
                .filter(([, interpretation]) => interpretation === "Resistant")
                .map(([antibiotic]) => (
                  <li key={antibiotic}>{antibiotic}</li>
                ))}
            </ul>
          </div>
        )}

        {/* Sensitive Antibiotics */}
        {Object.entries(prediction.other_interpretations).filter(([, interpretation]) => interpretation === "Sensitive").length > 0 && (
          <div className="mt-4">
            <h4 className="font-semibold">You may be sensitive to:</h4>
            <ul className="list-disc ml-5">
              {Object.entries(prediction.other_interpretations)
                .filter(([, interpretation]) => interpretation === "Sensitive")
                .map(([antibiotic]) => (
                  <li key={antibiotic}>{antibiotic}</li>
                ))}
            </ul>
          </div>
        )}
      </div>
    )}
  </div>
)}

    </div>
  );
};

export default Home;

