const { MariaDB } = require("./DBconnection");

const db = new MariaDB();

module.exports = db;