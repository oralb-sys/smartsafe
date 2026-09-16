import { Navigate, Route, Routes } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ReportCreatePage from './pages/ReportCreatePage'
import './App.css'
import MyReportsPage from './pages/MyReportsPage'
import ReportDetailPage from './pages/ReportDetailPage'
import SosPage from './pages/SosPage'
import EmergenciesPage from './pages/EmergenciesPage'
import EmergencyDetailPage from './pages/EmergencyDetailPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/reports/new" element={<ReportCreatePage />} />
      <Route
  path="/reports"
  element={<MyReportsPage />}
/>
      <Route
  path="/sos"
  element={<SosPage />}
/>

<Route
  path="/reports/:id"
  element={<ReportDetailPage />}
/>
 <Route
  path="/emergencies"
  element={<EmergenciesPage />}
/>

<Route
  path="/emergencies/:id"
  element={<EmergencyDetailPage />}
/>
    </Routes>
  )
}

export default App