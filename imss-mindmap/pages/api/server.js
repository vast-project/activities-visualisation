const express = require('express');
const app = express();
var bodyParser = require('body-parser');
global.__basedir__ = __dirname;
const db =  require('./config/dbconfig.js');
const Activity = db.Activity;
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
const server = app.listen(6071, function(){
    let host = server.address().address
    let port = server.address().port
    console.log("App listening at http://%s:%s", host, port);
})

db.sequelize.sync({}).then(() => {
    console.log('Drop and Resync with {force: true}');
    Activity.sync().then(() => {
    const activities = [
        {eventid: 1, randomid: 546743, eventdatafromdb: 'DATA RETRIEVED FROM TABLE EVENTS', userformdata: 'DATA INSERTED FROM COMPONENT FORM', ACTIVITYDATA: 'DATA INSERTED FROM COMPONENT MINDMAP'},
        {randomid: 456, userformdata: 'DATA INSERTED FROM COMPONENT FORM', ACTIVITYDATA: 'DATA INSERTED FROM COMPONENT MINDMAP'}
    ]
    for (let i=0; i<activities.length; i++){
        Activity.create(activities[i]);
    }
    })
});
