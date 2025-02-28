// import { useEffect, useState } from "react";
// import Papa from "papaparse";
// import AntibioticsCheckbox from "./AntibioticsCheckbox";

// const AntibioticsSelector = ({ selectedBacteria }) => {
//   const [antibioticsList, setAntibioticsList] = useState([]);
//   const [selectedAntibiotics, setSelectedAntibiotics] = useState([]);

//   useEffect(() => {
//     // Load CSV data
//     fetch("/path_to/FINALDATA.csv")
//       .then((response) => response.text())
//       .then((csvText) => {
//         Papa.parse(csvText, {
//           header: true,
//           skipEmptyLines: true,
//           complete: (result) => {
//             const data = result.data;

//             // Filter antibiotics based on selected bacteria
//             const filteredAntibiotics = data
//               .filter((row) => row.Bacteria === selectedBacteria) // Match bacteria
//               .map((row) => row.Antibiotic) // Get antibiotic names
//               .filter((value, index, self) => self.indexOf(value) === index); // Remove duplicates

//             setAntibioticsList(filteredAntibiotics);
//           },
//         });
//       });
//   }, [selectedBacteria]); // Runs when selected bacteria changes

//   return (
//     <AntibioticsCheckbox
//       antibioticsList={antibioticsList}
//       selectedAntibiotics={selectedAntibiotics}
//       setSelectedAntibiotics={setSelectedAntibiotics}
//     />
//   );
// };

// export default AntibioticsSelector;


import Papa from "papaparse";
import { useEffect, useState } from "react";

const AntibioticsSelector = ({ selectedBacteria }) => {
  const [antibiotics, setAntibiotics] = useState([]);

  useEffect(() => {
    const fetchCSV = async () => {
      const response = await fetch("/data/FINALDATA.csv"); // Adjust if needed
      const reader = response.body.getReader();
      const result = await reader.read();
      const text = new TextDecoder("utf-8").decode(result.value);
      
      Papa.parse(text, {
        header: true, // If CSV has headers
        complete: (result) => {
          const filteredAntibiotics = result.data
            .filter((row) => row.Bacteria === selectedBacteria) // Match bacteria
            .map((row) => row.Antibiotic) // Extract antibiotic names
            .filter((value, index, self) => self.indexOf(value) === index); // Remove duplicates

          setAntibiotics(filteredAntibiotics);
        },
      });
    };

    fetchCSV();
  }, [selectedBacteria]);

  return (
    <div>
      <h3>Select Antibiotic:</h3>
      {antibiotics.map((antibiotic) => (
        <div key={antibiotic}>
          <input type="checkbox" value={antibiotic} />
          <label>{antibiotic}</label>
        </div>
      ))}
    </div>
  );
};

export default AntibioticsSelector;
