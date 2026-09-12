import { useNavigate } from 'react-router-dom'

function DashboardPage() {
  const navigate = useNavigate()
  const role = localStorage.getItem('smartsafe_role')

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <div>
          <h1>SmartSafe</h1>
          <p>Panel principal</p>
        </div>

        <span className="role-badge">{role}</span>
      </header>

      <section>
        <h2>¿Qué deseas hacer?</h2>

        <div className="module-grid">
          <article>
            <h3>Registrar incidencia</h3>
            <p>
              Reporta baches, residuos, problemas de alumbrado
              o fugas de agua.
            </p>

            <button onClick={() => navigate('/reports/new')}>
              Registrar incidencia
            </button>
          </article>

          <article>
            <h3>SmartSOS</h3>
            <p>
              Módulo académico para alertas de emergencia.
            </p>

            <button disabled>Próximamente</button>
          </article>
        </div>
      </section>
    </main>
  )
}

export default DashboardPage