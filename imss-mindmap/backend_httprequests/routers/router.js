let express = require('express');
let router = express.Router();

const activities = require('../controllers/controller.js');

router.post('/api/activity', activities.createActivity);
router.put('/api/activity', activities.updateActivity);

module.exports = router;
