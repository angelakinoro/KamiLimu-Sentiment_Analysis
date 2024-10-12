import React , { useState }from 'react'
import { Line, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import 'tailwindcss/tailwind.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ArcElement);

// Sample dummy data
const dummySentimentData = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June'],
  datasets: [
    {
      label: 'Positive',
      data: [65, 59, 80, 81, 56, 55],
      borderColor: 'rgb(75, 192, 192)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
    },
    {
      label: 'Negative',
      data: [28, 48, 40, 19, 86, 27],
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
    },
  ],
};

const dummyProjectSentiments = [
  { project: 'School Renovation', sentiment: 'Positive', feedbackVolume: 120 },
  { project: 'Road Construction', sentiment: 'Negative', feedbackVolume: 60 },
  { project: 'Water Supply', sentiment: 'Neutral', feedbackVolume: 90 },
];

const Sentiments = () => {
  const [selectedProject, setSelectedProject] = useState(dummyProjectSentiments[0].project);

  const handleProjectChange = (event) => {
    setSelectedProject(event.target.value);
  };

  const selectedProjectData = dummyProjectSentiments.find(
    (project) => project.project === selectedProject
  );

  return (
    <div className="p-10 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-center mb-10">Mathare CDF Projects Dashboard</h1>
      
      
      {/* Sentiment Overview */}
      <div className="mb-10">
        <h2 className="text-2xl font-semibold mb-4">Sentiment Overview</h2>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Line data={dummySentimentData} />
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
          {dummyProjectSentiments.map((project, index) => (
            <option key={index} value={project.project}>
              {project.project}
            </option>
          ))}
        </select>
      </div>

      
      {/* Selected Project Sentiment Details */}
      <div className="mb-10">
        <h2 className="text-2xl font-semibold mb-4">Selected Project Details</h2>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">{selectedProjectData.project}</h3>
          <p>Sentiment: {selectedProjectData.sentiment}</p>
          <p>Feedback Volume: {selectedProjectData.feedbackVolume}</p>
        </div>
      </div>

      {/* Feedback Volume */}
      <div className="mb-10">
        <h2 className="text-2xl font-semibold mb-4">Feedback Volume</h2>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <Pie
            data={{
              labels: ['School Renovation', 'Road Construction', 'Water Supply'],
              datasets: [
                {
                  data: [120, 60, 90],
                  backgroundColor: ['rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(255, 206, 86)'],
                },
              ],
            }}
          />
        </div>
      </div>

      {/* Cards to Display Single Numbers */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">Total Projects</h3>
          <p className="text-4xl font-semibold">15</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">Negative Sentiments</h3>
          <p className="text-4xl font-semibold">65%</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-bold">Total Feedback</h3>
          <p className="text-4xl font-semibold">270</p>
        </div>
      </div>

      {/* Update Alerts */}
      <div className="mb-10">
        <h2 className="text-2xl font-semibold mb-4">Update Alerts</h2>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <p>New updates: Road Construction project has been resumed.</p>
        </div>
      </div>
    </div>
  );
};

export default Sentiments;
