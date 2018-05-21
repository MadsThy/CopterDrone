var request = require('request');
var Promise = require('bluebird');
var qs = require('qs');

var JAR = request.jar();
var base = 'http://api.3drobotics.com/api/v1';
var app_id = process.env.DRONEKIT_APPID;
var app_key = process.env.DRONEKIT_APPKEY;

function fetch (path, args) {

  return {
    get: function (next) {
      return go('GET', args || {}, undefined, next)
    },
    post: function (next, body) {
      return go('POST', args || {}, body, next)
    }
  };

  function go (method, args, body, next) {
    return new Promise(function (resolve, reject) {
      args.api_key = app_id + '.' + app_key;
      var url = base + '/' + path.replace(/^\//, '') + '?' + qs.stringify(args);
      request({
        method: method,
        url: url,
        json: true,
        form: body,
        jar: JAR,
        timeout: 10*1000,
      }, function (error, response, body) {
        if (error) {
          reject(error, 'hi');
        } else {
          var res = {
            status: response.statusCode,
            headers: response.headers,
            body: body,
            toString: function () {
              return body.message
            },
          };

          if (response.statusCode.toString().slice(0, 1) != '2') {
            reject(res);
          } else {
            resolve(res);
          }
        }
      })
    })
    .nodeify(next, {
      spread: true
    });
  }
}

// fetch('api/v1/auth/user').get()
// .then(function (res) {
//   console.log('success', res);
// }, function (res) {
//   console.log('err', res);
// })

fetch('auth/login', {
  login: process.env.DRONEKIT_LOGIN,
  password: process.env.DRONEKIT_PASSWORD,
}).post()
.then(function (res) {
  console.log('Logged in!');
  console.log(res.body);
//   return fetch('vehicle/1', {
//   }).get()
// })
// .then(function (res) {
//   console.log(res.body);
})