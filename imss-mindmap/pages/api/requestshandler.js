console.log('Inserting to DB');
const db = require('./config/dbconfig.js');
const Activity = db.Activity;

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
