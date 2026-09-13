var express = require('express');
var router = express.Router();

const multer = require('multer');
const path = require('path');

const db = require('../bin/db');


// ========================================
// CONFIGURACIÓN DE MULTER
// ========================================

const storage = multer.diskStorage({

  destination: function (req, file, cb) {

    cb(
      null,
      path.join(__dirname, '../public/uploads')
    );

  },

  filename: function (req, file, cb) {

    const extension =
      path.extname(file.originalname);

    const nombre =
      'evento-' +
      Date.now() +
      extension;

    cb(null, nombre);

  }

});


const upload = multer({

  storage: storage,

  limits: {
    fileSize: 5 * 1024 * 1024
  },

  fileFilter: function (req, file, cb) {

    if (file.mimetype.startsWith('image/')) {

      cb(null, true);

    } else {

      cb(new Error('Solo se permiten imágenes'));

    }

  }

});


// ========================================
// MOSTRAR FORMULARIO
// ========================================

router.get('/', (req, res, next) => {

  res.render('index', {
    title: 'SmartSafe - Reportar evento'
  });

});


// ========================================
// REGISTRAR EVENTO
// ========================================

router.post(
  '/',
  upload.single('foto'),
  async (req, res, next) => {

    try {

      const {
        usuario,
        tipo,
        descripcion,
        latitud,
        longitud
      } = req.body;


      // ========================================
      // 1. VALIDACIONES
      // ========================================

      if (!usuario) {

        return res.status(400).send(
          'Debe ingresar el DNI del usuario.'
        );

      }


      if (!tipo) {

        return res.status(400).send(
          'Debe seleccionar el tipo de evento.'
        );

      }


      if (!descripcion) {

        return res.status(400).send(
          'Debe ingresar una descripción.'
        );

      }


      if (!latitud || !longitud) {

        return res.status(400).send(
          'No se pudieron obtener las coordenadas GPS.'
        );

      }


      if (!req.file) {

        return res.status(400).send(
          'Debe adjuntar una fotografía.'
        );

      }


      // ========================================
      // 2. BUSCAR USUARIO
      // ========================================

      const usuarios =
        await db.executeQuery(
          `
          SELECT id, nombres, apellidos
          FROM tUsuario
          WHERE dni = ?
          LIMIT 1
          `,
          [usuario]
        );


      // ========================================
      // 3. VERIFICAR USUARIO
      // ========================================

      if (usuarios.length === 0) {

        return res.status(404).send(
          'El DNI ingresado no corresponde a un usuario registrado.'
        );

      }


      const idUsuario =
        usuarios[0].id;


      // ========================================
      // 4. RUTA DE LA FOTO
      // ========================================

      const fotoPath =
        '/uploads/' + req.file.filename;


      // ========================================
      // 5. CREAR COORDENADAS
      // ========================================

      const punto =
        `POINT(${longitud} ${latitud})`;


      // ========================================
      // 6. INSERTAR EVENTO
      // ========================================

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
      `;


      const resultado =
        await db.execute(
          sql,
          [
            idUsuario,
            tipo,
            descripcion,
            fotoPath,
            punto
          ]
        );


      // ========================================
      // 7. RESPUESTA
      // ========================================

      res.status(201).send(`

        <!DOCTYPE html>

        <html lang="es">

        <head>

          <meta charset="UTF-8">

          <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0">

          <title>SmartSafe</title>

          <link
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
            rel="stylesheet">

        </head>


        <body class="bg-light">

          <div class="container py-5">

            <div class="row justify-content-center">

              <div class="col-12 col-md-8 col-lg-6">

                <div class="card shadow-sm">

                  <div class="card-body text-center p-4">

                    <h2 class="text-success">
                      ✓ Evento reportado
                    </h2>

                    <p class="mt-3">
                      Su reporte ha sido registrado correctamente.
                    </p>

                    <p>
                      Usuario:
                      <strong>
                        ${usuarios[0].nombres}
                        ${usuarios[0].apellidos}
                      </strong>
                    </p>

                    <p>
                      Estado:
                      <strong>Pendiente</strong>
                    </p>

                    <p>
                      Código del evento:
                      <strong>${resultado.insertId}</strong>
                    </p>

                    <a
                      href="/"
                      class="btn btn-primary">

                      Registrar otro evento

                    </a>

                  </div>

                </div>

              </div>

            </div>

          </div>

        </body>

        </html>

      `);


    } catch (error) {

      console.error(
        'Error al registrar evento:',
        error
      );

      next(error);

    }

  }
);


module.exports = router;