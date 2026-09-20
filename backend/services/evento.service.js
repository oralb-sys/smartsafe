const db = require('../bin/db');

// ========================================
// ERROR TIPADO PARA VALIDACIONES
// ========================================
// Permite que cada ruta decida el formato
// de respuesta (HTML o JSON) usando el
// mismo status y mensaje.

class ValidationError extends Error {
  constructor(status, mensaje) {
    super(mensaje);
    this.status = status;
  }
}

// ========================================
// LÓGICA COMPARTIDA: REGISTRAR EVENTO
// ========================================
// Usada tanto por la ruta web (POST /) como
// por la API (POST /api/eventos).

async function registrarEvento({
  usuario,
  tipo,
  descripcion,
  latitud,
  longitud,
  archivo
}) {

  // ----- 1. VALIDACIONES -----

  if (!usuario) {
    throw new ValidationError(400, 'Debe ingresar el DNI del usuario.');
  }

  if (!tipo) {
    throw new ValidationError(400, 'Debe seleccionar el tipo de evento.');
  }

  if (!descripcion) {
    throw new ValidationError(400, 'Debe ingresar una descripción.');
  }

  if (!latitud || !longitud) {
    throw new ValidationError(400, 'No se pudieron obtener las coordenadas GPS.');
  }

  if (!archivo) {
    throw new ValidationError(400, 'Debe adjuntar una fotografía.');
  }

  // ----- 2. BUSCAR USUARIO -----

  const usuarios = await db.executeQuery(
    `
    SELECT id, nombres, apellidos
    FROM tUsuario
    WHERE dni = ?
    LIMIT 1
    `,
    [usuario]
  );

  // ----- 3. VERIFICAR USUARIO -----

  if (usuarios.length === 0) {
    throw new ValidationError(404, 'El DNI ingresado no corresponde a un usuario registrado.');
  }

  const idUsuario = usuarios[0].id;

  // ----- 4. RUTA DE LA FOTO -----

  const fotoPath = '/uploads/' + archivo.filename;

  // ----- 5. CREAR COORDENADAS -----

  const punto = `POINT(${longitud} ${latitud})`;

  // ----- 6. INSERTAR EVENTO -----

  const sql = `
    INSERT INTO tEvento
    (
      id_usuario,
      tipo,
      id_personal,
      descripcion,
      foto_path,
      coordenadas,
      estado,
      fue_atendido
    )
    VALUES
    (
      ?,
      ?,
      NULL,
      ?,
      ?,
      ST_GeomFromText(?),
      'Pendiente',
      FALSE
    )
  `,[idUsuario, tipo, descripcion, fotoPath, punto]
  ;

  const resultado = await db.execute(
    sql,
    [idUsuario, tipo, descripcion, fotoPath, punto]
  );

  // ----- 7. RESULTADO COMÚN -----

  return {
    idEvento: resultado.insertId,
    fotoPath: fotoPath,
    usuario: {
      dni: usuario,
      nombres: usuarios[0].nombres,
      apellidos: usuarios[0].apellidos
    }
  };

}

module.exports = {
  registrarEvento,
  ValidationError
};