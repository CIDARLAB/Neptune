var mongoose = require("mongoose");
var bcrypt = require("bcrypt-nodejs");
var Schema = mongoose.Schema;

var userSchema = new Schema({
    local: {
        email: String,
        password: String,
        created_at: Date,
        updated_at: Date,
    },
    workspaces: { type: [String], required: false },
    jobs: { type: [String], required: false },
});

userSchema.methods.generateHash = function (password) {
    return bcrypt.hashSync(password, bcrypt.genSaltSync(8), null);
};

userSchema.methods.validPassword = function (password) {
    return bcrypt.compareSync(password, this.local.password);
};

userSchema.methods.generateWorkspaces_and_updateSchema = async function generateWorkspaces_and_updateSchema(
    user
) {
    var Workspace = require("../models/workspace");

    var defaultworkspace = new Workspace();
    defaultworkspace.name = "Default";
    await defaultworkspace.save();
    defaultworkspace.generateEmptyFiles_and_updateSchema(defaultworkspace);
    user.workspaces.push(defaultworkspace._id);

    var microfluidicexamples = new Workspace();
    microfluidicexamples.name = "Microfluidic Examples";
    await microfluidicexamples.save();
    microfluidicexamples.generateFiles_and_updateSchema(microfluidicexamples);
    user.workspaces.push(microfluidicexamples._id);

    await user.save().catch((err) => {
        console.error(
            "Error generating workspaces and updating the schema:",
            err
        );
    });
};

userSchema.methods.createJob = async function createJob(next) {
    var Job = require("./job");
    // Created job model, and updates user with id of new object.
    var newJob = new Job();
    newJob.name = "";
    await newJob.save();
    this.jobs.push(newJob._id.toString());
    this.save();
    console.log("XUSER JOBS", this.jobs.toString());
    next(newJob._id);
};

userSchema.pre("save", function (next) {
    this.set("_id", mongoose.Types.ObjectId(this._id), { strict: false });

    // Save date of creation
    var currentDate = new Date(); // Get the current date
    this.updated_at = currentDate; // Change the updated_at field to current date
    if (!this.created_at) this.created_at = currentDate; // If created_at doesn't exist, add to that field

    next();
});

var User = mongoose.model("User", userSchema);
module.exports = User;
