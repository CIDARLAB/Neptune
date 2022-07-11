/*
 Created by Priya on 27/09/2016.
 JS file populates table based on calculations
*/

localStorage.crankradius = 0.63;
localStorage.pistonrod = 3;
localStorage.offset = 0.88;

var servoTable = servo;
var syringeTable = syringe;

/*
 Iterates through syringes 1-12
 Iterates through servos A-L
 Calculates Vc and Pc
 If Vc>=V and Pc<=P then save servo and syringe into table
*/
function calculateRecommended() {
    var arr = [];

    // loadButtons();
    // setNumberOfDispensers_JSON();
    // setNumberOfPumps_JSON();

    for (var key in servoTable) {
        if (servoTable.hasOwnProperty(key)) {
            var servoID = servoTable[key].id;

            var r = parseFloat(localStorage.crankradius);
            var b = parseFloat(localStorage.pistonrod);
            var d = parseFloat(localStorage.offset);

        }

        // localStorage.numberofvalves = JSON.parse(localStorage.pumpData).length;
        // localStorage.numberofdispensers = JSON.parse(localStorage.dispenserData).length;

        for (var key2 in syringeTable) {
            if (syringeTable.hasOwnProperty(key2)) {
                //loop through syringes

                var syringeID = syringeTable[key2].ids;

                //1 * 10^-9 m3 = 1 microLitre = 0.610237441 inch ^3
                //Find x1 such that Area*x1= 0.610237441 inch ^3
                //So x1 = (0.610237441 inch ^3)/Area = inches

                var syringex1 = (0.0610237441) / syringeTable[key2].area;
                var syringevolume = syringeTable[key2].volume;
                var syringecost = syringeTable[key2].costs;


                var servocost = servoTable[key].cost;
                var PWM_min = servoTable[key].PWM_min;
                var PWM_max = servoTable[key].PWM_max;

                console.log("PWM MIN " + PWM_min + " PWM_MAX " + PWM_max + " syringex1 " + syringex1);
                var setupvalues = initializeSetup(PWM_min, PWM_max, 0.63, 3, 0, syringex1);

                // Error Check
                var insidesqrt = Math.pow((r * Math.sin(setupvalues.theta_max * Math.PI / 180)) + parseFloat(d), 2);
                var insidesqrt2 = Math.pow((r * Math.sin(setupvalues.theta_min * Math.PI / 180)) + parseFloat(d), 2);
                var x1 = (r * Math.cos(setupvalues.theta_max * Math.PI / 180)) + Math.sqrt((b * b) - insidesqrt);
                var x2 = (r * Math.cos(setupvalues.theta_min * Math.PI / 180)) + Math.sqrt((b * b) - insidesqrt2);
                var xtotal = Math.abs(x1 - x2);


                var servo_volume = xtotal / syringex1;
                var my_servo_volume;
                if (servo_volume > syringevolume) {
                    my_servo_volume = syringevolume;
                }
                else {
                    my_servo_volume = servo_volume;
                }

                if (localStorage.volume / 1000 <= syringevolume && my_servo_volume >= localStorage.volume / 1000 && localStorage.precision >= setupvalues.uL_precision) {
                    //Save servo syringe combo in array
                    console.log("Servo ID passed: " + servoID);
                    console.log("Syringe ID passed: " + syringeID);
                    var singlestage = {};
                    singlestage.servoID = servoID;
                    singlestage.syringeID = syringeID;
                    singlestage.v = xtotal / syringex1;
                    singlestage.p = setupvalues.uL_precision;
                    singlestage.cost = servocost + syringecost;
                    arr.push(singlestage);
                }
            }
        }

    }


    //comboList
    var combolist = document.getElementById("comboList");
    for (var index = combolist.rows.length - 1; index > 0; index--) {
        combolist.deleteRow(index);
    }
    var i = 0;
    var count = 0;
    for (var key in arr) {
        if (arr.hasOwnProperty(key)) {
            var row = combolist.insertRow(i + 1);
            row.style.fontSize = 20;
            var cell1 = row.insertCell(0); //Combo ID
            var cell2 = row.insertCell(1); //Servo
            var cell3 = row.insertCell(2);// Syringe Names
            var cell4 = row.insertCell(3); //Precision
            var cell5 = row.insertCell(4); //Volume
            var cell6 = row.insertCell(5); //Cost
            // var cell6 = row.insertCell(5); //Syringe URL
            // var cell7 = row.insertCell(6); //Servo URL

            var ServoObject = getObjects(servoTable, 'id', arr[key].servoID);
            var SyringeObject = getObjects(syringeTable, 'ids', arr[key].syringeID);

            // cell1.innerHTML = arr[key].servoID +arr[key].syringeID;
            cell1.innerHTML = "<strong class='primary-font' style='font-size: 20px'>" + arr[key].servoID + arr[key].syringeID + "</strong>";
            cell2.innerHTML = "<p style='font-size:17px; font:bold'>" + "Servo: " + ServoObject[0].name
                + "</br><img src='../../images/build/standardservo.JPG' style='height: 60px;'>" + "</p>";
            cell3.innerHTML = "<p style='font-size:17px; font:bold'>" + "Syringe: " + SyringeObject[0].volume + "ml"
                + "</br></br><img src='../../images/fluigi/SyringeTube.png' style='height: 30px;'>" + "</p>";
            cell4.innerHTML = "<p style='font-size:17px; font:bold'>" + Math.round(arr[key].p * 1000) / 1000 + " uL precision</p>";
            cell5.innerHTML = "<p style='font-size:17px; font:bold'>" + "Dispension of " + Math.round(arr[key].v * 1000) / 1000 + " ml" + "</p>";
            cell6.innerHTML = "<p style='font-size:17px; font:bold'>" + "$" + Math.round(arr[key].cost * 1000) / 1000 + " (as of Oct 2016)" + "</p>";


            i++;
            count++;
        }
    }

    if (count == 0) { //If no possible combinations found
        console.log("No Combinations Found!");
        var row = combolist.insertRow(i + 1);
        var cell1 = row.insertCell(0); //Combo ID
        var cell2 = row.insertCell(1); //Servo
        var cell3 = row.insertCell(2);// Syringe Names
        var cell4 = row.insertCell(3); //Precision
        var cell5 = row.insertCell(4); //Volume
        var cell6 = row.insertCell(5); //Cost

        cell1.innerHTML = 'No combinations found';
        cell2.innerHTML = '-';
        cell3.innerHTML = '-';
        cell4.innerHTML = '-';
        cell5.innerHTML = '-';
        cell6.innerHTML = '-';
    }

}

