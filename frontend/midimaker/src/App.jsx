import React from "react";
import Navbar from "./components/Navbar/Navbar";
import MidiForm from "./components/MidiForm/MidiForm";

function App() {
  return (
    <div className="app">
      <Navbar />
      <main>
        <MidiForm />
      </main>
    </div>
  );
}

export default App;
