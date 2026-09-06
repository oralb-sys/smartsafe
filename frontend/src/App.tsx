import './App.css'

function App() {
  return (
    <main>
      <header>
        <h1>SmartSafe</h1>
        <p>Plataforma académica de seguridad y gestión urbana</p>
      </header>

      <section>
        <h2>Bienvenido a SmartSafe</h2>
        <p>
          Una plataforma integrada para reportar incidencias urbanas
          y gestionar alertas de emergencia.
        </p>
      </section>

      <section aria-labelledby="modules-title">
        <h2 id="modules-title">Módulos de la plataforma</h2>

        <article>
          <h3>SmartReport</h3>
          <p>
            Registra y consulta incidencias urbanas no urgentes,
            como baches, residuos, alumbrado y fugas de agua.
          </p>
        </article>

        <article>
          <h3>SmartSOS</h3>
          <p>
            Prototipo académico para registrar y dar seguimiento
            a alertas de emergencia.
          </p>
          <p>
            SmartSOS es un prototipo académico y no reemplaza
            los servicios oficiales de emergencia.
          </p>
        </article>
      </section>

      <footer>
        <p>SmartSafe · Proyecto académico</p>
      </footer>
    </main>
  )
}

export default App