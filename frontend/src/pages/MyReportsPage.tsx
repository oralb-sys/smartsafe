import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { getMyReports } from '../services/api'
import type { ReportListItem } from '../types/report'

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

function MyReportsPage() {
  const navigate = useNavigate()

  const [reports, setReports] =
    useState<ReportListItem[]>([])

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  useEffect(() => {
    async function loadReports() {
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
          await getMyReports(token)

        setReports(data)
      } catch {
        setError(
          'No se pudieron cargar tus reportes.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadReports()
  }, [navigate])

  return (
    <main className="reports-page">
      <section className="reports-container">
        <div className="reports-header">
          <div>
            <h1>Mis reportes</h1>

            <p>
              Consulta las incidencias
              que has registrado.
            </p>
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              navigate('/dashboard')
            }
          >
            Volver
          </button>
        </div>

        {loading && (
          <p>Cargando reportes...</p>
        )}

        {error && (
          <p className="form-error">
            {error}
          </p>
        )}

        {!loading &&
          !error &&
          reports.length === 0 && (
            <div className="empty-state">
              <h2>
                Aún no tienes reportes
              </h2>

              <p>
                Cuando registres una
                incidencia aparecerá
                aquí.
              </p>

              <button
                type="button"
                onClick={() =>
                  navigate('/reports/new')
                }
              >
                Registrar incidencia
              </button>
            </div>
          )}

        <div className="reports-grid">
          {reports.map((report) => (
            <article
              key={report.id}
              className="report-item"
            >
              <div className="report-item-body">
                <div className="report-item-top">
                  <div>
                    <h2>
                      {categoryLabels[
                        report.category
                      ] ??
                        report.category}
                    </h2>

                    <p className="report-date">
                      {new Date(
                        report.created_at,
                      ).toLocaleString()}
                    </p>
                  </div>

                  <span
                    className={`status-badge status-${report.status.toLowerCase()}`}
                  >
                    {statusLabels[
                      report.status
                    ] ??
                      report.status}
                  </span>
                </div>

               <div className="report-item-actions">
                <button
                    type="button"
                    className="report-detail-button"
                    onClick={() =>
                    navigate(`/reports/${report.id}`)
                    }
                >
                    Ver detalle
                </button>
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}

export default MyReportsPage