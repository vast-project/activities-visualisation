const db = require('../config/db.config.js');
const Activity = db.Activity;

/* Save an Activity object to datadase PostgreSQL
*@param (*) req
*@param (*) res
*/
exports.createActivity = (req, res) => {
    let activity = {};

    try{
        //Building Activity object from uploading request's body
        activity.eventid = req.body.eventid;
        activity.randomid = req.body.randomid;
        activity.eventdatafromdb = req.body.eventdatafromdb;
        activity.userformdata = req.body.userformdata;
        
        //Save to PostgreSQL database
        Activity.create(activity,
                {attributes: ['id', 'eventid', 'randomid', 'eventdatafromdb', 'userformdata']})
            .then (result => {
                res.status(200).json(result);
            });
    }
    catch(error){
        res.status(500).json({
            message: "Fail!!",
            error: error.message
        });
    }

}

/* Updating an Activity
*@param (*) req
*@param (*) res
*/
exports.updateActivity = async(req, res)=> {
    try {
        let activity = await Activity.findOne({ where: {randomid: req.body.randomid} });

        if (!activity){
            //return response to client
            res.status(404).json({
                message: "Not found for updating an activity with id = " + req.params.id,
                error: "404"
            });
        }
        else {
            let updatedObject = {
                randomid: req.body.randomid,
                activitydata: req.body.activitydata
            }
            let result = await Activity.update(updatedObject, {
                    returning:true,
                    where: {randomid: req.body.randomid},
                    attributes: ['id', 'randomid', 'activitydata']
                });
            if(!result) {
                res.status(500).json({
                    message: "Error -> Cannot update an activity with id = " + req.params.id,
                    error: "Cannot Update"
                })
            }
            res.status(200).json(result);
        }
    }
    catch
    {
        res.status(500).json({
            message: "Error -> Cannot update an activity with id = " + req.params.id,
            error: "Cannot Update 2"
        });
    }
}
