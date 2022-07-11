/**
 * Communication between AWS EC2 instance and S3
 */

var exports = module.exports;
const path = require("path");
const fs = require("fs");
//var s3s         = require('s3-streams');
const AWS = require("aws-sdk");
const db = require("./databaseInterface");
const Job = require("../models/job");
const User = require("../models/user");

AWS.config.update({
    accessKeyId: process.env["NEPTUNE_AWSID"],
    secretAccessKey: process.env["NEPTUNE_AWSKEY"],
});
const Target_BUCKET_ID = process.env["NEPTUNE_S3_BUCKET_ID"];

const s3 = new AWS.S3();

/*
 Amazon Web Services Management Exports
 */
exports.Create_Bucket_Object = function (file, text) {
    var Target_Object_KEY = file._id.toString();
    var Target_Object_BODY = text;
    var Parameters = {
        Bucket: Target_BUCKET_ID,
        Key: Target_Object_KEY,
        Body: Target_Object_BODY,
        ACL: "public-read",
    };

    s3.upload(Parameters, async function (err, data) {
        if (err) console.log(err);
        else {
            file.S3_path = data.Location;
            await file.save();
        }
    });
};
exports.Read_Bucket_Object = function (req, res) {
    var Target_Bucket_ID = process.env["NEPTUNE_S3_BUCKET_ID"];
    var Target_Object_KEY = req.body.Target_Object_KEY;
    var Parameters = {
        Bucket: Target_Bucket_ID,
        Key: Target_Object_KEY,
        ResponseContentEncoding: "utf-8",
        ResponseContentType: "string/utf-8",
    };
    s3.getObject(Parameters, function (error, data) {
        var fd = fs.openSync("response.txt", "w+");
        fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
        fs.closeSync(fd);

        var readStream = fs.createReadStream("response.txt");
        readStream.on("open", function () {
            readStream.pipe(res);
        });
        //fd.pipe(res);
        //res.send(data);
    });

    // var path = req.body.path;
    // console.log(path);
    // var readStream = fs.createReadStream(path);
    // readStream.on('open',function()
    // {
    //     //readStream.pipe(res);
    // });

    // var Target_Bucket_ID = 'neptune.primary.fs';
    // var Target_Object_KEY = req.body.Target_Object_KEY;
    // var download = s3s.ReadStream(new AWS.S3(), {
    //     Bucket: Target_Bucket_ID,
    //     Key: Target_Object_KEY
    // });
    // console.log(download);
    // res.send(download);
};
exports.Update_Bucket_Object = function (req, res) {
    var Target_Bucket_ID = process.env["NEPTUNE_S3_BUCKET_ID"]; //req.body.Target_Bucket_ID;
    var Target_Object_KEY = req.body.Target_Object_KEY;
    var Target_Object_STREAM = req.body.Target_Object_STREAM;

    var Parameters = {
        Bucket: Target_Bucket_ID,
        Key: Target_Object_KEY,
        Body: Target_Object_STREAM,
    };

    s3.upload(Parameters, function (err, data) {
        if (err) {
            console.log(err);
        } else {
            console.log(data);
            //res.send(data);
            return data;
        }
    });
};
exports.Delete_Bucket_Object = function (req, res) {
    var Target_Bucket_ID = req.body.Target_Bucket_ID;
    var Target_Object_KEY = req.body.Target_Object_KEY;
    var Parameters = {
        Bucket: Target_Bucket_ID,
        Delete: {
            Objects: [
                {
                    Key: Target_Object_KEY,
                },
            ],
        },
    };
    s3.deleteObjects(Parameters, function (err, data) {
        if (err) console.log(err, err.stack);
        else console.log(data);
    });
};

