var express = require('express');
var router = express.Router();

const multer = require('multer');
const path = require('path');

const { registrarEvento, ValidationError } = require('../services/evento.service');


// ========================================
// CONFIGURACIÓN DE MULTER
// ========================================

const storage = multer.diskStorage({

  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, '../public/uploads'));
  },

  filename: function (req, file, cb) {
    const extension = path.extname(file.originalname);
    const nombre = 'evento-' + Date.now() + extension;
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
// REGISTRAR EVENTO DESDE LA PÁGINA WEB
// ========================================

router.post('/', upload.single('foto'), async (req, res, next) => {

  try {

    const { usuario, tipo, descripcion, latitud, longitud } = req.body;

    const resultado = await registrarEvento({
      usuario,
      tipo,
      descripcion,
      latitud,
      longitud,
      archivo: req.file
    });

    res.status(201).render('correcto', {
      nombres: resultado.usuario.nombres,
      apellidos: resultado.usuario.apellidos,
      insertId: resultado.idEvento
    });

  } catch (error) {

    if (error instanceof ValidationError) {
      return res.status(error.status).send(error.message);
    }

    console.error('Error al registrar evento:', error);
    next(error);

  }

});


// =====================================================
// API REST - REGISTRAR EVENTO
// =====================================================
//
// Permite que otras aplicaciones (ej. Python)
// registren eventos.
//
// POST /api/eventos
// =====================================================

router.post('/api/eventos', upload.single('foto'), async (req, res, next) => {

  try {

    const { usuario, tipo, descripcion, latitud, longitud } = req.body;

    const resultado = await registrarEvento({
      usuario,
      tipo,
      descripcion,
      latitud,
      longitud,
      archivo: req.file
    });

    return res.status(201).json({
      success: true,
      mensaje: 'Evento registrado correctamente.',
      id_evento: Number(resultado.idEvento),
      usuario: resultado.usuario,
      foto: resultado.fotoPath
    });

  } catch (error) {

    if (error instanceof ValidationError) {
      return res.status(error.status).json({
        success: false,
        mensaje: error.message
      });
    }

    console.error('Error en API /api/eventos:', error);
    next(error);

  }

});


module.exports = router;