//The required keywords below needs to be installed with node.js npm or the program will not run.
var fs             =         require('fs')
var events         =         require('events');
var express        =         require("express");
var bodyParser     =         require("body-parser");
var spawn          =         require("child_process").spawn;
var path           =         require('path')
var app            =         express();

//--------------------------------------------------
//To use bodyparser
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

//To use static files like javascript and css
app.use(express.static(path.join(__dirname, 'public')));

//--------------------------------------------------
//Serve html page
app.get('/',function(req,res){
  res.sendfile("Index.html");
});

//--------------------------------------------------
//AJAX call from /command
app.post('/command',function(req,res){

  //Get HTML element value
  var usercommand=req.body.command;
  var usercommandValue=req.body.commandValue;
  
  //Print to console
  console.log("Command: " + usercommand + " with value: " + usercommandValue + " has been sent to the drone");

  //Create eventhandler
  var eventEmitter = new events.EventEmitter();
  
  //Append time and command to a file
  var myEventHandler = function () {
    fs.appendFile('usercommands.txt', "Command: " + usercommand + " with value: " + usercommandValue
    + " has been sent to the drone on: " + new Date().toISOString().
    replace(/T/, ' '). // replace T with a space
    replace(/\..+/, '')  + "\r\n", function (err) {
      if (err) throw err;
      console.log('The file has been saved on the system.');
    });
  }
  
  //Assign the event handler to an event:
  eventEmitter.on('savefile', myEventHandler);
  
  //Fire the 'savefile' event:
  eventEmitter.emit('savefile');  

  //Call python script and get a return value from the "data" parameter
  var process = spawn('python',["scripts.py", usercommand, usercommandValue] );
    process.stdout.on('data', function(data) {
        console.log(data.toString());
    });
  res.end("yes");
});

//--------------------------------------------------
//AJAX call from /dronestatus
app.post('/dronestatus',function(req,res){
  //Call python script and get a return value from the "data" parameter
  var process = spawn('python',["droneinfo.py", usercommand, usercommandValue] );
    process.stdout.on('data', function(data) {
        console.log(data.toString());
        res.send(data);
    });
  });

//--------------------------------------------------
//Read Userlog
app.post('/userlog',function(req,res){
  fs.readFile('usercommands.txt', 'utf8', function(err, data){
    if (err) throw err;
    res.send(data);
  });
});

//--------------------------------------------------
//Listen on port 3000. This also allows to connect to the device hosting the node.js server, if both devices are on the same network
app.listen(3000, '0.0.0.0', function() {
  console.log('Listening to port:  ' + 3000);
});