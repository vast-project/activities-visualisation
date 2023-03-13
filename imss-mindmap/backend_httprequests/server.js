const express = require('express');
const app = express();
var bodyParser = require('body-parser');
global.__basedir__ = __dirname;
const db =  require('./config/db.config.js');
const Activity = db.Activity;
let router = require('./routers/router.js');
const cors = require('cors');
const corsOptions = {
    origin: 'http://localhost:4200',
    optionsSuccessStatus: 200
}
app.use(cors(corsOptions));
app.use(bodyParser.json());
app.use(express.static('resources'));
app.use('/', router);

//Create a server
const server = app.listen(6072, function(){
    let host = server.address().address
    let port = server.address().port
    console.log("App listening at http://%s:%s", host, port);
})

//db.sequelize.sync({force: true}).then(() => {
//    console.log('Drop and Resync with {force: true}');
//    Activity.sync().then(() => {
//    const activities = [
//        {randomid: 345678234, userformdata: 'user data from form'},
//        {eventid: 2, randomid: 345674987, eventdatafromdb: 'datafromdb2', userformdata: 'user data from form2'},
//        {eventid: 3, randomid: 698754678, eventdatafromdb: 'datafromdb3', userformdata: 'user data from form3', activitydata: 'activitydat3'}
//    ]
//    for (let i=0; i<activities.length; i++){
//        Activity.create(activities[i]);
//    }
//    })
//});