const request = require('supertest');
const app = require('../app');
const db = require('../bin/db');

jest.mock('../bin/db', () => ({
  executeQuery: jest.fn(),
  execute: jest.fn(),
  connect: jest.fn(),
  disconnect: jest.fn(),
}));

describe('POST / (registrar evento - web)', () => {

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('debe registrar un evento correctamente', async () => {

    db.executeQuery.mockResolvedValue([
      { id: 1, nombres: 'Rony', apellidos: 'Villafuerte' }
    ]);
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
  });

});


describe('POST /api/eventos (registrar evento - API JSON)', () => {

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('debe registrar un evento y devolver JSON con success:true', async () => {

    db.executeQuery.mockResolvedValue([
      { id: 1, nombres: 'Rony', apellidos: 'Villafuerte' }
    ]);
    db.execute.mockResolvedValue({ insertId: 25 });

    const res = await request(app)
      .post('/api/eventos')
      .field('usuario', '12345678')
      .field('tipo', 'Incendio')
      .field('descripcion', 'Incendio en local comercial')
      .field('latitud', '-13.5183')
      .field('longitud', '-71.9781')
      .attach('foto', Buffer.from('fake-image-content'), {
        filename: 'test.jpg',
        contentType: 'image/jpeg'
      });

    expect(res.statusCode).toBe(201);
    expect(res.body.success).toBe(true);
    expect(res.body.id_evento).toBe(25);
    expect(res.body.usuario.dni).toBe('12345678');
    expect(res.body.foto).toContain('/uploads/');
  });

  it('debe devolver JSON con success:false si falta el DNI', async () => {

    const res = await request(app)
      .post('/api/eventos')
      .field('tipo', 'Robo')
      .field('descripcion', 'Sin DNI')
      .field('latitud', '-13.5')
      .field('longitud', '-71.9')
      .attach('foto', Buffer.from('fake'), {
        filename: 'test.jpg',
        contentType: 'image/jpeg'
      });

    expect(res.statusCode).toBe(400);
    expect(res.body.success).toBe(false);
    expect(res.body.mensaje).toContain('DNI');
  });

  it('debe devolver 404 en JSON si el DNI no existe', async () => {

    db.executeQuery.mockResolvedValue([]);

    const res = await request(app)
      .post('/api/eventos')
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
    expect(res.body.success).toBe(false);
  });

});