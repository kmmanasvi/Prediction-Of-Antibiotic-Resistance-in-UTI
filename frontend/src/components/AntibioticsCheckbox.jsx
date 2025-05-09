import React, { useEffect, useState } from "react";
import axios from "axios";

const AntibioticsCheckbox = ({ selectedBacteria, exposureLevel, selectedAntibiotics, setSelectedAntibiotics }) => {
  const [antibioticsList, setAntibioticsList] = useState([]);

  // Fetch antibiotics when bacteria or exposure level changes
  useEffect(() => {
    if (selectedBacteria && exposureLevel) {
      const fetchAntibiotics = async () => {
        try {
          const response = await axios.get(
            `http://localhost:5000/get_antibiotics?bacteria=${selectedBacteria}&exposure_level=${exposureLevel}`
          );
          setAntibioticsList(response.data.antibiotics);
          setSelectedAntibiotics([]); // Reset selected antibiotics when list updates
        } catch (error) {
          console.error("Error fetching antibiotics:", error);
        }
      };

      fetchAntibiotics();
    }
  }, [selectedBacteria, exposureLevel, setSelectedAntibiotics]);

  const handleChange = (antibiotic) => {
    setSelectedAntibiotics((prev) =>
      prev.includes(antibiotic) ? prev.filter((a) => a !== antibiotic) : [...prev, antibiotic]
    );
  };

  return (
    <div className="p-4 border rounded shadow">
      
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {antibioticsList.length === 0 ? (
          <p className="col-span-full text-gray-500">No antibiotics available.</p>
        ) : (
          antibioticsList
            .slice()
            .sort((a, b) => a.localeCompare(b))
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
            ))
        )}
      </div>
    </div>
  );
};

export default AntibioticsCheckbox;