exports.preCompileFileTransfer = function (req, res) {
    var Target_Bucket_ID = process.env["NEPTUNE_S3_BUCKET_ID"];

    var transferType = req.body.transferType;
    switch (transferType) {
        case "lfr":
            var lfrpath = req.body.job;
            var ucfpath = req.body.config;

            var Parameters_lfr = {
                Bucket: Target_Bucket_ID,
                Key: lfrpath,
                ResponseContentEncoding: "utf-8",
                ResponseContentType: "string/utf-8",
            };
            var Parameters_ucf = {
                Bucket: Target_Bucket_ID,
                Key: ucfpath,
                ResponseContentEncoding: "utf-8",
                ResponseContentType: "string/utf-8",
            };
            var path1 = path.join(global.Neptune_ROOT_DIR, "jobs", "job.txt");
            s3.getObject(Parameters_lfr, function (error, data) {
                var fd = fs.openSync(path1, "w+");
                fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
                fs.closeSync(fd);
            });
            var path2 = path.join(
                global.Neptune_ROOT_DIR,
                "jobs",
                "config.txt"
            );
            s3.getObject(Parameters_ucf, function (error, data) {
                var fd = fs.openSync(path2, "w+");
                fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
                fs.closeSync(fd);
            });
            res.send("Done");
            break;
        case "mint":
            var mintpath = req.body.job;
            var inipath = req.body.config;

            var Parameters_mint = {
                Bucket: Target_Bucket_ID,
                Key: mintpath,
                ResponseContentEncoding: "utf-8",
                ResponseContentType: "string/utf-8",
            };
            var Parameters_ini = {
                Bucket: Target_Bucket_ID,
                Key: inipath,
                ResponseContentEncoding: "utf-8",
                ResponseContentType: "string/utf-8",
            };
            var path1 = path.join(global.Neptune_ROOT_DIR, "jobs", "job.uf");
            s3.getObject(Parameters_mint, function (error, data) {
                var fd = fs.openSync(path1, "w+");
                fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
                fs.closeSync(fd);
            });
            var path2 = path.join(
                global.Neptune_ROOT_DIR,
                "jobs",
                "config.ini"
            );
            s3.getObject(Parameters_ini, function (error, data) {
                var fd = fs.openSync(path2, "w+");
                fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
                fs.closeSync(fd);
            });
            res.send("Done");
            break;
    }
};

