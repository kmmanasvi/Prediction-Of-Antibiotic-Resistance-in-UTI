import React from "react";

const AntibioticsCheckbox = ({ antibioticsList, selectedAntibiotics, setSelectedAntibiotics }) => {
  const handleChange = (antibiotic) => {
    setSelectedAntibiotics((prev) =>
      prev.includes(antibiotic) ? prev.filter((a) => a !== antibiotic) : [...prev, antibiotic]
    );
  };

  return (
    <div className="p-4 border rounded shadow">
      {/* <h2 className="font-bold text-lg mb-6">Antibiotic Prescribed</h2> */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {antibioticsList
          .slice() // Create a shallow copy of the list
          .sort((a, b) => a.localeCompare(b)) // Sort the list alphabetically
          .map((antibiotic) => (
            <div key={antibiotic} className="flex items-center space-x-2">
              <input
                type="checkbox"
                value={antibiotic}
                checked={selectedAntibiotics.includes(antibiotic)}
                onChange={() => handleChange(antibiotic)}
              />
              <label>{antibiotic}</label>
            </div>
          ))}
      </div>
    </div>
  );
};

export default AntibioticsCheckbox;


