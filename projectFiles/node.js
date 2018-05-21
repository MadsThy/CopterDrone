//The required keywords below needs to be installed with node.js npm or the program will not run.
var fs = require('fs')
var events = require('events');
var express = require("express");
var bodyParser = require("body-parser");
var spawn = require("child_process").spawn;
var path = require('path');
var app = express();

var cmd = require('node-cmd');

//--------------------------------------------------
//To use bodyparser
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

//To use static files like javascript and css.
//The static files are saved in the public folder in the project folder
app.use(express.static(path.join(__dirname, 'public')));

//CORS implementation
app.all('*', function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});
//--------------------------------------------------
//We use a technologi called "Express" to deliver an HTML page. 
//This response.sendfile does also work fine with any other files.
app.get('/', function (req, res) {
    res.sendfile("Index.html");
});

//--------------------------------------------------
//When receiving simple commands, do this to commands sent via x.x.x.x/commands?command=xxx
app.get('/commands', function (req, res) {
    commandString = 'python command.py '+req.param('command');
    var pyProcess = cmd.get(commandString);
    console.log("Command sent: "+commandString);

    res.end("OK"); //Something can be put here, if you want to return some data to the browser


    //Create eventhandler
    var eventEmitter = new events.EventEmitter();

    //Append date, time, and command to the logging file
    var myEventHandler = function () {
        fs.appendFile('usercommands.txt', "Command: " + usercommand + " sent at: " + new Date().toISOString().
                      replace(/T/, ' '). // replace T with a space
                      replace(/\..+/, '') + "\r\n", function (err) {
            if (err) throw err;
            console.log('[INFO] Command logged to file.');
        });
        //Assign the event handler to an event. "savefile" is the name of the event
        eventEmitter.on('savefile', myEventHandler);
        eventEmitter.emit('savefile');
    }

    });

//--------------------------------------------------
//AJAX call from /command. This sends a command to the drone by calling the scripts.py Python script. This also logs the command into a textfile stored locally.
app.post('/commands', function (req, res) {

    res.end("No POST commands ready yet."); //Something can be put here, if you want to return some data to the browser
});

//--------------------------------------------------
//AJAX call from /dronestatus. This reads the status of the Drone from the droneinfo.py Python script, and returns the value inside the HTML dronestatus textarea
app.get('/dronestatus', function (req, res) {

    console.log("Trying to get dronestatus");
    //Call python script and get a return value from the "data" parameter
    var process = spawn('python', ["droneinfo.py"]);
    process.stdout.on('data', function (data) {
        console.log(data.toString());

        //Create eventhandler
        var eventEmitter = new events.EventEmitter();

        //Append date, time, and droneinfo to a file
        var myEventHandler = function () {
            fs.appendFile('droneinfo.txt', data + " at: " + new Date().toISOString().
                          replace(/T/, ' '). // replace T with a space
                          replace(/\..+/, '') + "\r\n", function (err) {
                if (err) throw err;
                console.log('[INFO] File logged to system.');
            });
        }

        //Assign the event handler to an event:
        eventEmitter.on('savefile', myEventHandler);

        //Fire the 'savefile' event:
        eventEmitter.emit('savefile');

        //Send end data back to HTML textarea
        res.end(data);
    });
});

//--------------------------------------------------
//AJAX call from /userlog. This reads the usercommands.txt file and returns the value inside the HTML UserCommands textarea
app.get('/userlog', function (req, res) {

    fs.readFile('usercommands.txt', 'utf8', function (err, data) {
        if (err) throw err;
        //Send data back to HTML textarea
        res.send(data);
    });
});

//--------------------------------------------------
//Listen on port 80. This allows to connect to the device hosting the node.js server, if both devices are on the same network
app.listen(80, '0.0.0.0', function () {
    console.log('Listening to port:  ' + 80);
});