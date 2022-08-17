/**
 * Created by kestas on 3/18/2017.
 */

var exports = module.exports;
var express = require("express");
var cmd = require("node-cmd");
var path = require("path");
var mkdirp = require("mkdirp");
var jsonfile = require("jsonfile");
var mongoose = require("mongoose");
var fs = require("fs");
var AWS_S3 = require("./AWS_S3");
var User = require("../models/user");
var Workspace = require("../models/workspace");
var File = require("../models/file");
var Job = require("../models/job");


var s3 = AWS_S3.s3Instance;

exports.Create_User = async function (req, res) {
    var User = require("../models/user");
    var username = req.body.username;
    var password = req.body.password;

    var newUser = User({
        username: username,
        password: password,
    });

    var id_temp;
    // newUser.save(function(err, success) {
    //     id_temp = success.id;
    //     if (err) throw err;
    //     console.log('-- New User Created --');
    //     console.log('Username: %s', username);
    //     console.log('Password: %s', password);
    //     console.log('UniqueId: %s', success.id);
    //     console.log('----------------------');

    //     var User = require('../models/user');
    //     //User.findById(success.id);
    //     // newUser.methods.generateWorkspaces_and_updateSchema(id_temp);
    // });

    await newUser
        .save()
        .then((success) => {
            id_temp = success.id;
            console.log("-- New User Created --");
            console.log("Username: %s", username);
            console.log("Password: %s", password);
            console.log("UniqueId: %s", success.id);
            console.log("----------------------");

            // var User = require('../models/user');
            //User.findById(success.id);
            // newUser.methods.generateWorkspaces_and_updateSchema(id_temp);
            res.send(id_temp);
        })
        .catch((err) => {
            console.error("Error saving the new user:", err);
            throw err;
        });
};

exports.Update_User = function (req, res) {
    var User = require("../models/user");

    var userId = req.body.user_id;
    var update_type = req.body.update_type;
    var update_body = req.body.update;

    console.log(
        "ATTEMPTING TO UPDATE USER w/ ID [%s] BY PUSHING WORKSPACE ID: [%s]",
        userId,
        update_body
    );

    User.findByIdAndUpdate(
        userId,
        {
            $push: { workspaces: update_body },
        },
        { new: true },
        callback
    );

    function callback(err, numAffected) {}

    return 0;
};

exports.Update_User_cs = function (req, res) {
    var User = require("../models/user");

    var userId = req.body.user_id;
    var update_body = req.body.update;

    console.log(
        "ATTEMPTING TO UPDATE USER w/ ID [%s] BY PUSHING WORKSPACE ID: [%s]",
        userId,
        update_body
    );

    User.findByIdAndUpdate(
        userId,
        {
            $push: { workspaces: update_body },
        },
        { new: true },
        callback
    );

    function callback(err, numAffected) {}

    res.sendStatus(200);
};

exports.Query_User = function (req, res) {
    // We can effectively add logic for searching and all else here
    var User = require("../models/user");
    var id = req.body.id;
    var username = req.body.username;
    var lookupType = req.body.lookupType;
    var inquery = req.body.inquery;

    if (lookupType == "Specific") {
        User.find({ username: username }, function (err, user) {
            if (err) throw err;
        });
    } else if (lookupType == "Full") {
        User.find({}, function (err, users) {
            if (err) throw err;
        });
    } else if (lookupType == "Id") {
        var id = req.body.id;
        User.findById(id, function (err, user) {
            if (err) throw err;
            if (inquery == "workspace") {
                console.log("Sending to Client: ", user.workspaces);
                res.send(user.workspaces);
            }
        });
    } else if (lookupType == "Query") {
        var timespan = req.body.timespan;
        switch (timespan) {
            case "day":
                break;
            case "week":
                break;
            case "month":
                timespan.setMonth(timespan.getMonth() - 1);
                // User.find({ admin: true }).where('created_at').gt(monthAgo).exec(function(err, users) {
                //     if (err) throw err;
                //
                //     // show the admins in the past month
                //     console.log(users);
                break;
            case "year":
                break;
        }
    }
};

exports.Delete_User = function (req, res) {
    var user_id = req.body.id;
    var User = require("../models/user");
    User.findByIdAndRemove(user_id, function (err) {
        if (err) throw err;

        console.log("User with id %s deleted!", user_id);
    });
};

