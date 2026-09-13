import { Navigate, Route, Routes } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import ReportCreatePage from './pages/ReportCreatePage'
import './App.css'
import MyReportsPage from './pages/MyReportsPage'
import ReportDetailPage from './pages/ReportDetailPage'

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
  path="/reports/:id"
  element={<ReportDetailPage />}
/>
    </Routes>
  )
}

export default App