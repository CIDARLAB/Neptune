var exports = module.exports;
var express = require('express');
var cmd = require('node-cmd');
var path = require('path');
var mkdirp = require('mkdirp');
var jsonfile = require('jsonfile');
var mongoose = require('mongoose');
var fs = require('fs');
var AWS = require('aws-sdk');
var remove = require('rimraf');
var User = require('../models/user');
var Workspace = require('../models/workspace');
var File = require('../models/file');
var Job = require('../models/job');
var zip = require('express-zip');

AWS.config.update({
    accessKeyId: process.env['NEPTUNE_AWSID'],
    secretAccessKey: process.env['NEPTUNE_AWSKEY']
});

var s3 = new AWS.S3();

exports.downloadFile = function(req, res) {

    var Target_Object_KEY = req.query.id.toString();
    var Target_BUCKET_ID = process.env['NEPTUNE_S3_BUCKET_ID'];
    var fileName = req.query.name.toString();

    var Parameters = {
        Bucket: Target_BUCKET_ID,
        Key: Target_Object_KEY,
        ResponseContentEncoding: 'utf-8',
        ResponseContentType: 'string/utf-8'
    };

    var filepath = path.join(global.Neptune_ROOT_DIR, "downloads", fileName);

    fs.closeSync(fs.openSync(filepath, 'w'));
    s3.getObject(Parameters, function(error, data) {
        var fd = fs.openSync(filepath, 'w+');
        fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
        fs.close(fd, function() {
            res.download(filepath, fileName, function(err) {
                if (err) {
                    console.log("File Download Error");
                    console.log(err);
                    fs.unlink(filepath);
                } else {
                    console.log("File Download Success");
                    fs.unlink(filepath);
                }
            });

        });
    });

};


// Deprecated Notes and functions
// ---------------------------------------
// body = function getS3Text(key) {
//     var Target_BUCKET_ID = process.env['NEPTUNE_S3_BUCKET_ID'];
//     var Target_Object_KEY = key;
//     var Parameters = {
//         Bucket: Target_BUCKET_ID,
//         Key: Target_Object_KEY,
//         ResponseContentEncoding: 'utf-8',
//         ResponseContentType: 'string/utf-8'
//     };
//     s3.getObject(Parameters,function(err,data){
//         if(err){ console.err(err); res.send(500); throw err; }
//         res.send(data.Body);
//     });
// };
// res.setHeader('Content-disposition', 'attachment; filename=' + fileName);
// var filestream = fs.createReadStream(file);
// filestream.pipe(res);
// var options = {
//     root: filepath,
//     dotfiles: 'deny',
//     headers: {
//         'x-timestamp': Date.now(),
//         'x-sent': true
//     }
// };
// res.sendFile(fileName, options, function (err) {
//     if (err) {
//         console.log(err);
//     } else {
//         console.log('Sent:', fileName);
//     }
// });
//
// res.zip([
//     { path: filepath, name: fileName }
//     // { path: '/path/to/file2.name', name: 'file2.name' }
// ]);
//res.setHeader('Content-disposition', 'attachment; filename=data.xlsx');
//res.setHeader('Content-type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
//res.set("Content-Disposition", "attachment; filename=" + filepath);
//res.attachment(filepath);
//res.end();