import type {
  ReportDetail,
  ReportListItem,
} from '../types/report'

const API_BASE_URL =
  'http://localhost:8000/api/v1'


export async function login(
  email: string,
  password: string,
) {
  const response = await fetch(
    `${API_BASE_URL}/auth/login`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    },
  )

  if (!response.ok) {
    throw new Error(
      'Credenciales inválidas',
    )
  }

  return response.json()
}


export async function getMyReports(
  token: string,
): Promise<ReportListItem[]> {
  const response = await fetch(
    `${API_BASE_URL}/reports`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudieron obtener los reportes.',
    )
  }

  return response.json()
}


export async function getReportDetail(
  reportId: string,
  token: string,
): Promise<ReportDetail> {
  const response = await fetch(
    `${API_BASE_URL}/reports/${reportId}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudo obtener el detalle del reporte.',
    )
  }

  return response.json()
}


export interface EmergencyCreateResponse {
  id: string
  status: string
  created_at: string
}


export type EmergencyType =
  | 'MEDICAL'
  | 'ACCIDENT'
  | 'FIRE'
  | 'PERSONAL_SECURITY'


export async function createEmergency(
  token: string,
): Promise<EmergencyCreateResponse> {
  const response = await fetch(
    `${API_BASE_URL}/emergencies`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudo activar la alerta SOS.',
    )
  }

  return response.json()
}


export interface EmergencyLocationResponse {
  id: string
  latitude: number
  longitude: number
  status: string
}


export async function updateEmergencyLocation(
  emergencyId: string,
  latitude: number,
  longitude: number,
  token: string,
): Promise<EmergencyLocationResponse> {
  const response = await fetch(
    `${API_BASE_URL}/emergencies/${emergencyId}/location`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        latitude,
        longitude,
      }),
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudo registrar la ubicación de la emergencia.',
    )
  }

  return response.json()
}


export interface EmergencyListItem {
  id: string
  status: string
  latitude: number | null
  longitude: number | null
  created_at: string
}


export interface EmergencyDetail {
  id: string
  user_id: string
  status: string
  latitude: number | null
  longitude: number | null
  created_at: string
}


export async function getEmergencies(
  token: string,
): Promise<EmergencyListItem[]> {
  const response = await fetch(
    `${API_BASE_URL}/emergencies`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudieron obtener las emergencias.',
    )
  }

  return response.json()
}


export async function getEmergencyDetail(
  emergencyId: string,
  token: string,
): Promise<EmergencyDetail> {
  const response = await fetch(
    `${API_BASE_URL}/emergencies/${emergencyId}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudo obtener el detalle de la emergencia.',
    )
  }

  return response.json()
}


export type EmergencyStatus =
  | 'ACTIVE'
  | 'IN_PROGRESS'
  | 'FINISHED'


export interface EmergencyStatusUpdateResponse {
  id: string
  status: EmergencyStatus
}


export async function updateEmergencyStatus(
  emergencyId: string,
  newStatus: EmergencyStatus,
  token: string,
): Promise<EmergencyStatusUpdateResponse> {
  const response = await fetch(
    `${API_BASE_URL}/emergencies/${emergencyId}`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        status: newStatus,
      }),
    },
  )

  if (!response.ok) {
    throw new Error(
      'No se pudo actualizar el estado de la emergencia.',
    )
  }

  return response.json()
}