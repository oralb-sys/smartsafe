export interface ReportListItem {
  id: string
  category: string
  status: string
  created_at: string
}

export interface ReportDetail {
  id: string
  category: string
  description: string | null
  latitude: number
  longitude: number
  photo_url: string | null
  status: string
  created_at: string
}