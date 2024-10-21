import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const Sentiments = () => {
  const [sentimentData, setSentimentData] = useState([]);
  const [selectedProject, setSelectedProject] = useState('');
  const [selectedProjectData, setSelectedProjectData] = useState(null);

  useEffect(() => {
    // Fetch data from the Flask backend
    axios.get('http://127.0.0.1:5000/api/sentiments')
      .then(response => {
        setSentimentData(response.data);
        setSelectedProject(response.data[0]?.Project); // Set the initial selected project
        setSelectedProjectData(response.data[0]); // Set initial project data
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const handleProjectChange = (event) => {
    const projectName = event.target.value;
    setSelectedProject(projectName);
    const projectData = sentimentData.find((project) => project.Project === projectName);
    setSelectedProjectData(projectData);
  };

  // Pie chart data for project sentiment distribution
  const projectSentimentData = selectedProjectData
    ? {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [
          {
            label: 'Sentiment Distribution',
            data: [
              sentimentData.filter(item => item.Project === selectedProject && item.Sentiment === 'Positive').length,
              sentimentData.filter(item => item.Project === selectedProject && item.Sentiment === 'Negative').length,
              sentimentData.filter(item => item.Project === selectedProject && item.Sentiment === 'Neutral').length,
            ],
            backgroundColor: ['rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(255, 206, 86)'],
            borderColor: ['rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(255, 206, 86)'],
            borderWidth: 1,
          },
        ],
      }
    : null;

  // WordCloud options to make it more organized and circular
  const options = {
    rotations: 2, // Limit rotations to keep it more uniform
    rotationAngles: [0, 0], // No rotation to keep it neat
    scale: 'sqrt', // Make word scaling more proportional
    fontSizes: [20, 60], // Control the size range for better visual balance
    deterministic: true, // Use deterministic layout for consistent rendering
  };

  return (
    <div className="p-10 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-center mb-10">Mathare CDF Projects - Mood of the Hood</h1>

      {/* Cards for Key Figures */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">Total Feedbacks</h3>
          <p className="text-4xl font-semibold">{sentimentData.length}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">Positive Sentiments</h3>
          <p className="text-4xl font-semibold">{sentimentData.filter(item => item.Sentiment === 'Positive').length}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">Negative Sentiments</h3>
          <p className="text-4xl font-semibold">{sentimentData.filter(item => item.Sentiment === 'Negative').length}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">Neutral Sentiments</h3>
          <p className="text-4xl font-semibold">{sentimentData.filter(item => item.Sentiment === 'Neutral').length}</p>
        </div>
      </div>

      {/* Project Selection Dropdown */}
      <div className="mb-10 text-center">
        <label htmlFor="project-select" className="text-xl font-semibold mr-4">Select a Project:</label>
        <select
          id="project-select"
          value={selectedProject}
          onChange={handleProjectChange}
          className="p-2 border rounded-lg"
        >
          {sentimentData.map((project, index) => (
            <option key={index} value={project.Project}>
              {project.Project}
            </option>
          ))}
        </select>
      </div>

      {/* Project Sentiment Chart */}
      {projectSentimentData && (
        <div className="mb-10">
          <h2 className="text-2xl font-semibold mb-4">Sentiment Distribution for {selectedProject}</h2>
          <div className="bg-white p-6 rounded-lg shadow-md flex justify-center items-center">
            <div style={{ width: '50%', height: '50%' }}>
              <Pie data={projectSentimentData} />
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default Sentiments;
