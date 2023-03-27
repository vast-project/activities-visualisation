const express = require('express');
const app = express();
var bodyParser = require('body-parser');
let router = require('./routers/router.js');
const cors = require('cors');
const corsOptions = {
    origin: '*',  //'http://localhost:4200',
    optionsSuccessStatus: 200
}
app.use(cors(corsOptions));
app.use(bodyParser.json());
app.use(express.static('resources'));
app.use('/', router);

//Create a server
const server = app.listen(8080, function(){
    let host = server.address().address
    let port = server.address().port
    console.log("App listening at http://%s:%s", host, port);
})
