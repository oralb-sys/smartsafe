import {
  Navigate,
  Route,
  Routes,
} from 'react-router-dom'

import './App.css'

import DashboardPage from './pages/DashboardPage'
import EmergenciesPage from './pages/EmergenciesPage'
import EmergencyDetailPage from './pages/EmergencyDetailPage'
import EventsMapPage from './pages/EventsMapPage'
import LoginPage from './pages/LoginPage'
import MyReportsPage from './pages/MyReportsPage'
import ReportCreatePage from './pages/ReportCreatePage'
import ReportDetailPage from './pages/ReportDetailPage'
import SosPage from './pages/SosPage'


function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <Navigate
            to="/login"
            replace
          />
        }
      />

      <Route
        path="/login"
        element={
          <LoginPage />
        }
      />

      <Route
        path="/dashboard"
        element={
          <DashboardPage />
        }
      />

      <Route
        path="/reports/new"
        element={
          <ReportCreatePage />
        }
      />

      <Route
        path="/reports"
        element={
          <MyReportsPage />
        }
      />

      <Route
        path="/reports/:id"
        element={
          <ReportDetailPage />
        }
      />

      <Route
        path="/sos"
        element={
          <SosPage />
        }
      />

      <Route
        path="/emergencies"
        element={
          <EmergenciesPage />
        }
      />

      <Route
        path="/emergencies/:id"
        element={
          <EmergencyDetailPage />
        }
      />

      <Route
        path="/events/map"
        element={
          <EventsMapPage />
        }
      />
    </Routes>
  )
}

export default App