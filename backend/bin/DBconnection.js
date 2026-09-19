/**
 * AUTOR: Rony Villafuerte Serna
 * FECHA: 22-jun-2026
 * DESCRIPCIÓN:
 * Pool centralizado MariaDB reutilizable
 */

require("dotenv").config();

const mariadb = require("mariadb");

class MariaDB {

  static pool = null;

  static config = {
    host: process.env.MARIA_HOST,
    user: process.env.MARIA_USER,
    password: process.env.MARIA_PASSWORD,
    database: process.env.MARIA_DATABASE,

    connectionLimit: 10,
    acquireTimeout: 10000,
    connectTimeout: 10000,

    bigNumberStrings: true
  };

  async connect() {

    if (!MariaDB.pool) {

      MariaDB.pool = mariadb.createPool(MariaDB.config);
      console.log("Pool MariaDB iniciado");
    }

    return MariaDB.pool;
  }

  async disconnect() {

    if (MariaDB.pool) {

      await MariaDB.pool.end();
      MariaDB.pool = null;
      console.log("Pool MariaDB cerrado");
    }
  }

  async executeQuery(sql, params = []) {

    const pool = await this.connect();

    let conn;

    try {

      conn =
        await pool.getConnection();

      const result =
        await conn.query(sql, params);

      return result;

    } finally {

      if (conn) conn.release();
    }
  }

  async execute(sql, params = []) {

    const pool = await this.connect();

    let conn;

    try {

      conn =await pool.getConnection();
      const result =await conn.query(sql, params);
      return result;

    } finally {

      if (conn) conn.release();
    }
  }

  async getConnection() {

    const pool = await this.connect();

    return await pool.getConnection();
  }

}

module.exports = {
  MariaDB
};