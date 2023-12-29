import { Routes, Route } from "react-router-dom";
import HomePage from "../pages/HomePage/HomePage";
import DevicesPage from "../pages/DevicesPage/DevicesPage";



export default function MyRoutes() {
  return (
    <Routes>
      <Route path="" element={<HomePage />} />
      <Route path="devices" element={<DevicesPage />} />

    </Routes>
  );
}
