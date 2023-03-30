console.log('Inserting to DB');
//const db = require('./config/dbconfig.js');
//const Activity = db.Activity;


const express = require('express');
const app = express();
var bodyParser = require('body-parser');
global.__basedir__ = __dirname;
const db =  require('./config/dbconfig.js');
const Activity = db.Activity;
let router = require('./routers/router.js');
const cors = require('cors');
const corsOptions = {
    origin: '*',  //'http://localhost:3000',
    optionsSuccessStatus: 200
}
app.use(cors(corsOptions));
app.use(bodyParser.json());
app.use(express.static('resources'));
app.use('/', router);
//Create a server
const server = app.listen(3001, function(){
    let host = server.address().address
    let port = server.address().port
    console.log("App listening at http://%s:%s", host, port);
})

export default function handler(req, res) {
    const requestMethod = req.method;
    const activity = req.body;
    if(requestMethod ===  'POST') {
        db.sequelize.sync({}).then(() => {
            console.log('Drop and Resync with {force: true}');
            Activity.sync().then(() => {
                Activity.create(activity);
            })
        });
        console.log('POST');
        console.log(activity);
        res.json({ message: `POST OK` });
    }
    else if (requestMethod === 'GET') {
        Activity.update(activity);
        console.log('PUT');
        res.json({ message: `PUT OK` });
    }
    else {
        // handle other HTTP methods
        res.json({ message: 'JUST RETURN'});
    }
    console.log('Inserted to DB');
}
