const env = require('./env.js');

const Sequelize = require('sequelize');
const sequelize = new Sequelize(env.database, env.username, env.password, {
    host: env.host,
    dialect: env.dialect,
    operatorsAlianses: false,

    pool: {
        max: env.max,
        min: env.min,
        acquire: env.acquire,
        idle: env.edle
    }
});
const db = {};
db.Sequelize = Sequelize;
db.sequelize = sequelize;
db.Activity = require('../models/activity.model.js')(sequelize, Sequelize);

module.exports = db;