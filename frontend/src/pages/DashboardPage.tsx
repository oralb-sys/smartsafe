import { useNavigate } from 'react-router-dom'

function DashboardPage() {
  const navigate = useNavigate()

  const role =
    localStorage.getItem(
      'smartsafe_role',
    )

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <h1>SmartSafe</h1>
          <p>Panel principal</p>
        </div>

        <span className="role-badge">
          {role}
        </span>
      </header>

      <section>
        <h2>¿Qué deseas hacer?</h2>

        <div className="module-grid">

          {role === 'CITIZEN' && (
            <>
              <article>
                <h3>
                  Registrar incidencia
                </h3>

                <p>
                  Reporta baches, residuos,
                  problemas de alumbrado
                  o fugas de agua.
                </p>

                <button
                  type="button"
                  onClick={() =>
                    navigate(
                      '/reports/new',
                    )
                  }
                >
                  Registrar incidencia
                </button>
              </article>


              <article>
                <h3>
                  Mis reportes
                </h3>

                <p>
                  Consulta las incidencias
                  que has registrado y
                  revisa su estado actual.
                </p>

                <button
                  type="button"
                  onClick={() =>
                    navigate(
                      '/reports',
                    )
                  }
                >
                  Ver mis reportes
                </button>
              </article>


              <article className="sos-dashboard-card">
                <h3>
                  SmartSOS
                </h3>

                <p>
                  Activa una alerta de
                  emergencia cuando
                  necesites ayuda inmediata.
                </p>

                <button
                  type="button"
                  className="sos-dashboard-button"
                  onClick={() =>
                    navigate(
                      '/sos',
                    )
                  }
                >
                  Activar SOS
                </button>
              </article>
            </>
          )}


          {role === 'OPERATOR' && (
            <article className="dashboard-card">
              <h3>
                Emergencias SmartSOS
              </h3>

              <p>
                Consulta las alertas de
                emergencia registradas
                por los ciudadanos.
              </p>

              <button
                type="button"
                onClick={() =>
                  navigate(
                    '/emergencies',
                  )
                }
              >
                Ver emergencias
              </button>
            </article>
          )}

        </div>
      </section>
    </main>
  )
}

export default DashboardPage