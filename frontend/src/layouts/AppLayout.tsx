import { Outlet } from "react-router-dom";
import { ToastContainer } from "react-toastify";

export default function AppLayout() {
  return (
    <>
      <div className=" font-display bg-gray-100">
        <header className="m-auto w-full bg-gradient-to-r from-[#094FC2] to-[#5A38AA] flex justify-between items-center text-white py-3 px-8">
          <a className="flex items-center gap-2" href="/">
            <img src="/img/logo.svg" className="w-8 h-8" alt="Logo DataSense" />
            <h1 className="text-4xl font-bold">DataSense - AI</h1>
          </a>
          <img
            src="/img/iconos/svg/QuestionIcon.svg"
            className="w-6 h-6 cursor-pointer"
            alt="Icono de preguntas"
          />
        </header>

        <main className="flex font-display flex-col min-h-screen bg-gray-100">
          <Outlet />
        </main>

        {/* Alertas Toast */}
        <ToastContainer
          pauseOnHover={false}
          autoClose={3000}
          pauseOnFocusLoss={false}
        />
      </div>
    </>
  );
}
