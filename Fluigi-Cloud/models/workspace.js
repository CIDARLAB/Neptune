var mongoose = require("mongoose");
var Schema = mongoose.Schema;
var File = require("../models/file");

var workspaceSchema = new Schema({
    name: String,
    specify_files: { type: [String], required: false },
    design_files: { type: [String], required: false },
    solution_files: { type: [String], required: false },
    other_files: { type: [String], required: false },
    created_at: Date,
    updated_at: Date,
});

workspaceSchema.methods.createFile = async function createFile(filename, ext) {
    var newfile = new File();
    newfile.name = filename;
    newfile.file_extension = ext;
    await newfile.save();
    newfile.createAndUploadDefaultS3File();
    // this.update({$push:{specify_files: newfile._id}},{'new':true});
    this.specify_files.push(newfile.id);
    this.markModified("specify_files");
    // switch (ext) {
    //     case ".v":
    //         this.specify_files.push(newfile._id);
    //         break;
    //     case ".uf":
    //         this.design_files.push(newfile._id);
    //         break;
    //     case ".ini":
    //         this.design_files.push(newfile._id);
    //         break;
    //     case ".json":
    //         this.specify_files.push(newfile._id);
    //         break;
    //     default:
    //         this.other_files.push(newfile._id);
    // }
    await this.save(function (err) {
        console.log(err);
    });
    console.log("Workspace model pushing fileid to file array: ", newfile._id);
};

workspaceSchema.methods.generateFiles_and_updateSchema = async function generateFiles_and_updateSchema() {
    var newfile = new File();
    newfile.name = "LFR_example.lfr";
    newfile.file_extension = ".lfr";
    await newfile.save();
    newfile.createAndUploadDefaultS3File("lfr");
    this.specify_files.push(newfile._id);

    var newfile = new File();
    newfile.name = "UCF_example.json";
    newfile.file_extension = ".json";
    await newfile.save();
    await newfile.createAndUploadDefaultS3File("ucf");
    this.specify_files.push(newfile._id);

    var newfile = new File();
    newfile.name = "MINT_example.uf";
    newfile.file_extension = ".uf";
    await newfile.save();
    await newfile.createAndUploadDefaultS3File("mint");
    this.design_files.push(newfile._id.toString());

    var newfile = new File();
    newfile.name = "CONFIG_example.ini";
    newfile.file_extension = ".ini";
    await newfile.save();
    await newfile.createAndUploadDefaultS3File("ini");
    this.design_files.push(newfile._id);

    await this.save();
};

workspaceSchema.methods.generateEmptyFiles_and_updateSchema = async function generateFiles_and_updateSchema() {
    var newfile = new File();
    newfile.name = "new_LFR.lfr";
    newfile.file_extension = ".lfr";
    await newfile.save();
    newfile.createAndUploadEmptyS3File();
    this.specify_files.push(newfile._id);

    var newfile = new File();
    newfile.name = "new_UCF.json";
    newfile.file_extension = ".json";
    await newfile.save();
    newfile.createAndUploadEmptyS3File();
    this.specify_files.push(newfile._id);

    var newfile = new File();
    newfile.name = "new_MINT.mint";
    newfile.file_extension = ".mint";
    await newfile.save();
    newfile.createAndUploadEmptyS3File();
    this.design_files.push(newfile._id.toString());

    var newfile = new File();
    newfile.name = "new_Config.ini";
    newfile.file_extension = ".ini";
    await newfile.save();
    await newfile.createAndUploadEmptyS3File();
    this.design_files.push(newfile._id);

    await this.save();
};

workspaceSchema.pre("save", function (next) {
    this.set("_id", mongoose.Types.ObjectId(this._id), { strict: false });

    // Save date of creation
    var currentDate = new Date(); // Get the current date
    this.updated_at = currentDate; // Change the updated_at field to current date
    if (!this.created_at) this.created_at = currentDate; // If created_at doesn't exist, add to that field

    next();
});

var Workspace = mongoose.model("Workspace", workspaceSchema);
module.exports = Workspace;

/* Notes, Memos, And Deprecated Code */
/*
// var body ={body:{file_name:'myLFR.v',file_ext:'.v'}};
// databaseInterface.Create_File(body,function(file_id){
//     this.specify_files.push(file_id);
// });
// var body ={body:{file_name:'defaultUCF.JSON',file_ext:'.JSON'}};
// databaseInterface.Create_File(body,function(file_id){
//     this.specify_files.push(file_id);
// });
// var body ={body:{file_name:'myMINT.mint',file_ext:'.mint'}};
// databaseInterface.Create_File(body,function(file_id){
//     this.specify_files.push(file_id);
// });
// var body ={body:{file_name:'defaultConfig.ini',file_ext:'.ini'}};
// databaseInterface.Create_File(body,function(file_id){
//     this.specify_files.push(file_id);
// });



*/