/*
 Retrieves the json object of a particular servo/syringe
 */
function getObjects(obj, key, val) {
    var objects = [];
    for (var i in obj) {
        if (!obj.hasOwnProperty(i)) continue;
        if (typeof obj[i] == 'object') {
            objects = objects.concat(getObjects(obj[i], key, val));
        } else if (i == key && obj[key] == val) {
            objects.push(obj);
        }
    }
    return objects;
}

/*
 Performs specification calculations based on a servo-syringe combination
 */
function initializeSetup(PWM_min, PWM_max, r, b, d, a) {
    function deg2rad(degrees) {
        var pi = Math.PI;
        return (degrees * (pi / 180));
    }

    function PWM2rad(PWM) {
        var deg = ( (PWM - PWM_min) * (theta_max - theta_min) / (PWM_max - PWM_min) ) + theta_min;
        return (deg * (Math.PI / 180));
    }

    function displacement(thetaX, r, b, d, a) {
        return ( r * Math.cos(deg2rad(thetaX)) ) + Math.sqrt(Math.pow(b, 2) - ( Math.pow((r * Math.sin(deg2rad(thetaX)) + d), 2) ));
    }

    var thetaXArray = [];               // create array of angles to be populated in for loop
    var displacementArray = [];         // create array of displacement values
    var increment = 1000;               // Set resolution of system; from -90 to 270 degrees, 1000 total intervals is sufficient
    var stepSize = 360 / increment;       // Set step size for thetas to start at -90 and end at 270, a total of 360s
    for (var i = 0; i <= increment; i++) {       // Iterate from 0 to 1000 by one
        var thetaX_i = -90 + stepSize * i;              // Calculate theta value from i
        thetaXArray.push(thetaX_i);             // Add current theta value to theta array
        displacementArray.push(displacement(thetaX_i, r, b, d, a));     // Add current displacement value to array
    }

    var displacement_min = Math.min.apply(null, displacementArray);         // Calculate value by finding minimum of displacement array
    var displacement_max = Math.max.apply(null, displacementArray);         // Calculate value by finding maximum of displacement array


    var theta_min = thetaXArray[displacementArray.indexOf(displacement_max)];       // Calculate theta_min by pulling theta value from theta array at the index where the displacement max was found
    var theta_max = thetaXArray[displacementArray.indexOf(displacement_min)];       // Calculate theta_max by pulling theta value from theta array at the index where the displacement min was found
    var X_max = displacement(theta_min, r, b, d, a);                             // Calculate Xmax by plugging in theta_min to displacement function
    var X_min = displacement(theta_max, r, b, d, a);                             // Calculate Xmin by plugging in theta_max to displacement function
    var mL_min = 0;      // Default value for mLmax, initalized by user in Assembly step. MUST be true
    var mL_max = mL_min + (X_max - X_min) / a;                                       // Calculate mLmax by S
    var uL_min = mL_min * 1000;		// convert incoming variables from mL to uL
    var uL_max = mL_max * 1000;
    var mL_range = mL_max - mL_min;
    var uL_range = mL_range * 1000; 	// convert incoming variables from mL to uL


    // Create PWM_table and find uL_precision
    var PWM_table = [];    // used in this inner function
    var PWM_dic = {};       // passed as output to easily hash

    var not_found = true;
    for (var i = PWM_min; i <= PWM_max; i++) {		// From PWM_min value to PWM_max value
        PWM_table.push(i);						// Add current PWM value to PWM_table
        var mL_temp = mL_max - ((( r * Math.cos(PWM2rad(i)) ) + Math.sqrt(Math.pow(b, 2) - ( Math.pow((r * Math.sin(PWM2rad(i)) + d), 2) ))) - X_min) / a;	// Calculate mL value with formula of motion
        var uL_temp = Math.round(mL_temp * 100000) / 100;		// convert to uL and round to first decimal place
        PWM_table.push(uL_temp);				// Add uL value to PWM_table

        PWM_dic[i] = uL_temp;

        // Find uL_precision by finding the max uL difference between PWM values.
        var uL_diff = PWM_table[PWM_table.length - 1] - PWM_table[PWM_table.length - 3];
        var uL_diff_prev = PWM_table[PWM_table.length - 3] - PWM_table[PWM_table.length - 5];
        if (uL_diff < uL_diff_prev && not_found) {
            var uL_precision = Math.round(uL_diff_prev * 100) / 100;
            not_found = false;
        }
    }
    // create uL_table
    var uL_table = [];
    var uL_dic = {};
    for (var i = uL_min; i < uL_range + uL_min + uL_precision; i = i + uL_precision) {		// From uL_min (a given) to uL_min+uL_range! uL_precision added on to allow last uL value to be iterated through. Increase by steps of uL_precision
        // rename i (which is current uL value)
        var uL_current = i;									// rename i to something more readable
        uL_current = Math.round(uL_current * 100) / 100;		// round to 2 decimal places

        // Add uL to table
        uL_table.push(uL_current); 							// Add the current uL value to uL_table

        // Find PWM values
        // Add First PWM value, matched easily
        if (i == uL_min) {		// We know the first value, which can't be found with linear interpolation
            uL_table.push(PWM_table[0]);
            uL_dic[uL_current] = PWM_table[0];
            continue;
        }
        // Linear interpolation to find other PWM values
        // Skip to 2nd value as we already logged the first
        for (var j = 3; j <= PWM_table.length; j = j + 2) {			// Iterate through uL values in PWM_table (start at 2nd uL value, index 3. Go length of PWM table. Increase by 2 to avoid looking at PWM values)
            if (PWM_table[j] >= uL_current && j % 2 > 0) { 		// If uL value in PWM_table is greater than or equal to our current uL value, find PWM inbetween PWMs in PWM_table
                var PWM_between = PWM_table[j - 3] + (uL_current - PWM_table[j - 2]) * ((PWM_table[j - 1] - PWM_table[j - 3]) / (PWM_table[j] - PWM_table[j - 2]));	// Find PWM value via linear interpolation
                var PWM_between = Math.round(PWM_between * 100) / 100;	// Round calculated PWM value to 2 decimal places
                uL_table.push(PWM_between);						// Add calculated PWM value to table

                uL_dic[uL_current] = PWM_between;
                break;
            }
        }

        if (i >= uL_range + uL_min) {
            uL_table.push(PWM_max);      // Add last PWM value, not calculated above with linear interpolation
            uL_dic[uL_current] = PWM_max;
        }
    }
    return {
        theta_min: theta_min,
        theta_max: theta_max,
        X_min: X_min,
        X_max: X_max,
        uL_min: uL_min,
        uL_max: uL_max,
        PWM_table: PWM_table,
        PWM_dic: PWM_dic,
        uL_table: uL_table,
        uL_dic: uL_dic,
        uL_precision: uL_precision,
        r: r,
        b: b,
        d: d,
        a: a
    };
}

/*
 Pass on information of customized setup to control page
 */
function givetocontrol(PWM_min, PWM_max, syringex1) {
    var setupvalues = initializeSetup(PWM_min, PWM_max, 0.63, 3, 0.88, syringex1);
    var control_init = [];
    var disp = {};
    for (var j = 1; j != (parseInt(JSON.parse(localStorage.numberofdispensers) + 1)); j++) {
        disp.pwmtable = setupvalues.PWM_table;
        disp.pwmdic = setupvalues.PWM_dic;
        disp.ultable = setupvalues.uL_table;
        disp.uldic = setupvalues.uL_dic;
        disp.ulmax = setupvalues.uL_max;
        disp.ulmin = setupvalues.uL_min;
        disp.ulprecision = setupvalues.uL_precision;
        control_init.push(disp);
    }
//GIVE TO CONTROL:
    // localStorage.control_initialization = control_init;
    localStorage.setItem('control_initialization', JSON.stringify(control_init));
}