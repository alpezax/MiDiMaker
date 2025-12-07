// src/services/api.js

// Adaptamos generateMidi para que retorne { blob, fileName } sin descargar automáticamente
export const generateMidi = async (data) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Error al generar MIDI");

    const blob = await response.blob();

    const timestamp = Date.now();
    const progressionName = data.progression.join("-");
    const fileName = `midi_${progressionName}_${timestamp}.mid`;

    return { blob, fileName };
  } catch (error) {
    console.error(error);
    alert("Hubo un error al generar el archivo MIDI.");
    return null;
  }
};

// Nueva función: genera el MIDI y luego lo envía para obtener el blob del endpoint
export const generateAndFetchMidiBlob = async (data) => {
  try {
    // 1️⃣ Reutilizamos generateMidi
    const result = await generateMidi(data);
    if (!result) throw new Error("Error al generar MIDI");

    const { blob, fileName } = result;

    // 2️⃣ Enviar el blob al endpoint /api/v1/midi-blob
    const formData = new FormData();
    formData.append("file", new File([blob], fileName, { type: "audio/midi" }));

    const blobResponse = await fetch("http://127.0.0.1:8000/api/v1/midi-blob", {
      method: "POST",
      body: formData,
    });

    if (!blobResponse.ok) throw new Error("Error al obtener el blob MIDI");

    const returnedBlob = await blobResponse.blob();
    const url = window.URL.createObjectURL(returnedBlob);

    return { fileName, url };
  } catch (error) {
    console.error(error);
    alert("Hubo un error al generar o recuperar el archivo MIDI.");
    return null;
  }
};
