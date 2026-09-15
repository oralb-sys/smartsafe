import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { createEmergency } from '../services/api'

function SosPage() {
  const navigate = useNavigate()

  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [emergencyId, setEmergencyId] = useState('')

  async function handleActivateSos() {
    setMessage('')
    setError('')
    setLoading(true)

    const token =
      localStorage.getItem('smartsafe_token')

    if (!token) {
      setLoading(false)
      navigate('/login')
      return
    }

    try {
      const emergency =
        await createEmergency(token)

      setEmergencyId(emergency.id)

      setMessage(
        `Alerta SOS activada correctamente. Estado: ${emergency.status}`,
      )
    } catch {
      setError(
        'No se pudo activar la alerta SOS.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="sos-page">
      <section className="sos-card">
        <div className="sos-header">
          <div>
            <h1>SmartSOS</h1>
            <p>
              Activación de alerta de emergencia
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

        <div className="sos-content">
          <div className="sos-warning">
            <h2>¿Necesitas ayuda?</h2>

            <p>
              Presiona el botón SOS para
              iniciar una alerta de emergencia.
            </p>
          </div>

          <button
            type="button"
            className="sos-button"
            onClick={handleActivateSos}
            disabled={loading}
          >
            {loading
              ? 'Activando SOS...'
              : 'SOS'}
          </button>

          <p className="sos-help">
            Al activar el SOS se generará una
            alerta con estado inicial ACTIVE.
          </p>

          {message && (
            <div className="sos-success">
              <strong>
                Alerta registrada
              </strong>

              <p>{message}</p>

              {emergencyId && (
                <p>
                  ID de emergencia:
                  {' '}
                  {emergencyId}
                </p>
              )}
            </div>
          )}

          {error && (
            <p className="form-error">
              {error}
            </p>
          )}
        </div>
      </section>
    </main>
  )
}

export default SosPage