var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var AWS_S3 = require('../controllers/AWS_S3');
var fs = require('fs');
var path = require('path');

var s3 = AWS_S3.s3Instance;

var fileSchema = new Schema({
    name: String,
    S3_path: String,
    file_extension: String,
    created_at: Date,
    updated_at: Date
});

fileSchema.methods.createAndUploadDefaultS3File = function createS3File_and_linkToMongoDB(type) {
    var dateFormat = require('dateformat');
    var now = new Date();
    var timeStamp = dateFormat(now, "dddd, mmmm dS, yyyy, h:MM:ss TT");
    var text = '';
    var me = this;

    if (type === 'lfr') {
        fs.readFile(path.join(global.Neptune_ROOT_DIR, 'content', 'sample.lfr'), function (err, data) {
            if (err) console.log(err);
            text = data;
            var Target_BUCKET_ID = process.env['AWS_S3_BUCKET_NAME'];
            var Target_Object_KEY = me._id.toString();
            var Target_Object_BODY = text;

            var Parameters = {
                Bucket: Target_BUCKET_ID,
                Key: Target_Object_KEY,
                Body: Target_Object_BODY,
                ACL: "public-read"
            };
            s3.upload(Parameters, function (err, data) {
                if (err) { console.log(err); throw err; } else {
                    me.S3_path = data.Location;
                    me.save();
                    console.log("updated file path: " + me.S3_path);
                }
            });
        });
    } else if (type === 'ucf') {
        fs.readFile(path.join(global.Neptune_ROOT_DIR, 'content', 'ucf.json'), function (err, data) {
            if (err) console.log(err);
            text = data;
            var Target_BUCKET_ID = process.env['AWS_S3_BUCKET_NAME'];
            var Target_Object_KEY = me._id.toString();
            var Target_Object_BODY = text;

            var Parameters = {
                Bucket: Target_BUCKET_ID,
                Key: Target_Object_KEY,
                Body: Target_Object_BODY,
                ACL: "public-read"
            };
            s3.upload(Parameters, function (err, data) {
                if (err) { console.log(err); throw err; } else {
                    me.S3_path = data.Location;
                    me.save();
                    console.log("updated file path: " + me.S3_path);
                }
            });
        });
    } else if (type === 'mint') {
        fs.readFile(path.join(global.Neptune_ROOT_DIR, 'content', 'sample.uf'), function (err, data) {
            if (err) console.log(err);
            text = data;
            var Target_BUCKET_ID = process.env['AWS_S3_BUCKET_NAME'];
            var Target_Object_KEY = me._id.toString();
            var Target_Object_BODY = text;

            var Parameters = {
                Bucket: Target_BUCKET_ID,
                Key: Target_Object_KEY,
                Body: Target_Object_BODY,
                ACL: "public-read"
            };
            s3.upload(Parameters, function (err, data) {
                if (err) { console.log(err); throw err; } else {
                    me.S3_path = data.Location;
                    me.save();
                    console.log("updated file path: " + me.S3_path);
                }
            });
        });
    } else if (type === 'ini') {
        fs.readFile(path.join(global.Neptune_ROOT_DIR, 'content', 'config.ini'), function (err, data) {
            if (err) console.log(err);
            text = data;
            var Target_BUCKET_ID = process.env['AWS_S3_BUCKET_NAME'];
            var Target_Object_KEY = me._id.toString();
            var Target_Object_BODY = text;

            var Parameters = {
                Bucket: Target_BUCKET_ID,
                Key: Target_Object_KEY,
                Body: Target_Object_BODY,
                ACL: "public-read"
            };
            s3.upload(Parameters, function (err, data) {
                if (err) { console.log(err); throw err; } else {
                    me.S3_path = data.Location;
                    me.save();
                    console.log("updated file path: " + me.S3_path);
                }
            });
        });
    } else {

        text = '// Created By:__________ \n// Created On: ' + timeStamp;
        var Target_BUCKET_ID = process.env['AWS_S3_BUCKET_NAME'];
        var Target_Object_KEY = me._id.toString();
        var Target_Object_BODY = text;

        var Parameters = {
            Bucket: Target_BUCKET_ID,
            Key: Target_Object_KEY,
            Body: Target_Object_BODY,
            ACL: "public-read"
        };
        s3.upload(Parameters, function (err, data) {
            if (err) { console.log(err); throw err; } else {
                me.S3_path = data.Location;
                me.save();
                console.log("updated file path: " + me.S3_path);
            }
        });
    }

};

