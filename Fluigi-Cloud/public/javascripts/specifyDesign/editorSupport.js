/*
 Editor Support . JS
 Function Directory

 Function                    Order
 ---------------------------------
 changeSpecifyTabs()             1
 changeDesignTabs()              2
 saveEditorContent()             3
 pre_pushFileToEditor()          4
 pushFileToEditor()              5
 fill_editor()                   6
 translateLFR()                  7
 compileMINT()                   8
 generateUCF_UI()                9
 generateUCF()                   10
 loadPreviousProject()           11
 nameProject()                   12
 baseName()                      13
 color_ui()                      14

 This file holds all functions related to the editor and its function.
 */


localStorage.JOB       = 'mint.uf';                  // Working Set Job File
localStorage.CONFIG     = 'config.ini';             // Working Set Config File


// function initiate_LocalStorage()
// {
//     $.get('api/v1/workspaces',function (workspace_list)
//     {
//         localStorage.WORKSPACE = workspace_list[0];
//     })
// }
//
// function stage_job(job_id)
// {
//     localStorage.JOB = job_id;
// }
//
// function stage_config_and_execute(config_id,editor,session)
// {
//     localStorage.CONFIG = config_id;
//     dojob(editor,session,localStorage.jobType)
// }
//
// function newFile_cs(workspace_id)
// {
//     var filename = (document.getElementById('setfile_in').value);
//     var fileext  = (document.getElementById('setext_in').value);
//     var fileName = filename + fileext;
//     $.post('/api/Create_File_cs',{file_name: fileName, ext: fileext},function(file_id)
//     {
//         //TODO: update the files that are shown
//         $.get('/api/v1/files',{workspaceid: workspace_id},function (response) {
//            console.log(response);
//         });
//      });
// }

// function newWorkspace_cs()
// {
//     var workspace_name = (document.getElementById('setwrk_in').value);
//     $.post('/api/v1/workspace',
//         {
//             name: workspace_name
//         },
//         function(workspace_id)
//     {
//         console.log("Created Workspace: " + workspace_id);
//         console.log("Getting all the new workspaces :"  );
//         $.get('api/v1/workspaces',function (response) {
//             console.log(response);
//         })
//         //TODO update the user and workspace models
//         // $.post('/api/Update_User_cs',{user_id: user_id,update:workspace_id},function(data){
//         //     $.post('/api/partials_FileNavBar',{workspace_id:localStorage.WORKSPACE},function(html)
//         //     {
//         //         $("#filehbs").html(html)
//         //     });
//         //     $.post('/api/partials_WorkspaceNavBar',{user_id:localStorage.USER},function(html)
//         //     {
//         //         $("#workhbs").html(html)
//         //     });
//         //     $.post('/api/partials_JobSelect',{workspace_id:localStorage.WORKSPACE},function(html)
//         //     {
//         //         $("#compileModal").html(html)
//         //     });
//         // });
//     });
// }

// function loadFile(id)
// {
//     localStorage.FILE = id;
//    $('#selectConfig').modal('show');
// }
//
// function loadConfigFile(id)
// {
//     localStorage.CONFIG = id;
//     dojob(EDITOR.editor, EDITOR.session, localStorage.jobType);
// }
//
// function loadToEditor(id,editor,session,name)
// {
//     localStorage.FILE = id;
//     localStorage.FILE_NAME = name;
//     document.getElementById('filename').innerText = 'File Name: ' + localStorage.FILE_NAME;
//     $.post('/api/Read_Bucket_Object', {Target_Object_KEY: id}, function (data)
//     {
//         session.setValue(data);
//     });
// }

// function changeWorkspace(id,name)
// {
//     localStorage.WORKSPACE = id;
//     localStorage.WORKSPACE_NAME = name;
//     document.getElementById('workspacename').innerText = 'Inside Workspace: ' + localStorage.WORKSPACE_NAME;
//     $.post('/api/partials_FileNavBar',{workspace_id:localStorage.WORKSPACE},function(html)
//     {
//         $("#filehbs").html(html);
//         $.post('/api/partials_JobSelect',{workspace_id:localStorage.WORKSPACE},function(html)
//         {
//             $("#compileModal").html(html)
//         });
//     });
// }

// function initializeEditor()
// {
//     var editor_specify = ace.edit("editor_specify");
//     editor_specify.setTheme("ace/theme/crimson_editor");
//     editor_specify.setOptions({
//         fontFamily: "monospace",
//         fontSize: "12pt"
//     });
//     var MainSession = ace.createEditSession('MainSession', "ace/mode/verilog");
//     editor_specify.setSession(MainSession);
//
//     EDITOR = {editor: editor_specify, session: MainSession};
//     return EDITOR;
// }

function save(editor,session)
{
    var data = session.getValue();
    $.post('/api/Update_Bucket_Object', {Target_Object_KEY:localStorage.FILE,Target_Object_STREAM:data}, function(data) {});
}

// function dojob(editor,session,jobtype)
// {
//     save(editor,session);
//     switch (jobtype)
//     {
//         case 'lfr':
//             $.post('/api/preCompileFileTransfer',{transferType:'lfr',job:'lfr.v',config:'ucf.json'},function(data){
//                 $.post('/api/translate',{workspace: '58e05a0d1590c21a0cc16060'});
//             });
//             break;
//         case 'mint':
//             $.post('/api/preCompileFileTransfer',{transferType:'mint',job:'mint.uf',config:'config.ini'},function(data){
//                 $.post('/api/compile',{workspace: '58e05a0d1590c21a0cc16060'});
//             });
//             break;
//
//     }
// }


// function fill_editor(File_To_Fill_Editor_With,Editor_To_Fill,session)
// {
//     // Clear Editor before adding our file
//     Editor_To_Fill.setSession(session);
//     Editor_To_Fill.session.setValue('');
//
//     // We'll fill the editor line-by-line, so we needa know how many lines we're adding
//     var file_size = File_To_Fill_Editor_With.length;
//
//
//     for (var i = 0; i < file_size; i++)
//     {
//         Editor_To_Fill.session.replace({
//             start: {row: i, column: 0},
//             end: {row: i, column: Number.MAX_VALUE}
//         }, File_To_Fill_Editor_With[i] + '\n')
//     }
// }
//
// function newFile(filetype)
// {
//     var filename = (document.getElementById('new_file_name').value);
//     console.log(filename);
//     switch (filetype)
//     {
//         case 'LFR':
//             $.post("/api/Create_Bucket_Object",{Target_Bucket_ID:'neptune.primary.fs',Target_Bucket_KEY:filename,Target_Bucket_BODY:'New LFR'});
//             break;
//         case 'UCF':
//             $.post("/api/Create_Bucket_Object",{Target_Bucket_ID:'neptune.primary.fs',Target_Bucket_KEY:filename,Target_Bucket_BODY:'New UCF'});
//             break;
//         case 'MINT':
//             $.post("/api/Create_Bucket_Object",{Target_Bucket_ID:'neptune.primary.fs',Target_Bucket_KEY:filename,Target_Bucket_BODY:'New MINT'});
//             break;
//         case 'INI':
//             $.post("/api/Create_Bucket_Object",{Target_Bucket_ID:'neptune.primary.fs',Target_Bucket_KEY:filename,Target_Bucket_BODY:'New INI'});
//             break;
//     }
// }
//
// function queryWorkspace(workspace_id)
// {
//     $.post('/api/queryWorkspace',{workspace_id:workspace_id},function(workspace){
//         var workspace_json = workspace.design_files;
//         console.log(workspace_json);
//     });
//
//}