exports.getUser = function (req, res) {
    User.findById(req.user._id, function (err, user) {
        if (err) throw err;
        res.send({
            email: user.local.email,
            created_at: user.local.created_at,
            updated_at: user.local.updated_at,
            workspaces: user.workspaces,
            jobs: user.jobs,
        });
    });
};

exports.getWorkspaces = function (req, res) {
    User.findById(req.user._id, function (err, user) {
        if (err) throw err;
        res.send(user.workspaces);
    });
};

exports.getJobs = function (req, res) {
    User.findById(req.user._id, function (err, user) {
        if (err) throw err;
        res.send(user.jobs);
    });
};

exports.getWorkspace = function (req, res) {
    var id = req.query.workspace_id;
    Workspace.findById(id, function (err, workspace) {
        if (err) throw err;
        console.log(workspace);
        res.send({
            name: workspace.name,
            _id: workspace._id.toString(),
            specify_files: workspace.specify_files,
            design_files: workspace.design_files,
            other_files: workspace.other_files,
            created_at: workspace.created_at,
            updated_at: workspace.updated_at,
        });
        // res.send(workspace);
    });
};

exports.Create_Workspace = function (req, res) {
    var userid = req.user._id;
    var workspace_name = req.body.name;
    var Workspace = require("../models/workspace");

    var newWorkspace = Workspace({
        name: workspace_name,
    });

    newWorkspace.save(function (err) {
        if (err) throw err;
        console.log("New Workspace");
        console.log("Workspace Name: %s", workspace_name);
    });

    //newWorkspace.generateFiles_and_updateSchema();
    //TODO: Add the workspace to the current user
    User.findByIdAndUpdate(
        userid,
        { $push: { workspaces: newWorkspace._id } },
        { safe: true, upsert: true },
        function (err, user) {
            if (err) throw err;
        }
    );

    res.sendStatus(200);
};

exports.createWorkspace = function (req, res) {
    var userid = req.user._id;
    console.log("user id: " + userid);
    var workspace_name = req.body.name;
    var Workspace = require("../models/workspace");

    var newWorkspace = Workspace({
        name: workspace_name,
    });

    newWorkspace.save(function (err) {
        if (err) throw err;
        console.log("New Workspace");
        console.log("Workspace Name: %s", workspace_name);
    });

    newWorkspace.generateFiles_and_updateSchema();

    //TODO: Get the current user and add the new workspace to the person's profile get this from the session
    //newWorkspace.generateFiles_and_updateSchema();
    User.findByIdAndUpdate(
        userid,
        { $push: { workspaces: newWorkspace._id } },
        { safe: true, upsert: true },
        function (err, user) {
            if (err) {
                res.sendStatus(500);
                throw err;
            }
        }
    );

    var user = User.findById(userid, function (err, user) {
        if (err) {
            console.err(err);
        }
        console.log(user.workspaces);
    });
    res.send(newWorkspace._id);
};

exports.Query_Workspace = function (req, res) {
    var Workspace = require("../models/workspace");
    var searchFor = req.body.workspace_id;

    var fileSpace = {};
    Workspace.findById(
        "58d514934146a97023e32b26",
        { specify_files: 1, design_files: 1 },
        function (err, workspace) {
            if (err) throw err;
            fileSpace = {
                specify_files: workspace.specify_files,
                design_files: workspace.design_files,
            };
            console.log(fileSpace);
        }
    );

    return fileSpace;
};

exports.Update_Workspace = function (req, res) {
    var workspaceId = req.body.workspace_id;
    var update_body = req.body.update;
    var update_type = req.body.update_type;

    console.log(
        "ATTEMPTING TO UPDATE WORKSPACE w/ ID [%s] BY PUSHING FILE ID: [%s]",
        workspaceId,
        update_body
    );

    switch (update_type) {
        case "add_file_d":
            Workspace.findByIdAndUpdate(
                workspaceId,
                {
                    $push: { design_files: update_body },
                },
                { new: true },
                callback
            );

            break;
        case "add_file_sol":
            Workspace.findByIdAndUpdate(
                workspaceId,
                {
                    $push: { solution_files: update_body },
                },
                { new: true },
                callback
            );
            break;
        case "add_job":
            Workspace.findByIdAndUpdate(
                workspaceId,
                {
                    $push: { jobs: update_body },
                },
                { new: true },
                callback
            );
            break;
    }

    function callback(err, numAffected) {}
    return 0;
};

