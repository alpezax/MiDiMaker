import React, { useState, useEffect } from "react";
import styles from "./PatternMidiForm.module.css";
import ReactMidiPlayer from "react-midi-player";
import { generateAndFetchMidiBlob, generate808MidiBlob } from "../../services/api";

const PatternMidiForm = () => {
  const [patterns, setPatterns] = useState([]);
  const [selectedPattern, setSelectedPattern] = useState(null);
  const [bpm, setBpm] = useState(120);
  const [midiUrl, setMidiUrl] = useState(null);
  const [midiFileName, setMidiFileName] = useState(null);

  // Cargar patrones desde el endpoint
  useEffect(() => {
    const fetchPatterns = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/v1/patterns/");
        const data = await res.json();
        setPatterns(data);
        if (data.length > 0) {
          setSelectedPattern(data[0]);
          setBpm(data[0].bpm);
        }
      } catch (err) {
        console.error("Error cargando patrones:", err);
      }
    };
    fetchPatterns();
  }, []);

  const handlePatternSelect = (pattern) => {
    setSelectedPattern(pattern);
    setBpm(pattern.bpm);
    setMidiUrl(null);
    setMidiFileName(null);
  };

  const handleGenerateMidi = async () => {
    if (!selectedPattern) return;

    const patternData = {
      bpm,
      pattern_length: selectedPattern.steps,
      ...selectedPattern.instruments,
      pattern_name: selectedPattern.name
    };

    const result = await generate808MidiBlob(patternData);
    if (result) {
      setMidiUrl(result.url);
      setMidiFileName(result.fileName);
    }
  };

  const handleDownload = () => {
    if (!midiUrl || !midiFileName) return;
    const a = document.createElement("a");
    a.href = midiUrl;
    a.download = midiFileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  return (
    <div>
      <h3>RythmPatterns</h3>

      <div className={styles.patternGrid}>
        {patterns.map((p) => (
          <div
            key={p.name}
            className={`${styles.patternCard} ${
              selectedPattern?.name === p.name ? styles.selected : ""
            }`}
            onClick={() => handlePatternSelect(p)}
          >
            <strong>{p.name}</strong>
            <p>{p.genre}</p>
            <p>{p.steps} pasos</p>
            <p>BPM: {p.bpm}</p>
          </div>
        ))}
      </div>

      {selectedPattern && (
        <div className={styles.controls}>
          <label>
            BPM:
            <input
              type="number"
              value={bpm}
              onChange={(e) => setBpm(Number(e.target.value))}
              min={40}
              max={250}
            />
          </label>

          <button onClick={handleGenerateMidi}>Generar MIDI</button>
          {midiUrl && (
            <button onClick={handleDownload}>Descargar MIDI</button>
          )}
        </div>
      )}

      {midiUrl && (
        <div className={styles.player}>
          <p>{midiFileName}</p>
          <ReactMidiPlayer src={midiUrl} autoPlay={false} loop={false} controls />
        </div>
      )}
    </div>
  );
};

export default PatternMidiForm;
