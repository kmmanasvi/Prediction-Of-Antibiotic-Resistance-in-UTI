// import React, { useEffect, useState } from "react";
// import { fetchOptions, predictResistance } from "../api";
// import BacteriaCheckbox from "../components/BacteriaCheckbox";
// import AntibioticsCheckbox from "../components/AntibioticsCheckbox";

// const Home = () => {
//   const [bacteriaList, setBacteriaList] = useState([]);
//   const [antibioticsList, setAntibioticsList] = useState([]);
//   const [selectedBacteria, setSelectedBacteria] = useState([]);
//   const [selectedAntibiotics, setSelectedAntibiotics] = useState([]);
//   const [prediction, setPrediction] = useState(null);

//   // New State for Patient Details
//   const [patientName, setPatientName] = useState("");
//   const [patientAge, setPatientAge] = useState("");
//   const [patientGender, setPatientGender] = useState("");

//   // New state for exposure level
//   const [exposureLevel, setExposureLevel] = useState("");

//   useEffect(() => {
//     fetchOptions().then((data) => {
//       setBacteriaList(data.bacteria);
//       setAntibioticsList(data.antibiotics);
//     });
//   }, []);

//   const handleSubmit = async () => {
//     if (
//       selectedBacteria.length === 0 ||
//       selectedAntibiotics.length === 0 ||
//       !exposureLevel
//     ) {
//       alert("Please fill in all fields.");
//       return;
//     }

//     const data = {
//       bacteria: selectedBacteria[0].trim(),
//       antibiotic: selectedAntibiotics[0].trim(),
//       exposure_level: exposureLevel, // Adding the exposure level to the data
//     };

//     console.log("Sending sanitized data:", data);

//     try {
//       const result = await predictResistance(data);
//       console.log("Prediction result:", result);
//       setPrediction(result);
//     } catch (error) {
//       console.error("Error during prediction:", error);
//       alert("Failed to get prediction. Please try again.");
//     }
//   };


//   const closePopup = () => {
//     setPrediction(null);
//   };

//   return (
//     <div className="p-8 space-y-6 bg-gray-100 min-h-screen">
//       <header className="p-4 bg-white rounded shadow">
//         <h1 className="text-2xl font-bold text-gray-800">
//           Antibiotic Resistance Prediction Tool
//         </h1>
//       </header>

//       <div className="p-4 bg-white rounded shadow">
//         <h2 className="font-bold text-lg mb-4 text-gray-700">Patient Details</h2>
//         <div className="space-y-4">
//           <div>
//             <label className="block font-semibold text-gray-600">Name</label>
//             <input
//               type="text"
//               value={patientName}
//               onChange={(e) => setPatientName(e.target.value)}
//               placeholder="Enter patient's name"
//               className="w-full p-2 border rounded "
//             />
//           </div>
//           <div>
//             <label className="block font-semibold text-gray-600">Age</label>
//             <input
//               type="number"
//               value={patientAge}
//               onChange={(e) => setPatientAge(e.target.value)}
//               placeholder="Enter patient's age"
//               className="w-full p-2 border rounded"
//             />
//           </div>
//           <div>
//             <label className="block font-semibold text-gray-600">Gender</label>
//             <select
//               value={patientGender}
//               onChange={(e) => setPatientGender(e.target.value)}
//               className="w-full p-2 border rounded"
//             >
//               <option value="">Select gender</option>
//               <option value="Male">Male</option>
//               <option value="Female">Female</option>
//             </select>
//           </div>
//         </div>
//       </div>

