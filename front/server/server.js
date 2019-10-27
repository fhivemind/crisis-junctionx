var express         = require('express');
var morgan          = require('morgan')
var app             = express();

/// Configure timestamp logs
require('log-timestamp');
morgan.token('date', function(){
    return new Date().toISOString()
})

// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
/**
 * Carry function header controller.
 */
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

/// Log requests
app.use(morgan('[:date[web ]]\t\t :method :url :status :res[content-length] - :remote-addr - :response-time ms'))

/**
 * Event listener.
 */
app.listen(3000, function () {
    console.log('[  APP  ]\t Booted! Listening for requests on port :3000');
});

/**
 * -----------------------------------------------------
 * Serve site.
 * -----------------------------------------------------
 */
console.log('[  APP  ]\t Serving the site publically.');
app.use(express.static('public'));
app.use(function(req, res, next) {
    res.status(404).sendFile('404.html', {root: "public"});
});


/**
 * Clean object helper function.
 */
function cleanObject(obj) {
    for (var propName in obj) { 
        if (obj[propName] === null || obj[propName] === undefined) {
            delete obj[propName];
        }
    }
}