import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../services/api'
import type { LoginResponse } from '../types/auth'

function LoginPage() {
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const data: LoginResponse = await login(email, password)

      localStorage.setItem('smartsafe_token', data.access_token)
      localStorage.setItem('smartsafe_role', data.role)

      navigate('/dashboard')
    } catch {
      setError('No se pudo iniciar sesión. Verifica tus credenciales.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="login-page">
      <section className="login-card">
        <div className="login-brand">
          <h1>SmartSafe</h1>
          <p>Seguridad y gestión urbana en una sola plataforma.</p>
        </div>

        <form onSubmit={handleSubmit}>
          <h2>Iniciar sesión</h2>

          <label htmlFor="email">Correo electrónico</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />

          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          {error && <p className="form-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
      </section>
    </main>
  )
}

export default LoginPage