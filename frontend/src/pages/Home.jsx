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

    const data = {
      mic_value: micValue.trim(),
      bacteria: selectedBacteria[0].trim(),
      antibiotic: selectedAntibiotics[0].trim(),
    };

    console.log("Sending sanitized data:", data);

    try {
      const result = await predictResistance(data);
      console.log("Prediction result:", result);
      setPrediction(result);
    } catch (error) {
      console.error("Error during prediction:", error);
      alert("Failed to get prediction. Please try again.");
    }
  };

  const closePopup = () => {
    setPrediction(null);
  };

  return (
    <div className="p-8 space-y-6 bg-gray-100 min-h-screen">
      <header className="p-4 bg-white rounded shadow">
        <h1 className="text-2xl font-bold text-gray-800">Antibiotic Resistance Prediction Tool</h1>
      </header>

      <div className="p-4 bg-white rounded shadow">
        <h2 className="font-bold text-lg mb-4 text-gray-700">Patient Details</h2>
        <div className="space-y-4">
          <div>
            <label className="block font-semibold text-gray-600">Name</label>
            <input
              type="text"
              value={patientName}
              onChange={(e) => setPatientName(e.target.value)}
              placeholder="Enter patient's name"
              className="w-full p-2 border rounded "
            />
          </div>
          <div>
            <label className="block font-semibold text-gray-600">Age</label>
            <input
              type="number"
              value={patientAge}
              onChange={(e) => setPatientAge(e.target.value)}
              placeholder="Enter patient's age"
              className="w-full p-2 border rounded"
            />
          </div>
          <div>
            <label className="block font-semibold text-gray-600">Gender</label>
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

      <div className="p-4 bg-white rounded shadow">
        <h2 className="font-bold text-lg mb-4 text-gray-700">Select Bacteria</h2>
        <div className="flex flex-wrap gap-4">
          <BacteriaCheckbox
            bacteriaList={bacteriaList}
            selectedBacteria={selectedBacteria}
            setSelectedBacteria={setSelectedBacteria}
          />
        </div>
      </div>

      <div className="p-4 bg-white rounded shadow">
        <h2 className="font-bold text-lg mb-4 text-gray-700">Select Antibiotics</h2>
        <div className="flex flex-wrap gap-4">
          <AntibioticsCheckbox
            antibioticsList={antibioticsList}
            selectedAntibiotics={selectedAntibiotics}
            setSelectedAntibiotics={setSelectedAntibiotics}
          />
        </div>
      </div>

      <MICInput micValue={micValue} setMicValue={setMicValue} />

      <div className="text-right">
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Predict
        </button>
      </div>

      {prediction && (
  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div className="bg-white w-3/4 max-w-2xl max-h-[80vh] p-6 rounded shadow-lg relative overflow-y-auto">
      <button
        className="absolute top-2 right-2 text-gray-600 hover:text-red-600"
        onClick={closePopup}
      >
        ✕
      </button>
      <h2 className="font-bold text-lg text-gray-700">Prediction Result</h2>
      <p className="mt-2">
        <strong>Primary Antibiotic ({selectedAntibiotics[0]}):</strong>{" "}
        {prediction.interpretation}
      </p>
      {Object.entries(prediction.other_interpretations).length > 0 && (
        <div>
          {Object.entries(prediction.other_interpretations)
            .filter(([, interpretation]) => interpretation === "Resistant")
            .length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold text-gray-700">You may be resistant to:</h4>
              <ul className="list-disc ml-5 text-gray-600">
                {Object.entries(prediction.other_interpretations)
                  .filter(([, interpretation]) => interpretation === "Resistant")
                  .map(([antibiotic]) => (
                    <li key={antibiotic}>{antibiotic}</li>
                  ))}
              </ul>
            </div>
          )}
          {Object.entries(prediction.other_interpretations)
            .filter(([, interpretation]) => interpretation === "Sensitive")
            .length > 0 && (
            <div className="mt-4">
              <h4 className="font-semibold text-gray-700">You may be sensitive to:</h4>
              <ul className="list-disc ml-5 text-gray-600">
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
  </div>
)}
    </div>
  );
};

export default Home;
