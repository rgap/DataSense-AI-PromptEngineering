export async function sendFile(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch("/api/analizar", {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Error al analizar el archivo");
  return res.json();
}
