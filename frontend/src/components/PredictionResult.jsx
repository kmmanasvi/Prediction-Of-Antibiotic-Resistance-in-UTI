import React from "react";

const PredictionResult = ({ prediction }) => {
  // If no prediction is available, display a message
  if (!prediction) {
    return (
      <div className="mt-4 p-4 border rounded">
        <h2 className="text-lg font-bold">Prediction Result</h2>
        <p className="text-gray-500">No prediction available. Please try again.</p>
      </div>
    );
  }

  // Extract interpretation and other_interpretations (default to empty object if not provided)
  const { interpretation, other_interpretations = {} } = prediction;

  return (
    <div className="mt-4 p-4 border rounded shadow">
      <h2 className="text-lg font-bold">Prediction Result</h2>

      {/* Display the main interpretation */}
      <p>
        <span className="font-semibold">Interpretation:</span>{" "}
        {interpretation || "N/A"}
      </p>

      {/* Check and display other antibiotic predictions */}
      {Object.keys(other_interpretations).length > 0 ? (
        <>
          <h3 className="text-md font-bold mt-2">Other Predictions:</h3>
          <ul className="list-disc list-inside">
            {Object.entries(other_interpretations).map(([antibiotic, result]) => (
              <li key={antibiotic} className="mt-1">
                <span className="font-semibold">{antibiotic}:</span>{" "}
                {result} {/* The result is already "Sensitive" or "Resistant" */}
              </li>
            ))}
          </ul>
        </>
      ) : (
        // Handle case when no other predictions are available
        <p className="text-gray-500 mt-2">No additional predictions available.</p>
      )}
    </div>
  );
};

export default PredictionResult;
