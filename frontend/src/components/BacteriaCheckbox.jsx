import React from "react";

const BacteriaCheckbox = ({ bacteriaList, selectedBacteria, setSelectedBacteria }) => {
  const handleChange = (bacteria) => {
    setSelectedBacteria((prev) =>
      prev.includes(bacteria) ? prev.filter((b) => b !== bacteria) : [...prev, bacteria]
    );
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="font-bold text-lg">Bacteria</h2>
      {bacteriaList.map((bacteria) => (
        <div key={bacteria}>
          <label>
            <input
              type="checkbox"
              value={bacteria}
              checked={selectedBacteria.includes(bacteria)}
              onChange={() => handleChange(bacteria)}
            />
            {bacteria}
          </label>
        </div>
      ))}
    </div>
  );
};

export default BacteriaCheckbox;
