import React from "react";

const AntibioticsCheckbox = ({ antibioticsList, selectedAntibiotics, setSelectedAntibiotics }) => {
  const handleChange = (antibiotic) => {
    setSelectedAntibiotics((prev) =>
      prev.includes(antibiotic) ? prev.filter((a) => a !== antibiotic) : [...prev, antibiotic]
    );
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="font-bold text-lg">Antibiotics</h2>
      {antibioticsList.map((antibiotic) => (
        <div key={antibiotic}>
          <label>
            <input
              type="checkbox"
              value={antibiotic}
              checked={selectedAntibiotics.includes(antibiotic)}
              onChange={() => handleChange(antibiotic)}
            />
            {antibiotic}
          </label>
        </div>
      ))}
    </div>
  );
};

export default AntibioticsCheckbox;
