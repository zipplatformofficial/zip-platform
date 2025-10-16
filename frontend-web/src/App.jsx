import { useState } from "react";
import "./index.css"; // ✅ Make sure you import Tailwind’s index.css here

function App() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 text-center p-6">
      <h1 className="text-4xl font-bold text-blue-600 mb-2">
        Tailwind CSS is Working! 🚀
      </h1>
      <p className="text-blue-700 max-w-md">
        If you can see this styled text with colors and spacing, your Tailwind
        setup is configured correctly.
      </p>

      <button className="mt-6 px-6 py-3 bg-yellow-400 hover:bg-yellow-500 text-black font-semibold rounded-lg shadow-md transition-all">
        Test Button
      </button>
    </div>
  );
}

export default App;
