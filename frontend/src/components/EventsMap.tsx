import {
  useEffect,
} from 'react'

import {
  divIcon,
  latLngBounds,
} from 'leaflet'

import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMap,
} from 'react-leaflet'

import type {
  UrbanEvent,
} from '../services/api'

import './EventsMap.css'


interface EventsMapProps {
  events: UrbanEvent[]
  onSelectEvent: (
    event: UrbanEvent,
  ) => void
}


const reportIcon = divIcon({
  className:
    'urban-event-marker-wrapper',
  html: (
    '<div class="urban-event-marker ' +
    'urban-event-marker-report">' +
    'R' +
    '</div>'
  ),
  iconSize: [32, 32],
  iconAnchor: [16, 16],
})


const sosIcon = divIcon({
  className:
    'urban-event-marker-wrapper',
  html: (
    '<div class="urban-event-marker ' +
    'urban-event-marker-sos">' +
    'SOS' +
    '</div>'
  ),
  iconSize: [38, 38],
  iconAnchor: [19, 19],
})


function FitMapToEvents({
  events,
}: {
  events: UrbanEvent[]
}) {
  const map = useMap()

  useEffect(() => {
    const locatedEvents =
      events.filter(
        (event) =>
          event.latitude !== null &&
          event.longitude !== null,
      )

    if (
      locatedEvents.length === 0
    ) {
      return
    }

    if (
      locatedEvents.length === 1
    ) {
      const event =
        locatedEvents[0]

      map.setView(
        [
          event.latitude as number,
          event.longitude as number,
        ],
        16,
      )

      return
    }

    const bounds = latLngBounds(
      locatedEvents.map(
        (event) => [
          event.latitude as number,
          event.longitude as number,
        ],
      ),
    )

    map.fitBounds(
      bounds,
      {
        padding: [30, 30],
      },
    )
  }, [
    events,
    map,
  ])

  return null
}


function formatDate(
  value: string,
) {
  return new Intl.DateTimeFormat(
    'es-PE',
    {
      dateStyle: 'short',
      timeStyle: 'short',
    },
  ).format(
    new Date(value),
  )
}


function EventsMap({
  events,
  onSelectEvent,
}: EventsMapProps) {
  const locatedEvents =
    events.filter(
      (event) =>
        event.latitude !== null &&
        event.longitude !== null,
    )

  return (
    <MapContainer
      center={[
        -13.5204,
        -71.9751,
      ]}
      zoom={13}
      scrollWheelZoom
      className="events-map"
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url={
          'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        }
      />

      <FitMapToEvents
        events={locatedEvents}
      />

      {locatedEvents.map(
        (event) => (
          <Marker
            key={event.id}
            position={[
              event.latitude as number,
              event.longitude as number,
            ]}
            icon={
              event.source ===
              'SMART_SOS'
                ? sosIcon
                : reportIcon
            }
            eventHandlers={{
              click() {
                onSelectEvent(
                  event,
                )
              },
            }}
          >
            <Popup>
              <div className="event-popup">
                <strong>
                  {event.source ===
                  'SMART_SOS'
                    ? 'SmartSOS'
                    : 'SmartReport'}
                </strong>

                <p>
                  Tipo: {event.type}
                </p>

                <p>
                  Estado:
                  {' '}
                  {event.status}
                </p>

                <p>
                  {
                    formatDate(
                      event.created_at,
                    )
                  }
                </p>
              </div>
            </Popup>
          </Marker>
        ),
      )}
    </MapContainer>
  )
}

export default EventsMap