//       {/* New Section for Exposure Level */}
//       <div className="p-4 bg-white rounded shadow">
//         <h2 className="font-bold text-lg mb-4 text-gray-700">
//           How frequently have you been exposed to antibiotics?
//         </h2>
//         <div className="space-y-4">
//           <select
//             value={exposureLevel}
//             onChange={(e) => setExposureLevel(Number(e.target.value))}  // Convert to number here
//             className="w-full p-2 border rounded"
//           >
//             <option value="">Select Exposure Level</option>
//             <option value="1">
//               Barely needed antibiotics, just a few here and there 
//             </option>
//             <option value="2">
//               Took them a few times for infections 
//             </option>
//             <option value="3">
//               Relied on antibiotics for multiple or serious treatments 
//             </option>
//           </select>
//         </div>
//       </div>

//       <div className="p-4 bg-white rounded shadow">
//         <h2 className="font-bold text-lg mb-4 text-gray-700">Select Bacteria</h2>
//         <div className="flex flex-wrap gap-4">
//           <BacteriaCheckbox
//             bacteriaList={bacteriaList}
//             selectedBacteria={selectedBacteria}
//             setSelectedBacteria={setSelectedBacteria}
//           />
//         </div>
//       </div>

//       <div className="p-4 bg-white rounded shadow">
//         <h2 className="font-bold text-lg mb-4 text-gray-700">Select Antibiotics</h2>
//         <div className="flex flex-wrap gap-4">
//           <AntibioticsCheckbox
//             antibioticsList={antibioticsList}
//             selectedAntibiotics={selectedAntibiotics}
//             setSelectedAntibiotics={setSelectedAntibiotics}
//           />
//         </div>
//       </div>

//       <div className="text-right">
//         <button
//           onClick={handleSubmit}
//           className="bg-blue-500 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
//         >
//           Predict
//         </button>
//       </div>

//       {prediction && (
//         <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
//           <div className="bg-white w-3/4 max-w-2xl max-h-[80vh] p-6 rounded shadow-lg relative overflow-y-auto">
//             <button
//               className="absolute top-2 right-2 text-gray-600 hover:text-red-600"
//               onClick={closePopup}
//             >
//               ✕
//             </button>
//             <h2 className="font-bold text-lg text-gray-700">Prediction Result</h2>
//             <p className="mt-2">
//               <strong>User Interpretation (Exposure Level {exposureLevel}):</strong>{" "}
//               <span>{prediction.user_interpretation}</span>
//             </p>
//             <p className="mt-2">
//               <strong>Model Interpretation (Primary Antibiotic {selectedAntibiotics[0]}):</strong>{" "}
//               <span>{prediction.model_interpretation}</span>
//             </p>
//             <p className="mt-2">
//               You may be <strong>{prediction.model_interpretation}</strong> to{" "}
//               <strong>{selectedAntibiotics[0]}</strong>.
//             </p>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Home;

import React, { useEffect, useState } from "react";
import { fetchOptions,  predictResistance } from "../api";
import BacteriaCheckbox from "../components/BacteriaCheckbox";
import AntibioticsCheckbox from "../components/AntibioticsCheckbox";

