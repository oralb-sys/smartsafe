const request = require('supertest');
const path = require('path');
const app = require('../app');
const db = require('../bin/db');

// Mockeamos el módulo db (executeQuery = buscar usuario, execute = insertar evento)
jest.mock('../bin/db', () => ({
  executeQuery: jest.fn(),
  execute: jest.fn(),
  connect: jest.fn(),
  disconnect: jest.fn(),
}));

describe('POST / (registrar evento)', () => {

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('debe registrar un evento correctamente', async () => {

    // Simula que el DNI SÍ existe en tUsuario
    db.executeQuery.mockResolvedValue([
      { id: 1, nombres: 'Rony', apellidos: 'Villafuerte' }
    ]);

    // Simula el INSERT exitoso
    db.execute.mockResolvedValue({ insertId: 10 });

    const res = await request(app)
      .post('/')
      .field('usuario', '12345678')
      .field('tipo', 'Robo')
      .field('descripcion', 'Robo en la esquina')
      .field('latitud', '-13.5183')
      .field('longitud', '-71.9781')
      .attach('foto', Buffer.from('fake-image-content'), {
        filename: 'test.jpg',
        contentType: 'image/jpeg'
      });

    expect(res.statusCode).toBe(201);
    expect(res.text).toContain('Evento reportado');
    expect(db.executeQuery).toHaveBeenCalledTimes(1);
    expect(db.execute).toHaveBeenCalledTimes(1);
  });

  it('debe fallar si falta el DNI (usuario)', async () => {
    const res = await request(app)
      .post('/')
      .field('tipo', 'Robo')
      .field('descripcion', 'Evento sin DNI')
      .field('latitud', '-13.5')
      .field('longitud', '-71.9')
      .attach('foto', Buffer.from('fake'), {
        filename: 'test.jpg',
        contentType: 'image/jpeg'
      });

    expect(res.statusCode).toBe(400);
    expect(res.text).toContain('DNI');
    expect(db.executeQuery).not.toHaveBeenCalled();
  });

  it('debe fallar si falta el tipo de evento', async () => {
    const res = await request(app)
      .post('/')
      .field('usuario', '12345678')
      .field('descripcion', 'Evento sin tipo')
      .field('latitud', '-13.5')
      .field('longitud', '-71.9')
      .attach('foto', Buffer.from('fake'), {
        filename: 'test.jpg',
        contentType: 'image/jpeg'
      });

    expect(res.statusCode).toBe(400);
    expect(res.text).toContain('tipo');
  });

  it('debe fallar si faltan coordenadas GPS', async () => {
    const res = await request(app)
      .post('/')
      .field('usuario', '12345678')
      .field('tipo', 'Robo')
      .field('descripcion', 'Evento sin coordenadas')
      .attach('foto', Buffer.from('fake'), {
        filename: 'test.jpg',
        contentType: 'image/jpeg'
      });

    expect(res.statusCode).toBe(400);
    expect(res.text).toContain('coordenadas');
  });

  it('debe fallar si no se adjunta foto', async () => {
    const res = await request(app)
      .post('/')
      .field('usuario', '12345678')
      .field('tipo', 'Robo')
      .field('descripcion', 'Evento sin foto')
      .field('latitud', '-13.5')
      .field('longitud', '-71.9');

    expect(res.statusCode).toBe(400);
    expect(res.text).toContain('fotografía');
  });

  it('debe responder 404 si el DNI no existe en tUsuario', async () => {

    // Simula que la búsqueda no encuentra al usuario
    db.executeQuery.mockResolvedValue([]);

    const res = await request(app)
      .post('/')
      .field('usuario', '99999999')
      .field('tipo', 'Robo')
      .field('descripcion', 'DNI inexistente')
      .field('latitud', '-13.5')
      .field('longitud', '-71.9')
      .attach('foto', Buffer.from('fake'), {
        filename: 'test.jpg',
        contentType: 'image/jpeg'
      });

    expect(res.statusCode).toBe(404);
    expect(res.text).toContain('no corresponde a un usuario registrado');
    expect(db.execute).not.toHaveBeenCalled();
  });

});