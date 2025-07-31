import { sendFile } from "@/api/iaApi";
import Characteristics from "@/components/Characteristics";
import Title from "@/components/Title";
import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useDropzone } from "react-dropzone";

export default function DashboardView() {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);

  const mutation = useMutation({
    mutationFn: sendFile,
    onError: () => {
      toast.error("Error al enviar el archivo. Por favor, inténtalo de nuevo.");
    },
    onSuccess: (data) => {
      navigate("/resultados", { state: { metrics: data } });
    },
  });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (file) {
      navigate("/analizando");
      mutation.mutate(file);
    }
  };

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles && acceptedFiles[0]) {
      setFile(acceptedFiles[0]);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "text/csv": [".csv"] },
    maxFiles: 1,
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  return (
    <div className="flex flex-col items-center px-4 py-10 max-w-5xl mx-auto">
      {/* Título principal */}
      <Title />

      {/* Área de drag & drop */}
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8 mb-10"
      >
        <div
          {...getRootProps()}
          className={`border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center py-10 px-4 cursor-pointer transition ${
            isDragActive ? "bg-blue-50 border-blue-400" : ""
          }`}
        >
          <input {...getInputProps()} />
          <img
            src="/img/iconos/png/fileUpIcon.png"
            alt="Subir archivo"
            className="w-16 h-16 mb-4"
          />
          <p className="font-semibold text-lg mb-1">
            Arrastra tu archivo CSV aquí
          </p>
          <p className="text-gray-500 mb-2">
            o haz clic para seleccionar un archivo
          </p>
          {file && <p className="text-sm text-gray-700 mb-2">{file.name}</p>}
          <div className="flex items-center justify-center gap-2">
            <img
              src="/img/iconos/svg/csvFile.svg"
              alt="Archivo CSV"
              className="w-5 h-5 mb-4"
            />
            <p className="text-xs text-gray-400">
              Soporta archivos .csv hasta 50MB
            </p>
          </div>
        </div>
        <motion.button
          className="mt-6 w-full py-3 rounded-lg bg-gradient-to-r from-[#094FC2] to-[#5A38AA] text-white font-bold text-lg shadow transition hover:opacity-90 cursor-pointer"
          whileTap={{ scale: 1.1 }}
          transition={{ type: "spring", stiffness: 300, damping: 5 }}
          type="submit"
        >
          <span className="inline-flex items-center gap-2">
            <img
              src="/img/iconos/svg/upIcon.svg"
              alt="Icono de subida"
              className="w-5 h-5"
            />
            Comenzar análisis
          </span>
        </motion.button>
      </form>

      {/* Tarjetas de características */}
      <Characteristics />
    </div>
  );
}
