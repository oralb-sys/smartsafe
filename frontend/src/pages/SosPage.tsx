import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import {
  createEmergency,
} from '../services/api'

import type {
  EmergencyType,
} from '../services/api'

const emergencyTypes: {
  value: EmergencyType
  label: string
  icon: string
  description: string
}[] = [
  {
    value: 'MEDICAL',
    label: 'Emergencia médica',
    icon: '🩺',
    description:
      'Problema de salud que requiere atención inmediata.',
  },
  {
    value: 'ACCIDENT',
    label: 'Accidente',
    icon: '🚨',
    description:
      'Accidente vehicular, doméstico o en vía pública.',
  },
  {
    value: 'FIRE',
    label: 'Incendio',
    icon: '🔥',
    description:
      'Incendio, presencia de humo o riesgo relacionado.',
  },
  {
    value: 'PERSONAL_SECURITY',
    label: 'Seguridad personal',
    icon: '🛡️',
    description:
      'Situación que representa un riesgo para tu seguridad.',
  },
]

function SosPage() {
  const navigate = useNavigate()

  const [loading, setLoading] =
    useState(false)

  const [message, setMessage] =
    useState('')

  const [error, setError] =
    useState('')

  const [emergencyId, setEmergencyId] =
    useState('')

  const [
    selectedType,
    setSelectedType,
  ] = useState<EmergencyType | null>(
    null,
  )

  async function handleActivateSos() {
    setMessage('')
    setError('')
    setLoading(true)

    const token =
      localStorage.getItem(
        'smartsafe_token',
      )

    if (!token) {
      setLoading(false)
      navigate('/login')
      return
    }

    try {
      const emergency =
        await createEmergency(token)

      setEmergencyId(emergency.id)

      localStorage.setItem(
        'smartsafe_emergency_id',
        emergency.id,
      )

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

  function handleSelectType(
    type: EmergencyType,
  ) {
    setSelectedType(type)

    localStorage.setItem(
      'smartsafe_emergency_type',
      type,
    )
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
          {!emergencyId && (
            <>
              <div className="sos-warning">
                <h2>
                  ¿Necesitas ayuda?
                </h2>

                <p>
                  Presiona el botón SOS
                  para iniciar una alerta
                  de emergencia.
                </p>
              </div>

              <button
                type="button"
                className="sos-button"
                onClick={
                  handleActivateSos
                }
                disabled={loading}
              >
                {loading
                  ? 'Activando...'
                  : 'SOS'}
              </button>

              <p className="sos-help">
                Al activar el SOS se
                generará una alerta con
                estado inicial ACTIVE.
              </p>
            </>
          )}

          {message && (
            <div className="sos-success">
              <strong>
                Alerta registrada
              </strong>

              <p>{message}</p>

              <p>
                ID de emergencia:
                {' '}
                {emergencyId}
              </p>
            </div>
          )}

          {emergencyId && (
            <section className="emergency-type-section">
              <div className="emergency-type-header">
                <h2>
                  ¿Qué tipo de emergencia tienes?
                </h2>

                <p>
                  Selecciona la opción que
                  mejor describe la situación.
                </p>
              </div>

              <div className="emergency-type-grid">
                {emergencyTypes.map(
                  (type) => (
                    <button
                      key={type.value}
                      type="button"
                      className={
                        selectedType ===
                        type.value
                          ? 'emergency-type-card emergency-type-card-selected'
                          : 'emergency-type-card'
                      }
                      onClick={() =>
                        handleSelectType(
                          type.value,
                        )
                      }
                    >
                      <span className="emergency-type-icon">
                        {type.icon}
                      </span>

                      <strong>
                        {type.label}
                      </strong>

                      <span>
                        {
                          type.description
                        }
                      </span>
                    </button>
                  ),
                )}
              </div>

              {selectedType && (
                <div className="emergency-type-confirmation">
                  <strong>
                    Tipo de emergencia seleccionado:
                  </strong>

                  <p>
                    {
                      emergencyTypes.find(
                        (type) =>
                          type.value ===
                          selectedType,
                      )?.label
                    }
                  </p>
                </div>
              )}
            </section>
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