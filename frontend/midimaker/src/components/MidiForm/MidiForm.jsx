import React, { useState } from "react";
import styles from "./MidiForm.module.css";
import { generateMidi } from "../../services/api";

const keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
const scales = ["major", "minor"];
const progressions = ["I-vi-IV-V", "ii-V-I", "I-IV-V", "I-V-vi-IV"];
const chordTypes = ["7", "maj7", "m7", "9", "m9", "13"];
const octaves = [2, 3, 4, 5, 6];

const MidiForm = () => {
  const [form, setForm] = useState({
    key: "C",
    scale: "major",
    progression: progressions[0],
    chord_types: ["7", "m7", "7", "7"],
    tempo: 90,
    duration: 2.0,
    octave: 4,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
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
    //Generamos el fichero MiDi
    generateMidi(data);
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles["label-container"]}>
        <label>Key</label>
        <select name="key" value={form.key} onChange={handleChange}>
          {keys.map((k) => (
            <option key={k} value={k}>{k}</option>
          ))}
        </select>
      </div>

      <div className={styles["label-container"]}>
        <label>Scale</label>
        <select name="scale" value={form.scale} onChange={handleChange}>
          {scales.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      <div className={styles["label-container"]}>
        <label>Progression</label>
        <select name="progression" value={form.progression} onChange={handleChange}>
          {progressions.map((p) => (
            <option key={p} value={p}>{p}</option>
          ))}
        </select>
      </div>

      <div className={styles["label-container"]}>
        <label>Chord Types (4 acordes)</label>
        <input
          type="text"
          name="chord_types"
          value={form.chord_types.join(",")}
          onChange={(e) =>
            setForm({ ...form, chord_types: e.target.value.split(",") })
          }
        />
      </div>

      <div className={styles["label-container"]}>
        <label>Tempo</label>
        <input type="number" name="tempo" value={form.tempo} onChange={handleChange} />
      </div>

      <div className={styles["label-container"]}>
        <label>Duration (s)</label>
        <input
          type="number"
          step="0.1"
          name="duration"
          value={form.duration}
          onChange={handleChange}
        />
      </div>

      <div className={styles["label-container"]}>
        <label>Octave</label>
        <select name="octave" value={form.octave} onChange={handleChange}>
          {octaves.map((o) => (
            <option key={o} value={o}>{o}</option>
          ))}
        </select>
      </div>

      <button type="submit">Generar MIDI</button>
    </form>
  );
};

export default MidiForm;