const Home = () => {
  const [bacteriaList, setBacteriaList] = useState([]);
  const [antibioticsList, setAntibioticsList] = useState([]);
  const [selectedBacteria, setSelectedBacteria] = useState([]);
  const [selectedAntibiotics, setSelectedAntibiotics] = useState([]);
  const [prediction, setPrediction] = useState(null);

  // New State for Patient Details
  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [patientGender, setPatientGender] = useState("");

  // New state for exposure level
  const [exposureLevel, setExposureLevel] = useState("");

  // Fetch initial bacteria options on mount
  useEffect(() => {
    // Assuming fetchOptions (with no param) returns full bacteria list
    fetchOptions().then((data) => {
      setBacteriaList(data.bacteria);
      // Initially, antibioticsList can be empty or full list.
      setAntibioticsList([]);
    });
  }, []);

  // When a bacteria is selected, fetch antibiotics options for that bacteria
  useEffect(() => {
    if (selectedBacteria.length > 0) {
      // Here we assume fetchOptions can take an optional parameter to filter by bacteria.
      fetchOptions({ bacteria: selectedBacteria[0].trim() }).then((data) => {
        setAntibioticsList(data.antibiotics);
        // Reset selected antibiotics if the list changes.
        setSelectedAntibiotics([]);
      });
    } else {
      // If no bacteria is selected, clear the antibiotics list.
      setAntibioticsList([]);
      setSelectedAntibiotics([]);
    }
  }, [selectedBacteria]);

  // useEffect(() => {
  //   if (selectedBacteria.length > 0 && exposureLevel) {
  //     fetchOptions(selectedBacteria[0].trim(), exposureLevel)
  //       .then((data) => {
  //         setAntibioticsList(data.antibiotics);
  //         setSelectedAntibiotics([]);
  //       })
  //       .catch((error) => {
  //         console.error("Failed to fetch antibiotics:", error);
  //       });
  //   } else {
  //     setAntibioticsList([]);
  //     setSelectedAntibiotics([]);
  //   }
  // }, [selectedBacteria, exposureLevel]);  


  const handleSubmit = async () => {
    if (
      selectedBacteria.length === 0 ||
      selectedAntibiotics.length === 0 ||
      !exposureLevel
    ) {
      alert("Please fill in all fields.");
      return;
    }

    const data = {
      bacteria: selectedBacteria[0].trim(),
      antibiotic: selectedAntibiotics[0].trim(),
      exposure_level: exposureLevel, // exposure level as number 1,2, or 3
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

  const interpretationMap = {
    S: "Sensitive",
    R: "Resistant",
  };

// import React, { useEffect, useState } from "react";
// import { fetchOptions, predictResistance } from "../api";
// import BacteriaCheckbox from "../components/BacteriaCheckbox";
// import AntibioticsCheckbox from "../components/AntibioticsCheckbox";

// const Home = () => {
//   const [bacteriaList, setBacteriaList] = useState([]);
//   const [antibioticsList, setAntibioticsList] = useState([]);
//   const [selectedBacteria, setSelectedBacteria] = useState([]);
//   const [selectedAntibiotics, setSelectedAntibiotics] = useState([]);
//   const [prediction, setPrediction] = useState(null);

//   // New State for Patient Details
//   const [patientName, setPatientName] = useState("");
//   const [patientAge, setPatientAge] = useState("");
//   const [patientGender, setPatientGender] = useState("");

//   // New state for exposure level
//   const [exposureLevel, setExposureLevel] = useState("");

//   // Fetch initial bacteria options on mount
//   useEffect(() => {
//     // Assuming fetchOptions (with no param) returns full bacteria list
//     fetchOptions().then((data) => {
//       setBacteriaList(data.bacteria);
//       // Initially, antibioticsList can be empty or full list.
//       setAntibioticsList([]);
//     });
//   }, []);

//   // When a bacteria is selected, fetch antibiotics options for that bacteria
//   useEffect(() => {
//     if (selectedBacteria.length > 0) {
//       // Here we assume fetchOptions can take an optional parameter to filter by bacteria.
//       fetchOptions({ bacteria: selectedBacteria[0].trim() }).then((data) => {
//         setAntibioticsList(data.antibiotics);
//         // Reset selected antibiotics if the list changes.
//         setSelectedAntibiotics([]);
//       });
//     } else {
//       // If no bacteria is selected, clear the antibiotics list.
//       setAntibioticsList([]);
//       setSelectedAntibiotics([]);
//     }
//   }, [selectedBacteria]);

//   const handleSubmit = async () => {
//     if (
//       selectedBacteria.length === 0 ||
//       selectedAntibiotics.length === 0 ||
//       !exposureLevel
//     ) {
//       alert("Please fill in all fields.");
//       return;
//     }

//     const data = {
//       bacteria: selectedBacteria[0].trim(),
//       antibiotic: selectedAntibiotics[0].trim(),
//       exposure_level: exposureLevel, // exposure level as number 1,2, or 3
//     };

//     console.log("Sending sanitized data:", data);

//     try {
//       const result = await predictResistance(data);
//       console.log("Prediction result:", result);
//       setPrediction(result);
//     } catch (error) {
//       console.error("Error during prediction:", error);
//       alert("Failed to get prediction. Please try again.");
//     }
//   };

//   const closePopup = () => {
//     setPrediction(null);
//   };

//   const interpretationMap = {
//     S: "Sensitive",
//     R: "Resistant",
//   };

  return (
    <div className="p-8 space-y-6 bg-gray-100 min-h-screen">
      <header className="p-4 bg-white rounded shadow">
        <h1 className="text-2xl font-bold text-gray-800">
          Antibiotic Resistance Prediction Tool
        </h1>
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
              className="w-full p-2 border rounded"
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

      {/* New Section for Exposure Level */}
      <div className="p-4 bg-white rounded shadow">
        <h2 className="font-bold text-lg mb-4 text-gray-700">
          How frequently have you been exposed to antibiotics?
        </h2>
        <div className="space-y-4">
          <select
            value={exposureLevel}
            onChange={(e) => setExposureLevel(Number(e.target.value))} // Convert to number
            className="w-full p-2 border rounded"
          >
            <option value="">Select Exposure Level</option>
            <option value="1">
              Barely needed antibiotics, just a few here and there for infections
            </option>
            {/* <option value="2">
              Took them a few times for infections
            </option> */}
            <option value="2">
              Relied on antibiotics for multiple or serious treatments
            </option>
          </select>
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

      {/* Render Antibiotics selection only if a bacteria is selected */}
      {selectedBacteria.length > 0 && (
        <div className="p-4 bg-white rounded shadow">
          <h2 className="font-bold text-lg mb-4 text-gray-700">
            Select Antibiotic
          </h2>
          <div className="flex flex-wrap gap-4">
            <AntibioticsCheckbox
              antibioticsList={antibioticsList}
              selectedAntibiotics={selectedAntibiotics}
              setSelectedAntibiotics={setSelectedAntibiotics}
            />
          </div>
        </div>
      )}

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
          <div className="mt-2">
            <div className="bg-white rounded-xl shadow-lg p-6 space-y-4 max-w-xl mx-auto">
          <h2 className="text-2xl font-bold text-[#055484]">🧪 Prediction Result</h2>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-700 font-medium">Exposure Level:</p>
              <p className="text-md font-semibold">{exposureLevel}</p>
            </div>

            <div>
              <p className="text-gray-700 font-medium">Bacteria Identified:</p>
              <p className="text-md font-semibold">{selectedBacteria[0]}</p>
            </div>

            <div>
              <p className="text-gray-700 font-medium">Antibiotic Prescribed:</p>
              <p className="text-md font-semibold">{selectedAntibiotics[0]}</p>
            </div>

            <div>
              <p className="text-gray-700 font-medium">Predicted MIC Value:</p>
              <p className="text-md font-semibold">
                {prediction.mic_value} µg/mL
                <span className="block text-sm text-gray-600">
                  (Minimum Inhibitory Concentration)
                </span>
              </p>
            </div>
          </div>

          <div
            className={`py-3 px-4 rounded-xl text-center text-white ${
              prediction.interpretation === "R"
                ? "bg-red-500"
                : "bg-green-500"
            }`}
          >
            ⚠️ Based on the predicted MIC value, you may be{" "}
            <strong>{interpretationMap[prediction.interpretation] || prediction.interpretation}</strong>{" "}
            to <strong>{selectedAntibiotics[0]}</strong>.
          </div>

          <p className="text-sm text-gray-500">
           The MIC value represents the lowest concentration of the antibiotic required
            to inhibit the growth of the identified bacteria.
          </p>
          </div>

          </div>

          </div>
        </div>
      )}
    </div>
  );
};

export default Home;

