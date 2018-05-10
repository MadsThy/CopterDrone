var fs             =         require('fs')
var events         =         require('events');
var express        =         require("express");
var bodyParser     =         require("body-parser");
var spawn          =         require("child_process").spawn;
var path           =         require('path')
var app            =         express();

//--------------------------------------------------
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

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
  
  //Print to console
  console.log("Command: " + usercommand);

  //Create eventhandler
  var eventEmitter = new events.EventEmitter();
  
  //Append time and command to a file
  var myEventHandler = function () {
    fs.appendFile('usercommands.txt', "Command: " + usercommand 
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

  //Call python script
  var process = spawn('python',["scripts.py", usercommand] );
    process.stdout.on('data', function(data) {
        console.log(data.toString());
    });

  res.end("yes");
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
//Listen on port 3000
app.listen(3000, '0.0.0.0', function() {
  console.log('Listening to port:  ' + 3000);
});