exports.Delete_Workspace = function (req, res) {
    let userid = req.user._id;
    var workspace_id = req.body.id;
    var Workspace = require("../models/workspace");
    Workspace.findByIdAndRemove(workspace_id, function (err) {
        if (err) throw err;
        console.log("Workspace with id %s deleted!", workspace_id);
        User.findById(userid, async function (err, user) {
            if (err) throw err;
            const index = user.workspaces.indexOf(workspace_id);
            if (index > -1) {
                user.workspaces.splice(index, 1);
            }
            await user.save();
            res.sendStatus(200);
        });
    });
};

exports.createFile = function (req, res) {
    var file_name = req.body.file_name;
    var file_ext = req.body.ext;
    var workspace_id = req.body.workspaceid;

    Workspace.findById(workspace_id, function (err, data) {
        if (err) {
            console.error(err);
            throw err;
        }
        data.createFile(file_name, file_ext);
        res.sendStatus(200);
    });
};

exports.Create_File = function (req, res) {
    var file_name = req.body.file_name;
    var file_ext = req.body.file_ext;

    var File = require("../models/file");

    var newFile = File({
        name: file_name,
        file_extension: file_ext,
    });

    newFile.save(function (err) {
        if (err) throw err;
        console.log("New file model created: %s", file_name);
    });

    newFile.createAndUploadDefaultS3File();
    return newFile._id;
};

exports.Create_File_cs = function (req, res) {
    var file_name = req.body.file_name;
    var file_ext = req.body.ext;

    var File = require("../models/file");

    var newFile = File({
        name: file_name,
        file_extension: file_ext,
    });

    newFile.save(function (err) {
        if (err) throw err;
        console.log("New file model created: %s", file_name);
    });

    newFile.createAndUploadDefaultS3File();
    //TODO: Add file to current workspace , also send the current workspace id when doing this

    res.send(newFile._id);
};

exports.getFiles = function (req, res) {
    var workspaceid = req.query.id;
    if ("" == workspaceid) {
        res.sendStatus(500);
        return;
    }
    Workspace.findById(workspaceid, function (err, data) {
        if (err) {
            console.log(err);
            res.sendStatus(500);
            return;
        }
        if (null == data) {
            res.sendStatus(404);
            return;
        }
        var retarray = [];
        for (var i = 0; i < data.specify_files.length; i++) {
            retarray.push(data.specify_files[i]);
        }
        for (var i = 0; i < data.design_files.length; i++) {
            retarray.push(data.design_files[i]);
        }
        for (var i = 0; i < data.solution_files.length; i++) {
            retarray.push(data.solution_files[i]);
        }
        res.send(retarray);
    });
};

exports.getJobFiles = function (req, res) {
    console.log("TEST1", req.query.id);
    var jobid = req.query.id;
    if ("" == jobid) {
        res.sendStatus(500);
        return;
    }
    Job.findById(jobid, function (err, data) {
        if (err) {
            console.log(err);
            res.sendStatus(500);
            return;
        }
        console.log("TEST2");
        if (null == data) {
            res.sendStatus(404);
            return;
        }
        var retarray = [];
        for (var i = 0; i < data.files.length; i++) {
            retarray.push(data.files[i]);
        }

        console.log(err);
        res.send(retarray);
    });
};

exports.getFile = function (req, res) {
    var fileid = req.query.id;
    if (null == fileid || undefined == fileid || "" === fileid) {
        res.sendStatus(500);
        return;
    }
    console.log("requesting file id: " + fileid);
    File.findById(fileid, function (err, data) {
        if (err) {
            console.log(err);
            res.sendStatus(500);
        }
        if (null == data) {
            res.sendStatus(400);
            console.log("Cannot find data with given fileid: " + fileid);
            return;
        }
        res.send({
            id: data._id,
            name: data.name,
            ext: data.file_extension,
            link: data.S3_path,
            updated_at: data.updated_at,
        });
    });
};

exports.Query_File = function (req, res) {
    var file_id = req.body.file_id;
    var File = require("../models/file");

    File.findById(file_id, function (err, file) {
        console.log("File found");
        console.log(file);
        if (err) throw err;
        return file;

        //res.send(file);
    });
};

