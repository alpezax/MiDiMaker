import React from "react";
import Navbar from "./components/Navbar/Navbar";
import MidiForm from "./components/MidiForm/MidiForm";
import PatternMidiForm from "./components/PatternMidiForm/PatternMidiForm";

function App() {
  return (
    <div className="app">
      <Navbar />
      <main>
        <MidiForm />
        <br /><br />
        <PatternMidiForm />
      </main>
    </div>
  );
}

export default App;
