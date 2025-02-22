import React, { useState, useEffect } from "react";

export default function LearningApp() {
  const [file, setFile] = useState(null);
  const [modules, setModules] = useState([]);
  const [mcqs, setMcqs] = useState([]);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    fetch("http://127.0.0.1:5000/modules")
      .then((res) => res.json())
      .then((data) => setModules(data));

    fetch("http://127.0.0.1:5000/mcqs")
      .then((res) => res.json())
      .then((data) => setMcqs(data));
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });
    alert("File uploaded successfully");
  };

  const handleAnswerChange = (question, answer) => {
    setAnswers({ ...answers, [question]: answer });
  };

  return (
    <div className="p-6 max-w-4xl mx-auto bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">Learning System</h1>
      
      {/* Document Upload */}
      <div className="mb-8 p-6 bg-white shadow-lg rounded-lg border border-gray-200">
        <h2 className="text-xl font-semibold mb-3">Upload Document</h2>
        <div className="flex items-center space-x-4">
          <input 
            type="file" 
            onChange={handleFileChange} 
            className="border p-2 rounded w-full cursor-pointer focus:ring focus:ring-blue-300" 
          />
          <button 
            onClick={handleUpload} 
            className="bg-blue-600 text-white px-5 py-2 rounded hover:bg-blue-700 transition-all"
          >
            Upload
          </button>
        </div>
      </div>
      
      {/* Learning Modules */}
      <div className="mb-8 p-6 bg-white shadow-lg rounded-lg border border-gray-200">
        <h2 className="text-xl font-semibold mb-4">Learning Modules</h2>
        {modules.map((module, index) => (
          <div key={index} className="p-4 border-l-4 border-blue-500 bg-gray-100 rounded-lg mb-3">
            <h3 className="font-bold text-lg text-blue-700">{module.title}</h3>
            <p className="text-gray-700 mt-2">{module.content}</p>
          </div>
        ))}
      </div>

      {/* MCQs */}
      <div className="p-6 bg-white shadow-lg rounded-lg border border-gray-200">
        <h2 className="text-xl font-semibold mb-4">MCQs</h2>
        {mcqs.map((mcq, index) => (
          <div key={index} className="p-4 border-l-4 border-green-500 bg-gray-100 rounded-lg mb-3">
            <h3 className="font-bold text-lg text-green-700">{mcq.question}</h3>
            <div className="mt-2 space-y-2">
              {mcq.options.map((option, i) => (
                <div key={i} className="flex items-center space-x-2">
                  <input
                    type="radio"
                    name={mcq.question}
                    value={option}
                    onChange={() => handleAnswerChange(mcq.question, option)}
                    className="form-radio text-green-600 focus:ring focus:ring-green-300"
                  />
                  <label className="text-gray-700">{option}</label>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  ); 
}
