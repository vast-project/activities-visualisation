const db = require('../config/dbconfig.js');
const Activity = db.Activity;
console.log('controller');

/* Save an Activity object to datadase PostgreSQL
*@param (*) req
*@param (*) res
*/
exports.create = (req, res) => {
    console.log('controllercr');
    let activity = {};

    try{
        //Building Activity object from uploading request's body
        activity.randomid = req.body.randomid;
        activity.userformdata = req.body.userformdata;
        console.log('23456');
        //Save to PostgreSQL database
        Activity.create(activity,
            {attributes: ['id',  'randomid', 'userformdata']})
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
exports.update = async(req, res)=> {
    console.log('controllerup');
    try {
        let activity = await Activity.findOne({ where: {randomid: req.body.randomid} });

        if (!activity){
            //return response to client
            res.status(404).json({
                message: "Not found for updating an activity with randomid = " + req.body.randomid,
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
                    message: "Error -> Cannot update an activity with randomid = " + req.body.randomid,
                    error: "Cannot Update"
                })
            }
            res.status(200).json(result);
        }
    }
    catch
    {
        res.status(500).json({
            message: "Error -> Cannot update an activity with randomid = " + req.body.randomid,
            error: "Cannot Update 2"
        });
    }
}