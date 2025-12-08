import React, { useState } from "react";
import styles from "./MidiForm.module.css";
import { generateAndFetchMidiBlob } from "../../services/api";
import ReactMidiPlayer from "react-midi-player";

const keys = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
const scales = ["major","minor"];
const progressions = ["I-vi-IV-V","ii-V-I","I-IV-V","I-V-vi-IV"];
const octaves = [2,3,4,5,6];

const MidiForm = () => {
  const [form, setForm] = useState({
    key: "C",
    scale: "major",
    progression: progressions[0],
    chord_types: ["7","m7","7","7"],
    tempo: 90,
    duration: 2.0,
    octave: 4,
  });

  const [midiUrl, setMidiUrl] = useState(null);
  const [midiFileName, setMidiFileName] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = {
      key: form.key,
      scale: form.scale,
      progression: form.progression.split("-"),
      chord_types: form.chord_types,
      tempo: Number(form.tempo),
      duration: Number(form.duration),
      octave: Number(form.octave),
    };

    const result = await generateAndFetchMidiBlob(data);
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
      <h3>Chord Progressions</h3>
      <form className={styles.form} onSubmit={handleSubmit}>
        {["key","scale","progression","chord_types","tempo","duration","octave"].map((field) => (
          <div key={field} className={styles["label-container"]}>
            <label>{field.charAt(0).toUpperCase() + field.slice(1)}</label>
            {field === "chord_types" ? (
              <input
                type="text"
                name="chord_types"
                value={form.chord_types.join(",")}
                onChange={(e) => setForm({...form, chord_types: e.target.value.split(",")})}
              />
            ) : field === "key" ? (
              <select name="key" value={form.key} onChange={handleChange}>
                {keys.map(k => <option key={k} value={k}>{k}</option>)}
              </select>
            ) : field === "scale" ? (
              <select name="scale" value={form.scale} onChange={handleChange}>
                {scales.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            ) : field === "progression" ? (
              <select name="progression" value={form.progression} onChange={handleChange}>
                {progressions.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            ) : field === "octave" ? (
              <select name="octave" value={form.octave} onChange={handleChange}>
                {octaves.map(o => <option key={o} value={o}>{o}</option>)}
              </select>
            ) : (
              <input
                type={field==="tempo"||field==="duration"?"number":"text"}
                step={field==="duration"?0.1:undefined}
                name={field}
                value={form[field]}
                onChange={handleChange}
              />
            )}
          </div>
        ))}

        <div style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}>
          <button type="submit">Generar MIDI</button>
          {midiUrl && (
            <button type="button" onClick={handleDownload}>
              Descargar MIDI
            </button>
          )}
        </div>
      </form>

      {midiUrl && (
        <div style={{ marginTop: "1rem" }}>
          <p>{midiFileName}</p>
          <ReactMidiPlayer
            src={midiUrl}
            autoPlay={false}
            loop={false}
            controls={true}
          />
        </div>
      )}
    </div>

  );
};

export default MidiForm;
