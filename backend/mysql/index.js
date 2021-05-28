const mysql = require("mysql2/promise");

const pool = mysql.createPool({
    host: "3.35.8.78",
    user: "SSAFY15_04_2",
    password:"1234",
    database: "DB_15_04",
    waitForConnections: true,
    connectionLimit : 10,
    queueLimit :0
})

module.exports={pool}