var File = require('../models/file');
var AWS = require('aws-sdk');
var s3 = new AWS.S3();


module.exports.downloadFile = function(req, res) {
    var fileid = req.query.id;
    if (fileid == null || fileid == undefined || fileid === ''){
        res.sendStatus(500);
    }

    if (null == fileid) { res.sendStatus(400) }
    console.log("XXX requesting file id: " + fileid);

    //TODO: Check if file belongs to the user
    File.findById(fileid, function(err, data) {
        if (err) {
            console.log(err);
            res.sendStatus(500);
        }
        if (null == data) {
            res.sendStatus(400);
            console.log("Cannot find data with given fileid: " + fileid);
            return;
        }

        res.attachment(data.name);
        s3.getObject({
            Bucket: process.env['NEPTUNE_S3_BUCKET_ID'],
            Key: fileid //data.id
        }).createReadStream().pipe(res);;
    });

};