export type UserRole = 'CITIZEN' | 'OPERATOR'

export interface LoginResponse {
  access_token: string
  token_type: string
  role: UserRole
}