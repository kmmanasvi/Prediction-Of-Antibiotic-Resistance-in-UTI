import React from "react";

const MICInput = ({ micValue, setMicValue }) => {
  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="font-bold text-lg">MIC Value</h2>
      <input
        type="text"
        placeholder="Enter MIC value (e.g., >=4)"
        className="border p-2 w-full"
        value={micValue}
        onChange={(e) => setMicValue(e.target.value)}
      />
    </div>
  );
};

export default MICInput;
