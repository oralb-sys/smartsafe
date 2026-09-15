import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import LocationPicker from '../components/LocationPicker'

import {
  createEmergency,
  updateEmergencyLocation,
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

  const [latitude, setLatitude] =
    useState('-13.5204')

  const [longitude, setLongitude] =
    useState('-71.9751')

  const [
    locationLoading,
    setLocationLoading,
  ] = useState(false)

  const [
    locationMessage,
    setLocationMessage,
  ] = useState('')

  const [
    locationSaved,
    setLocationSaved,
  ] = useState(false)


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

      setEmergencyId(
        emergency.id,
      )

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


  function updateLocation(
    newLatitude: number,
    newLongitude: number,
  ) {
    setLatitude(
      newLatitude.toFixed(6),
    )

    setLongitude(
      newLongitude.toFixed(6),
    )

    setLocationMessage(
      'Ubicación seleccionada.',
    )

    setLocationSaved(false)
  }


  function useCurrentLocation() {
    setLocationMessage('')
    setError('')

    if (!navigator.geolocation) {
      setLocationMessage(
        'La geolocalización no está disponible en este navegador.',
      )
      return
    }

    setLocationLoading(true)

    navigator.geolocation.getCurrentPosition(
      (position) => {
        updateLocation(
          position.coords.latitude,
          position.coords.longitude,
        )

        setLocationMessage(
          'Ubicación actual obtenida correctamente.',
        )

        setLocationLoading(false)
      },
      () => {
        setLocationMessage(
          'No fue posible obtener tu ubicación. Puedes seleccionarla manualmente en el mapa.',
        )

        setLocationLoading(false)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      },
    )
  }


  async function handleSaveLocation() {
    if (!emergencyId) {
      setError(
        'Primero debes activar una alerta SOS.',
      )
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

    setLocationLoading(true)
    setLocationMessage('')
    setError('')

    try {
      const emergency =
        await updateEmergencyLocation(
          emergencyId,
          Number(latitude),
          Number(longitude),
          token,
        )

      setLatitude(
        Number(
          emergency.latitude,
        ).toFixed(6),
      )

      setLongitude(
        Number(
          emergency.longitude,
        ).toFixed(6),
      )

      setLocationSaved(true)

      setLocationMessage(
        'Ubicación asociada correctamente a la alerta.',
      )
    } catch {
      setError(
        'No se pudo registrar la ubicación de la emergencia.',
      )
    } finally {
      setLocationLoading(false)
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


          {emergencyId &&
            selectedType && (
              <section className="sos-location-section">
                <div className="emergency-type-header">
                  <h2>
                    Ubicación de la emergencia
                  </h2>

                  <p>
                    Usa tu ubicación actual
                    o selecciona manualmente
                    el punto en el mapa.
                  </p>
                </div>

                <button
                  type="button"
                  className="location-button"
                  onClick={
                    useCurrentLocation
                  }
                  disabled={
                    locationLoading
                  }
                >
                  {locationLoading
                    ? 'Obteniendo ubicación...'
                    : '📍 Usar mi ubicación actual'}
                </button>

                <LocationPicker
                  latitude={
                    Number(latitude)
                  }
                  longitude={
                    Number(longitude)
                  }
                  onLocationChange={
                    updateLocation
                  }
                />

                <p className="location-help">
                  Puedes hacer clic sobre
                  el mapa o arrastrar el
                  marcador para ajustar
                  la ubicación.
                </p>

                <div className="coordinates-grid">
                  <div>
                    <label htmlFor="sos-latitude">
                      Latitud
                    </label>

                    <input
                      id="sos-latitude"
                      type="number"
                      step="any"
                      value={latitude}
                      onChange={(event) => {
                        setLatitude(
                          event.target.value,
                        )
                        setLocationSaved(
                          false,
                        )
                      }}
                    />
                  </div>

                  <div>
                    <label htmlFor="sos-longitude">
                      Longitud
                    </label>

                    <input
                      id="sos-longitude"
                      type="number"
                      step="any"
                      value={longitude}
                      onChange={(event) => {
                        setLongitude(
                          event.target.value,
                        )
                        setLocationSaved(
                          false,
                        )
                      }}
                    />
                  </div>
                </div>

                <button
                  type="button"
                  className="sos-location-save"
                  onClick={
                    handleSaveLocation
                  }
                  disabled={
                    locationLoading
                  }
                >
                  {locationLoading
                    ? 'Guardando ubicación...'
                    : 'Guardar ubicación'}
                </button>

                {locationMessage && (
                  <p className="location-message">
                    {
                      locationMessage
                    }
                  </p>
                )}

                {locationSaved && (
                  <div className="sos-location-success">
                    Ubicación registrada
                    y asociada a la alerta.
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