// import React from "react";

// const PredictionResult = ({ prediction }) => {
//   return (
//     <div className="mt-4 p-4 border rounded">
//       <h2 className="text-lg font-bold">Prediction Result</h2>
//       <p>Interpretation: {prediction.interpretation}</p>
//       <h3 className="text-md font-bold mt-2">Other Predictions:</h3>
//       <ul>
//         {Object.entries(prediction.other_interpretations).map(([antibiotic, result]) => (
//           <li key={antibiotic}>
//             {antibiotic}: {result === 0 ? "Sensitive" : "Resistant"}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default PredictionResult;

import React from "react";

const PredictionResult = ({ prediction }) => {
  if (!prediction) {
    return (
      <div className="mt-4 p-4 border rounded">
        <h2 className="text-lg font-bold">Prediction Result</h2>
        <p className="text-gray-500">No prediction available. Please try again.</p>
      </div>
    );
  }

  const { interpretation, other_interpretations = {} } = prediction;

  return (
    <div className="mt-4 p-4 border rounded shadow">
      <h2 className="text-lg font-bold">Prediction Result</h2>
      <p>
        <span className="font-semibold">Interpretation:</span>{" "}
        {interpretation || "N/A"}
      </p>
      {Object.keys(other_interpretations).length > 0 ? (
        <>
          <h3 className="text-md font-bold mt-2">Other Predictions:</h3>
          <ul className="list-disc list-inside">
            {Object.entries(other_interpretations).map(([antibiotic, result]) => (
              <li key={antibiotic} className="mt-1">
                <span className="font-semibold">{antibiotic}:</span>{" "}
                {result === 0 ? "Sensitive" : "Resistant"}
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p className="text-gray-500 mt-2">No additional predictions available.</p>
      )}
    </div>
  );
};

export default PredictionResult;
