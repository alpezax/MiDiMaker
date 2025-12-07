// src/services/api.js
export const generateMidi = async (data) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Error al generar MIDI");

    // Obtener blob del archivo MIDI
    const blob = await response.blob();

    // Generar nombre aleatorio basado en timestamp y progresión
    const timestamp = Date.now();
    const progressionName = data.progression.join("-");
    const fileName = `midi_${progressionName}_${timestamp}.mid`;

    // Descargar el archivo
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();

    // Retornar nombre del archivo generado
    return fileName;

  } catch (error) {
    console.error(error);
    alert("Hubo un error al generar el archivo MIDI.");
    return null;
  }
};
