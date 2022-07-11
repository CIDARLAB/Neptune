/**
 * Created by kestas on 4/13/2017.
 */

var mongoose = require('mongoose');
var Schema = mongoose.Schema;
var File = require('../models/file');

var jobSchema = new Schema({
    name: String,
    files: { type: [String], required: false },
    created_at: Date,
    updated_at: Date
});

jobSchema.methods.addName = function createFile(name) {
    this.name = name;
    this.save();
};

jobSchema.methods.prune = function createFile(length) {
    var clean = [];
    for (var i = 0; i < length; i++) {
        clean[i] = this.files[i];
    }
    this.files = clean;
    this.save();
};

jobSchema.methods.createFile = async function createFile(filename, ext, text) {
    var newfile = new File();
    newfile.name = filename;
    newfile.file_extension = ext;
    await newfile.createAndUploadS3File(text)
        .catch(err => {
            console.error("Error creating and saving the s3 file:", err);
            throw err;
        });
    this.files.push(newfile._id);
    console.log('Job model pushing file id to self array: ', newfile._id);
    await this.save()
        .catch(err => {
            console.error("Error updating the job after creating the file:", err);
        });
};

jobSchema.methods.addJobToUser = function addJobToUser(user_id) {

};

jobSchema.pre('save', function(next) {
    this.set("_id", mongoose.Types.ObjectId(this._id), { strict: false });

    // Save date of creation
    var currentDate = new Date(); // Get the current date
    this.updated_at = currentDate; // Change the updated_at field to current date
    if (!this.created_at)
        this.created_at = currentDate; // If created_at doesn't exist, add to that field

    next();

});

var Job = mongoose.model('Job', jobSchema);
module.exports = Job;