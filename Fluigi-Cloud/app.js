const express = require("express");
const AWS = require("aws-sdk");
const path = require("path");
const history = require("connect-history-api-fallback");
var app = express();
var dotenv = require("dotenv");
dotenv.load();

var mongoose = require("mongoose"); //MongoDB object modeling tool
var passport = require("passport"); //Handles users and login
var flash = require("connect-flash");
var cookieParser = require("cookie-parser"); //Parses cookies
var bodyParser = require("body-parser");
var morgan = require("morgan");
var session = require("express-session");
var MongoStore = require("connect-mongo")(session);
const Sentry = require("@sentry/node");
const Tracing = require("@sentry/tracing");

Sentry.init({
    dsn:
        "https://9308264a065c431b87c2be3d1949bea1@o522267.ingest.sentry.io/5633504",
    integrations: [
        // enable HTTP calls tracing
        new Sentry.Integrations.Http({ tracing: true }),
        // enable Express.js middleware tracing
        new Tracing.Integrations.Express({ app }),
    ],

    // We recommend adjusting this value in production, or using tracesSampler
    // for finer control
    tracesSampleRate: 1.0,
});

// RequestHandler creates a separate execution context using domains, so that every
// transaction/span/breadcrumb is attached to its own Hub instance
app.use(Sentry.Handlers.requestHandler());
// TracingHandler creates a trace for every incoming request
app.use(Sentry.Handlers.tracingHandler());

// The error handler must be before any other error middleware and after all controllers
app.use(Sentry.Handlers.errorHandler());

// Optional fallthrough error handler
app.use(function onError(err, req, res, next) {
    // The error id is attached to `res.sentry` to be returned
    // and optionally displayed to the user for support.
    res.statusCode = 500;
    res.end(res.sentry + "\n");
});

global.Neptune_ROOT_DIR = __dirname;

var configDB = process.env["NEPTUNE_MONGOURL"];
mongoose
    .connect(configDB, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        useFindAndModify: false,
    })
    .then((respose) => {
        console.log("Connection to MongoDB successful");
    })
    .catch((error) => {
        console.error("Error in connecting to MongoDB:", error);
    }); // connect to our database

// set up our cookies and html information for login
app.use(morgan("dev")); // log every request to the console
app.use(cookieParser());
//app.use(session({secret:process.env['NEPTUNE_SESSIONSECRET']}))
//app.use(express.cookieParser()); // read cookies (needed for auth)
app.use(bodyParser.json()); // get information from html forms
app.use(bodyParser.urlencoded({ extended: true }));

// session required for passport
app.use(
    session({
        store: new MongoStore({
            mongooseConnection: mongoose.connection,
            ttl: 7 * 24 * 60 * 60,
        }),
        secret: process.env["NEPTUNE_SESSIONSECRET"],
        resave: true,
        saveUninitialized: true,
    })
);

app.use(passport.initialize());
app.use(passport.session()); // persistent login sessions
app.use(flash()); // use connect-flash for flash messages stored in session

require("./controllers/passport.js")(passport); // pass passport for configuration
// load our routes and pass in our app and fully configured passport
// require('./controllers/loginRoutes.js')(app, passport);

//Express app itself
// Middleware for serving '/dist' directory
const staticFileMiddleware = express.static("dist");

// 1st call for unredirected requests
app.use(staticFileMiddleware);

// Support history api
app.use(history());

// 2nd call for redirected requests
app.use(staticFileMiddleware);

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "http://localhost:8081");
    res.header(
        "Access-Control-Allow-Headers",
        "Origin, X-Requested-With, Content-Type, Accept",
        "Access-Control-Allow-Credentials",
        "true"
    );
    next();
});

/**************** CONTROLLERS ****************/
{
    var compileController = require("./controllers/process");
    var databaseController = require("./controllers/databaseInterface");
    var AWS_S3_Controller = require("./controllers/AWS_S3");
    var filesystemController = require("./controllers/filesystem");
}

/*********************   VIEWS   *********************/
{
    app.get("/", function (req, res) {
        res.sendFile(path.join(__dirname, "dist/index.html"), function (err) {
            if (err) {
                res.status(500).send(err);
            }
        });
    });

    app.get("/logout", function (req, res) {
        req.logout();
        res.redirect("/");
    });

    // process the login form
    app.post(
        "/login",
        passport.authenticate("local-login", {
            successRedirect: "/profile", // redirect to the secure profile section
            failureRedirect: "/login", // redirect back to the signup page if there is an error
            failureFlash: true, // allow flash messages
        })
    );

    // process the signup form
    app.post(
        "/signup",
        passport.authenticate("local-signup", {
            successRedirect: "/profile", // redirect to the secure profile section
            failureRedirect: "/signup", // redirect back to the signup page if there is an error
            failureFlash: true, // allow flash messages
        })
    );

    // route middleware to ensure user is logged in
    function isLoggedIn(req, res, next) {
        if (req.isAuthenticated()) return next();
        res.redirect("/login");
    }
}

