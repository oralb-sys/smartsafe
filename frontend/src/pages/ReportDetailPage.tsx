import { useEffect, useState } from 'react'
import {
  useNavigate,
  useParams,
} from 'react-router-dom'

import { getReportDetail } from '../services/api'
import type { ReportDetail } from '../types/report'

const API_BASE_URL =
  'http://localhost:8000'

const categoryLabels: Record<string, string> = {
  POTHOLE: 'Bache',
  WASTE: 'Residuos',
  STREET_LIGHT: 'Alumbrado público',
  WATER_LEAK: 'Fuga de agua',
}

const statusLabels: Record<string, string> = {
  REPORTED: 'Reportado',
  IN_PROGRESS: 'En atención',
  RESOLVED: 'Resuelto',
}

function ReportDetailPage() {
  const navigate = useNavigate()
  const { id } = useParams()

  const [report, setReport] =
    useState<ReportDetail | null>(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  useEffect(() => {
    async function loadReport() {
      if (!id) {
        setError(
          'No se encontró el identificador del reporte.',
        )
        setLoading(false)
        return
      }

      const token =
        localStorage.getItem(
          'smartsafe_token',
        )

      if (!token) {
        navigate('/login')
        return
      }

      try {
        const data =
          await getReportDetail(
            id,
            token,
          )

        setReport(data)
      } catch {
        setError(
          'No se pudo cargar el reporte.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadReport()
  }, [id, navigate])

  if (loading) {
    return (
      <main className="report-detail-page">
        <p>
          Cargando reporte...
        </p>
      </main>
    )
  }

  if (error || !report) {
    return (
      <main className="report-detail-page">
        <section className="report-detail-card">
          <p className="form-error">
            {error ||
              'Reporte no encontrado.'}
          </p>

          <button
            type="button"
            onClick={() =>
              navigate('/reports')
            }
          >
            Volver
          </button>
        </section>
      </main>
    )
  }

  return (
    <main className="report-detail-page">
      <section className="report-detail-card">
        <div className="report-detail-header">
          <div>
            <h1>
              {categoryLabels[
                report.category
              ] ?? report.category}
            </h1>

            <p>
              Detalle de incidencia
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              navigate('/reports')
            }
          >
            Volver
          </button>
        </div>

        <div className="report-detail-status">
          <span
            className={`status-badge status-${report.status.toLowerCase()}`}
          >
            {statusLabels[
              report.status
            ] ?? report.status}
          </span>
        </div>

        {report.photo_url && (
          <img
            className="report-detail-photo"
            src={`${API_BASE_URL}${report.photo_url}`}
            alt="Fotografía de la incidencia"
          />
        )}

        <div className="report-detail-content">
          <div>
            <strong>
              Descripción
            </strong>

            <p>
              {report.description ||
                'Sin descripción'}
            </p>
          </div>

          <div>
            <strong>
              Fecha de registro
            </strong>

            <p>
              {new Date(
                report.created_at,
              ).toLocaleString()}
            </p>
          </div>

          <div>
            <strong>
              Ubicación
            </strong>

            <p>
              Latitud:
              {' '}
              {report.latitude}
            </p>

            <p>
              Longitud:
              {' '}
              {report.longitude}
            </p>
          </div>

          <div>
            <strong>
              Identificador
            </strong>

            <p className="report-id">
              {report.id}
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}

export default ReportDetailPage