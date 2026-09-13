import { useEffect } from 'react'
import {
  MapContainer,
  Marker,
  TileLayer,
  useMap,
  useMapEvents,
} from 'react-leaflet'
import { divIcon } from 'leaflet'

interface LocationPickerProps {
  latitude: number
  longitude: number
  onLocationChange: (
    latitude: number,
    longitude: number,
  ) => void
}

const locationIcon = divIcon({
  className: 'location-marker',
  html: '<div class="location-marker-dot"></div>',
  iconSize: [24, 24],
  iconAnchor: [12, 12],
})

function MapClickHandler({
  onLocationChange,
}: {
  onLocationChange: (
    latitude: number,
    longitude: number,
  ) => void
}) {
  useMapEvents({
    click(event) {
      onLocationChange(
        event.latlng.lat,
        event.latlng.lng,
      )
    },
  })

  return null
}

function RecenterMap({
  latitude,
  longitude,
}: {
  latitude: number
  longitude: number
}) {
  const map = useMap()

  useEffect(() => {
    map.setView(
      [latitude, longitude],
      map.getZoom(),
    )
  }, [latitude, longitude, map])

  return null
}

function LocationPicker({
  latitude,
  longitude,
  onLocationChange,
}: LocationPickerProps) {
  return (
    <MapContainer
      center={[latitude, longitude]}
      zoom={16}
      scrollWheelZoom
      className="location-map"
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker
        position={[latitude, longitude]}
        icon={locationIcon}
        draggable
        eventHandlers={{
          dragend(event) {
            const marker = event.target
            const position = marker.getLatLng()

            onLocationChange(
              position.lat,
              position.lng,
            )
          },
        }}
      />

      <MapClickHandler
        onLocationChange={onLocationChange}
      />

      <RecenterMap
        latitude={latitude}
        longitude={longitude}
      />
    </MapContainer>
  )
}

export default LocationPicker