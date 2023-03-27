const { Sequelize } = require("sequelize");

module.exports = (sequelize, Sequelize) => {
    const Activity = sequelize.define('activitiesdata', {
        id: {
            type: Sequelize.INTEGER,
            autoIncrement: true,
            primaryKey: true
        },
        eventid: {
            type: Sequelize.INTEGER
        },
        randomid: {
            type: Sequelize.INTEGER
        },
        eventdatafromdb: {
            type: Sequelize.STRING
        },
        userformdata: {
            type: Sequelize.STRING
        },
        activitydata: {
            type: Sequelize.STRING
        }
    });
    return Activity;
}