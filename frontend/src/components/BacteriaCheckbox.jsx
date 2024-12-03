import React from "react";

const BacteriaCheckbox = ({ bacteriaList, selectedBacteria, setSelectedBacteria }) => {
  const handleChange = (bacteria) => {
    setSelectedBacteria((prev) =>
      prev.includes(bacteria) ? prev.filter((b) => b !== bacteria) : [...prev, bacteria]
    );
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="font-bold text-lg mb-4">Name Of the Bacteria</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {bacteriaList
          .slice() // Create a shallow copy of the list
          .sort((a, b) => a.localeCompare(b)) // Sort the list alphabetically
          .map((bacteria) => (
            <div key={bacteria} className="flex items-center space-x-2">
              <input
                type="checkbox"
                value={bacteria}
                checked={selectedBacteria.includes(bacteria)}
                onChange={() => handleChange(bacteria)}
              />
              <label>{bacteria}</label>
            </div>
          ))}
      </div>
    </div>
  );
};

export default BacteriaCheckbox;
