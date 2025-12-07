// src/services/api.js
export const generateMidi = async (data) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error("Error al generar MIDI");

    // Descarga el archivo MIDI
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "composition.mid";
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch (error) {
    console.error(error);
    alert("Hubo un error al generar el archivo MIDI.");
  }
};
