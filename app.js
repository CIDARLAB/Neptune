var express = require("express");
var path = require('path');
var app = express();
var dotenv = require('dotenv');
dotenv.load();

var mongoose     = require('mongoose');             //MongoDB object modeling tool
var passport     = require('passport');             //Handles users and login
var flash        = require('connect-flash');
var cookieParser = require('cookie-parser');        //Parses cookies
var bodyParser   = require('body-parser');
var session      = require('express-session');      //Handles user sessions
var fs           = require('fs');
var morgan       = require('morgan');

global.Neptune_ROOT_DIR = __dirname;

var configDB = process.env['MONGOURL'];
mongoose.connect(configDB); // connect to our database

// set up our cookies and html information for login
app.use(morgan('dev')); // log every request to the console
app.use(cookieParser()); // read cookies (needed for auth)
app.use(bodyParser.json()); // get information from html forms
app.use(bodyParser.urlencoded({ extended: true }));

// required for passport
app.use(session({ secret: 'iamneptune' })); // session secret
app.use(passport.initialize());
app.use(passport.session()); // persistent login sessions
app.use(flash()); // use connect-flash for flash messages stored in session

require('./controllers/passport.js')(passport); // pass passport for configuration
// load our routes and pass in our app and fully configured passport
// require('./controllers/loginRoutes.js')(app, passport);


//Express app itself
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'hbs');
var hbs = require('hbs');
hbs.registerPartials(__dirname + '/views/partials');

/**************** CONTROLLERS ****************/
{
    var viewsController = require('./controllers/views');
    var writeController = require('./controllers/fileWrite');
    var workspaceController = require('./controllers/workspace');
    var compileMintController = require('./controllers/compileMint');
    var translateLFRController = require('./controllers/translateLFR');
    var AWS_S3_Controller = require('./controllers/AWS_S3');
}

/*********************   VIEWS   *********************/

{
    app.get('/assembly', viewsController.openAssemblyPage);
    app.get('/', viewsController.openHomePage);
    app.get('/build', viewsController.openBuildPage);
    app.get('/dashboard', viewsController.openDashboardPage);
    app.get('/control', viewsController.openControlPage);
    app.get('/specify', viewsController.openSpecifyPage);
    app.get('/design', viewsController.openDesignPage);

        // PROFILE SECTION =========================
        app.get('/profile', isLoggedIn, function(req, res) {
            res.render('profile.ejs', {
                user : req.user
            });
        });

        // LOGOUT ==============================
        app.get('/logout', function(req, res) {
            req.logout();
            res.redirect('/');
        });

        // locally --------------------------------
        // LOGIN ===============================
        // show the login form
        app.get('/login', function(req, res) {
            res.render('login.ejs', { message: req.flash('loginMessage') });
        });

        // process the login form
        app.post('/login', passport.authenticate('local-login', {
            successRedirect : '/profile', // redirect to the secure profile section
            failureRedirect : '/login', // redirect back to the signup page if there is an error
            failureFlash : true // allow flash messages
        }));

        // SIGNUP =================================
        // show the signup form
        app.get('/signup', function(req, res) {
            res.render('signup.ejs', { message: req.flash('signupMessage') });
        });

        // process the signup form
        app.post('/signup', passport.authenticate('local-signup', {
            successRedirect : '/profile', // redirect to the secure profile section
            failureRedirect : '/signup', // redirect back to the signup page if there is an error
            failureFlash : true // allow flash messages
        }));

    }

// route middleware to ensure user is logged in
    function isLoggedIn(req, res, next) {
        if (req.isAuthenticated())
            return next();

        res.redirect('/');
    }

/*************************** FILE WRITE ********************/
{
    app.post('/api/writeToFile',writeController.writeToFile);
}

/************** AMAZON WEB SERVICES S3 FILE STORAGE  ***************/
{
    app.post('/api/Create_Unique_Bucket', AWS_S3_Controller.Create_Unique_Bucket);
    app.post('/api/Delete_Unique_Bucket', AWS_S3_Controller.Delete_Unique_Bucket);
    app.post('/api/Delete_Bucket_Object', AWS_S3_Controller.Delete_Bucket_Object);
    app.post('/api/Create_Bucket_Object', AWS_S3_Controller.Create_Bucket_Object);
    app.post('/api/Get_Bucket_Object'   , AWS_S3_Controller.Get_Bucket_Object);
    app.post('/api/Read_S3_Link'        , AWS_S3_Controller.read_link);
    //app.post('/api/sendToAWS'           , AWS_S3_Controller.sendToAWS);
}

/************** Mongoose DataBase Calls **************/
{
    app.post('/api/Create_User', AWS_S3_Controller.Create_User);
    app.post('/api/Update_User',AWS_S3_Controller.Update_User);
    app.post('/api/Query_User', AWS_S3_Controller.Query_User);
    app.post('/api/Delete_User',AWS_S3_Controller.Delete_User);

    app.post('/api/Create_Workspace', AWS_S3_Controller.Create_Workspace);
    app.post('/api/Update_Workspace',AWS_S3_Controller.Update_Workspace);
    app.post('/api/Query_Workspace', AWS_S3_Controller.Query_Workspace);
    app.post('/api/Delete_Workspace',AWS_S3_Controller.Delete_Workspace);

    app.post('/api/Create_File', AWS_S3_Controller.Create_File);
    //app.post('/api/Update_File',AWS_S3_Controller.Update_File);
    //app.post('/api/Query_File', AWS_S3_Controller.Query_File);
    //app.post('/api/Delete_File',AWS_S3_Controller.Delete_File);
}

/************** Redirects **************/
{
    app.post('/api/redirectToSpecify', AWS_S3_Controller.redirectToSpecify);
}

/**************** USHROOM MAPPER & FLUIGI ****************/
{
    app.post('/api/compileMint', compileMintController.compileMint);
    app.post('/api/translateLFR', translateLFRController.translateLFR);
}

/**************** WORKSPACE INITIATION AND MAINTAINENCE ****************/
{
    app.post('/api/clearFiles', workspaceController.clearFiles);
    app.post('/api/generateUCF', workspaceController.generateUCF);
    app.post('/api/getFile', workspaceController.getFile);
    app.post('/api/download', workspaceController.download);
    app.post('/api/parseDir', workspaceController.parseDir);
    app.post('/api/getProjects', workspaceController.getProjects);
    app.post('/api/makeProject', workspaceController.makeProject);
    app.post('/api/scanFiles', workspaceController.scanFiles);
    app.post('/api/findHome', workspaceController.findHome);
}


/*******************************************************/


app.listen(8080, function(){console.log("Starting application")});