exports.updateFile = function (req, res) {
    console.log("Updating the file:");
    console.log("fileid: " + req.body.fileid);
    console.log("name: " + req.body.name);
    console.log("name: " + req.body.text);
    //TODO: Check for file access permissions
    File.findById(req.body.fileid, function (err, data) {
        if (err) {
            console.err(err);
            res.sendStatus(500);
            throw err;
        }
        var Target_Bucket_ID = process.env["AWS_S3_BUCKET_NAME"];
        var Target_Object_KEY = data._id.toString();
        var Target_Object_STREAM = req.body.text;

        var Parameters = {
            Bucket: Target_Bucket_ID,
            Key: Target_Object_KEY,
            Body: Target_Object_STREAM,
        };

        s3.upload(Parameters, function (err, data) {
            if (err) {
                console.log(err);
                res.sendStatus(500);
                throw err;
            } else {
                console.log(data);
                res.sendStatus(200);
            }
        });
    });
};

exports.deleteFile = function (req, res) {
    var workspaceid = req.body.workspaceid;
    var fileid = req.body.fileid;
    console.log("Deleting the file:");
    console.log("workspaceid: " + workspaceid);
    console.log("fileid: " + req.body.fileid);
    if (null == workspaceid) {
        res.sendStatus(400);
        return;
    }
    File.findByIdAndRemove(fileid, function (err, data) {
        if (err) {
            console.err(err);
            res.sendStatus(500);
            throw err;
        }
        //Remove entry in workspace
        Workspace.findById(workspaceid, async function (err, data) {
            if (err) {
                console.err(err);
                res.sendStatus(500);
                throw err;
            }
            var index = data.specify_files.indexOf(fileid);
            if (index > -1) {
                data.specify_files.splice(index, 1);
                console.log("Deleted Specify File");
            }
            var index = data.design_files.indexOf(fileid);
            if (index > -1) {
                data.design_files.splice(index, 1);
                console.log("Deleted design File");
            }
            var index = data.solution_files.indexOf(fileid);
            if (index > -1) {
                data.solution_files.splice(index, 1);
                console.log("Deleted solution File");
            }
            await data.save();
            res.sendStatus(200);
        });
    });
};

exports.Update_File = function (req, res) {
    var fileId = req.body.id;

    File.findById(fileId, function (err, file) {
        if (err) throw err;
        var update_type = req.body.update_type;
        var update_body = req.body.update_body;
        switch (update_type) {
            case "name":
                file.name = update_body;
                break;
            case "body":
                break;
        }
    });
};

exports.Delete_File = function (req, res) {
    var fileId = req.body.id;
    var File = require("../models/file");

    File.findById(fileId, function (err, file) {
        if (err) throw err;
        var update_type = req.body.update_type;
        var update_body = req.body.update_body;
        switch (update_type) {
            case "name":
                file.name = update_body;
                break;
            case "body":
                break;
        }
    });
};

exports.Create_Job = function (user_id) {
    var Job = require("../models/job");

    var newJob = Job();

    newJob.save(function (err) {
        if (err) throw err;
        console.log("New job model created: %s", newJob._id);
    });

    //newJob.addJobToUser(user_id);
    return newJob._id;
};

exports.Update_Job = function (parameters) {
    var job_id = parameters.job_id;
    var update_body = parameters.update_body;
    var update_type = parameters.update_type;

    console.log(
        "ATTEMPTING TO UPDATE JOB w/ ID [%s] BY PUSHING FILE ID: [%s]",
        job_id,
        update_body
    );

    switch (update_type) {
        case "add_file_svg":
            Job.findByIdAndUpdate(
                job_id,
                {
                    $push: { svg_files: update_body },
                },
                { new: true },
                callback
            );

            break;
        case "add_file_eps":
            Job.findByIdAndUpdate(
                job_id,
                {
                    $push: { eps_files: update_body },
                },
                { new: true },
                callback
            );
            break;
        case "add_file_other":
            Job.findByIdAndUpdate(
                job_id,
                {
                    $push: { other_files: update_body },
                },
                { new: true },
                callback
            );
            break;
    }

    function callback(err, numAffected) {}
    return 0;
};

exports.getJob = function (req, res) {
    var id = req.query.job_id;
    Job.findById(id, function (err, job) {
        if (err) throw err;
        console.log(job);
        res.send({
            name: job.name,
            id: job._id,
            created_at: job.created_at,
            updated_at: job.updated_at,
            files: job.files,
        });
    });
};