fileSchema.methods.createAndUploadEmptyS3File = function createS3File_and_linkToMongoDB() {
    var dateFormat = require('dateformat');
    var now = new Date();
    var timeStamp = dateFormat(now, "dddd, mmmm dS, yyyy, h:MM:ss TT");
    var text = '// Created By:__________ \n// Created On: ' + timeStamp;

    var Target_BUCKET_ID = process.env['AWS_S3_BUCKET_NAME'];
    var Target_Object_KEY = this._id.toString();
    var Target_Object_BODY = text;
    console.log("Bucket key:" + Target_BUCKET_ID);

    var Parameters = {
        Bucket: Target_BUCKET_ID,
        Key: Target_Object_KEY,
        Body: Target_Object_BODY,
        ACL: "public-read"
    };
    var me = this;
    s3.upload(Parameters, function(err, data) {
        if (err) { console.log(err); throw err; } else {
            me.S3_path = data.Location;
            me.save();
            console.log("updated file path: " + me.S3_path);
        }
    });
};


fileSchema.methods.createAndUploadS3File = async function createAndUploadS3File(text) {

    var Target_BUCKET_ID = process.env['AWS_S3_BUCKET_NAME'];
    var Target_Object_KEY = this._id.toString();

    //TODO:This is a shitty fix incase there is no text present, this should be more elegant
    if ("" == text) {
        text = "null";
    }

    var Parameters = {
        Bucket: Target_BUCKET_ID,
        Key: Target_Object_KEY,
        Body: text,
        ACL: "public-read"
    };

    var me = this;

    s3.upload(Parameters, function(err, data) {
        if (err) { console.log(err); throw err; } else {
            me.S3_path = data.Location;
            me.save();
            console.log("Uploaded non-default file to file path: " + me.S3_path);
        }
    });

}

fileSchema.methods.updateS3File = function updateS3File() {
    var AWS_S3 = require('../controllers/AWS_S3');
    var body = { body: { Target_Bucket_ID: 'neptune.primary.fs', Target_Object_KEY: this.id, Target_Object_BODY: 'edit me :)\n\nexample body' } };
    AWS_S3.Create_Bucket_Object(body, function(S3_path) {
        this.S3_path = S3_path.ETag;
    });
};

fileSchema.pre('save', function(next) {
    this.set("_id", mongoose.Types.ObjectId(this._id), { strict: false });

    // Save date of creation
    var currentDate = new Date(); // Get the current date
    this.updated_at = currentDate; // Change the updated_at field to current date
    if (!this.created_at)
        this.created_at = currentDate; // If created_at doesn't exist, add to that field

    next();

});

var File = mongoose.model('File', fileSchema);
module.exports = File;



// s3.getSignedUrl('putObject',Parameters, function(err, url) {
//     if (err) {
//         console.log(err)
//     } else {
//         me.S3_path = url;
//         me.save();
//     }
// });

// s3.putObject(Parameters, function(err, data) {
//     if (err) {
//         console.log(err)
//     } else {
//         me.S3_path = data.ETag;
//         me.save();
//     }
// });
//var body = {body:{Target_Bucket_ID:'neptune.primary.fs', Target_Object_KEY: this._id.toString(), Target_Object_BODY:message}};
// var s3_path = AWS_S3.Create_Bucket_Object(body,function(S3_path)
// {
//     this.S3_path = S3_path.ETag;
//     this.save();
// });