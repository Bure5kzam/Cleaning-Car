const express = require('express');
const app = express();
const cors = require('cors')
const {pool} = require('./mysql');
const PORT = 8080;
app.use(cors())
app.use(express.urlencoded({extended:false}));
app.use(express.json());

app.get("/status", async (req, res) => {
    try {
        const command = await pool.query("select * from command_02 where is_finish = 1 limit 1");
        const sense = await pool.query("select * from sensing_02 order by time desc limit 1")
        console.log(command[0][0], sense[0][0])
        res.send({data:{command: command[0][0], sense : sense[0][0]}});
    } catch (error) {
        res.send({"error":error});
    }
})

app.listen(PORT, () => console.log(`this server ${PORT}`));