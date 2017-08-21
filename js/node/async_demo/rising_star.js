// Examples based on YouTube video from RisingStar
//
// https://www.youtube.com/watch?v=ca7HAqbfd90

// Setup
// npm init --yes
// node -v

const fs = require('fs');
const path = require('path');
const async = require('async');

fs.readFile(path.join(__dirname, 'package.json'), 'utf-8', function (err, result) {
    if (err) {
        return console.error(err);
    }
    // Synchronous exception handling within the callback
    try {
        const object = JSON.parse(result);
        console.log(object.name);
    } catch (ex) {
        return console.error(ex);
    }


})

// Part II : npm i async --save
// Additional require statement added in the top stanza

async.map(['package.json', 'package-clone.json'], function (name, callback) {
    fs.readFile(path.join(__dirname, name), 'utf-8', 
        function (err, result) {
            if (err) {
                return callback(err);
            }
            // Synchronous exception handling within the callback
            try {
                const object = JSON.parse(result);
                console.log(object.name);
            } catch (ex) {
                return callback(ex);
            }
            callback(null, object.name)

        })
}, function(err, results) {
    console.log(results);
})