exports.preMMFileTransfer = async function (req, res, next) {
    var Target_Bucket_ID = process.env["NEPTUNE_S3_BUCKET_ID"];

    var lfrpath = req.body.sourcefileid;
    var configpath = req.body.configfileid;
    var lfrname = req.body.sourcefilename;
    var configname = req.body.configfilename;
    var workspace_id = req.body.workspace;
    var email = req.body.user;

    var Parameters_lfr = {
        Bucket: Target_Bucket_ID,
        Key: lfrpath,
        ResponseContentEncoding: "utf-8",
        ResponseContentType: "string/utf-8",
    };
    var Parameters_ucf = {
        Bucket: Target_Bucket_ID,
        Key: configpath,
        ResponseContentEncoding: "utf-8",
        ResponseContentType: "string/utf-8",
    };

    var newJob = new Job();

    var date = new Date();
    var nameid =
        date.getFullYear() +
        "-" +
        (date.getMonth() + 1) +
        "-" +
        date.getDate() +
        " " +
        date.getHours() +
        ":" +
        date.getMinutes() +
        ":" +
        date.getSeconds();
    var jobname = "pyLFR_job_" + nameid;
    newJob.name = jobname;
    await newJob.save();
    req.body.jobid = newJob._id.toString();

    User.findOneAndUpdate(
        {
            "local.email": email,
        },
        {
            $push: { jobs: newJob._id },
        },
        {
            new: true,
        },
        function (err, user) {
            if (err) {
                console.error(err);
                throw err;
            }
            console.log("FOUND and updated THE USER...");
        }
    );

    var jobdir = "./jobs/tmp__" + newJob._id;

    var update = {
        body: {
            workspace_id: workspace_id,
            update: newJob._id,
            update_type: "add_job",
        },
    };
    db.Update_Workspace(update);

    if (!fs.existsSync(jobdir)) {
        fs.mkdirSync(jobdir);
    } else {
        console.log("ERROR: Unique Dir Already Exists!");
    }

    var path1 = path.join(global.Neptune_ROOT_DIR, jobdir, lfrname);
    s3.getObject(Parameters_lfr, function (error, data) {
        var fd = fs.openSync(path1, "w+");
        fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
        fs.closeSync(fd);

        var path2 = path.join(global.Neptune_ROOT_DIR, jobdir, configname);
        s3.getObject(Parameters_ucf, function (error, data) {
            var fd = fs.openSync(path2, "w+");
            fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
            fs.closeSync(fd);

            req.body.jobdir = jobdir;
            req.body.jobname = jobname;
            next();
        });
    });
};
exports.preFluigiFileTransfer = async function (req, res, next) {
    var Target_Bucket_ID = process.env["NEPTUNE_S3_BUCKET_ID"];

    var mintpath = req.body.sourcefileid;
    var inipath = req.body.configfileid;
    var mintname = req.body.sourcefilename;
    var ininame = req.body.configfilename;
    var workspace_id = req.body.workspace;
    var email = req.body.user;
    console.log("EMAIL:", email);

    var Parameters_mint = {
        Bucket: Target_Bucket_ID,
        Key: mintpath,
        ResponseContentEncoding: "utf-8",
        ResponseContentType: "string/utf-8",
    };
    var Parameters_ini = {
        Bucket: Target_Bucket_ID,
        Key: inipath,
        ResponseContentEncoding: "utf-8",
        ResponseContentType: "string/utf-8",
    };

    // Created job model, and updates user with id of new object.
    var newJob = new Job();
    var date = new Date();
    var nameid =
        date.getFullYear() +
        "-" +
        (date.getMonth() + 1) +
        "-" +
        date.getDate() +
        " " +
        date.getHours() +
        ":" +
        date.getMinutes() +
        ":" +
        date.getSeconds();
    var jobname = "pyLFR_job_" + nameid;
    newJob.name = jobname;
    await newJob.save();
    req.body.jobid = newJob._id.toString();

    User.findOneAndUpdate(
        {
            "local.email": email,
        },
        {
            $push: { jobs: newJob._id },
        },
        {
            new: true,
        },
        function (err, user) {
            if (err) {
                console.error(err);
                throw err;
            }
            console.log("FOUND and updated THE USER...");
        }
    );

    var jobdir = "./jobs/tmp__" + newJob._id;
    console.log("Directory that is being created:", jobdir);

    var update = {
        body: {
            workspace_id: workspace_id,
            update: newJob._id,
            update_type: "add_job",
        },
    };
    db.Update_Workspace(update);

    if (!fs.existsSync(jobdir)) {
        fs.mkdirSync(jobdir);
    } else {
        console.log("ERROR: Unique Dir Already Exists!");
    }

    var path1 = path.join(global.Neptune_ROOT_DIR, jobdir, mintname);
    s3.getObject(Parameters_mint, function (error, data) {
        var fd = fs.openSync(path1, "w+");
        fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
        fs.closeSync(fd);

        var path2 = path.join(global.Neptune_ROOT_DIR, jobdir, ininame);
        s3.getObject(Parameters_ini, function (error, data) {
            var fd = fs.openSync(path2, "w+");
            fs.writeSync(fd, data.Body, 0, data.Body.length, 0);
            fs.closeSync(fd);

            req.body.jobdir = jobdir;
            req.body.jobname = jobname;
            next();
        });
    });
};

exports.getS3Text = function (req, res) {
    var Target_BUCKET_ID = process.env["NEPTUNE_S3_BUCKET_ID"];
    var Target_Object_KEY = req.query.id;
    var Parameters = {
        Bucket: Target_BUCKET_ID,
        Key: Target_Object_KEY,
        ResponseContentEncoding: "utf-8",
        ResponseContentType: "string/utf-8",
    };
    s3.getObject(Parameters, function (err, data) {
        if (err) {
            console.err(err);
            res.send(500);
            throw err;
        }
        res.send(data.Body);
    });
};

exports.redirectToSpecify = function (req, res) {
    res.redirect("../Specify");
};
