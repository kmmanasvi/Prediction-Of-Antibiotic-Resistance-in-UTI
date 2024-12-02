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

    try {
      const result = await predictResistance(data);
      console.log("Prediction result:", result);  // Log the result from the backend
      setPrediction(result);  // Update state with the result
    } catch (error) {
      console.error("Error during prediction:", error);
      alert("Failed to get prediction. Please try again.");
    }
  };

  return (
    <div className="p-8 space-y-4">
      <BacteriaCheckbox
        bacteriaList={bacteriaList}
        selectedBacteria={selectedBacteria}
        setSelectedBacteria={setSelectedBacteria}
      />
      <AntibioticsCheckbox
        antibioticsList={antibioticsList}
        selectedAntibiotics={selectedAntibiotics}
        setSelectedAntibiotics={setSelectedAntibiotics}
      />
      <MICInput micValue={micValue} setMicValue={setMicValue} />
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
      >
        Predict
      </button>
      {prediction && (
        <div className="p-4 border rounded shadow">
          <h2 className="font-bold text-lg">Prediction Result</h2>
          <p><strong>Primary Antibiotic ({selectedAntibiotics[0]}):</strong> {prediction.interpretation}</p>

          <h3 className="font-semibold text-md mt-2">Other Antibiotic Interpretations:</h3>
          <ul>
            {Object.entries(prediction.other_interpretations).map(([antibiotic, interpretation]) => (
              <li key={antibiotic}>
                <strong>{antibiotic}:</strong> {interpretation}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Home;