/************** Mongoose DataBase Calls **************/
{
    app.post("/api/Update_User", databaseController.Update_User);
    app.post("/api/Update_User_cs", databaseController.Update_User_cs);
    app.post("/api/Query_User", databaseController.Query_User);
    app.post("/api/Delete_User", databaseController.Delete_User);

    app.get("/api/v1/workspaces", databaseController.getWorkspaces);
    app.get("/api/v1/jobs", databaseController.getJobs);
    app.get("/api/v1/workspace", databaseController.getWorkspace);
    app.post("/api/v1/workspace", databaseController.createWorkspace);
    app.delete("/api/v1/workspace", databaseController.Delete_Workspace);

    app.get("/api/v1/files", databaseController.getFiles);
    app.get("/api/v1/jobfiles", databaseController.getJobFiles);

    app.get("/api/v1/file", databaseController.getFile);
    app.post("/api/v1/file", databaseController.createFile);
    app.put("/api/v1/file", databaseController.updateFile);
    app.delete("/api/v1/file", databaseController.deleteFile);

    app.get("/api/v1/fs", AWS_S3_Controller.getS3Text);

    app.get("/api/v1/job", databaseController.getJob);

    app.get("/api/v1/downloadFile", filesystemController.downloadFile);
}

/**************** USHROOM MAPPER & FLUIGI ****************/
{
    app.post("/api/v1/mushroommapper", [
        AWS_S3_Controller.preMMFileTransfer,
        compileController.translate,
    ]);
    app.post("/api/v1/fluigi", [
        AWS_S3_Controller.preFluigiFileTransfer,
        compileController.compile,
    ]);
}
/************** API V2 **************/

app.post("/api/v2/login", (req, res, next) => {
    passport.authenticate("local-login", (err, user, info) => {
        if (err) {
            return next(err);
        }

        req.login(user, (err) => {
            res.send({ message: "Logged In !", user: user._id }, 200);
        });
    })(req, res, next);
});

app.get("/api/v2/logout", function (req, res) {
    req.logout();

    console.log("logged out");

    return res.send();
});

app.get("/api/v2/user", databaseController.getUser);

app.post("/api/v2/register", (req, res, next) => {
    passport.authenticate("local-signup", (err, user, info) => {
        if (err) {
            return next(err);
        }

        req.login(user, (err) => {
            if (user == false) {
                res.status(406).send({ message: "User already exists" });
                return;
            }
            if (err) {
                return next(err);
            }
            res.send({ message: "Registered", user: user._id }, 200);
        });
    })(req, res, next);
});

{
    app.get("/api/v2/user", function (req, res) {
        res.send(200);
    });
    app.post("/api/v2/user", function (req, res) {
        res.send(200);
    });

    app.get("/api/v2/workspace", function (req, res) {
        res.send(200);
    });
    app.post("/api/v2/workspace", function (req, res) {
        res.send(200);
    });
    app.delete("/api/v2/workspace", function (req, res) {
        res.send(200);
    });

    app.get("/api/v2/job", function (req, res) {
        res.send(404);
    });

    app.get("/api/v2/file", function (req, res) {
        res.send(200);
    });
    app.post("/api/v2/file", function (req, res) {
        res.send(200);
    });
    app.put("/api/v2/file", function (req, res) {
        res.send(200);
    });
    app.delete("/api/v2/file", function (req, res) {
        res.send(200);
    });

    app.get("/api/v2/file/fs", function (req, res) {
        res.send(200);
    });
    app.post("/api/v2/file/fs", function (req, res) {
        res.send(200);
    });
    app.post("/api/v2/file/copy", function (req, res) {
        res.send(200);
    });
    app.get("/api/v2/workspace/zipfs", function (req, res) {
        res.send(200);
    });
    app.get("/api/v2/job/zipfs", function (req, res) {
        res.send(200);
    });

    app.post("/api/v2/compile/lfr", [
        AWS_S3_Controller.preMMFileTransfer,
        compileController.translate,
    ]);
    app.post("/api/v2/compile/mint", [
        AWS_S3_Controller.preFluigiFileTransfer,
        compileController.compile,
    ]);
}

/*******************************************************/

/*******************************************************/

app.listen(8080, function () {
    console.log("Starting application");
});

/**************** SOCKETIO-REDIS ****************/
var io = require("socket.io")(3000);
var redis = require("socket.io-redis");
io.adapter(
    redis({
        host: process.env["NEPTUNE_REDIS_HOST"],
        port: process.env["NEPTUNE_REDIS_PORT"],
    })
);

io.of("/").adapter.on("error", function (err) {
    console.error("Error connecting to REDIS:", err);
});

io.sockets.on("connection", function (socket) {
    console.log("A new socket connection has started");
    socket.on("all", function (data) {
        socket.broadcast.emit("message", data);
    });

    //On the monitor event, join an ongoing job's channel
    //TODO: Need to check if this belongs to the user
    socket.on("monitor", function (jobid) {
        console.log("job: " + jobid + " is now being monitored");
        socket.join(jobid);
    });
});

/*******************************************************/

/**************** CHECKS IF S3 BUCKET EXISTS ***********/

AWS.config.update({
    accessKeyId: process.env["NEPTUNE_AWSID"],
    secretAccessKey: process.env["NEPTUNE_AWSKEY"],
});
var Target_BUCKET_ID = process.env["NEPTUNE_S3_BUCKET_ID"];

var s3 = new AWS.S3();
s3.headBucket({ Bucket: Target_BUCKET_ID })
    .promise()
    .then(() => {
        console.log("S3 File System bucket exists");
    })
    .catch((error) => {
        if (error.statusCode === 404 || error.statusCode === 400) {
            console.error("S3 File System bucket does not exist !");
        }
    });

/*******************************************************/

app.get("/debug-sentry", function mainHandler(req, res) {
    throw new Error("My first Sentry error!");
});
