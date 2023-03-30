let express = require('express');
let router = express.Router();
const activities = require('../controllers/controller.js');

router.post('/api/activity', activities.create);
router.put('/api/activity', activities.update);

module.exports = router;