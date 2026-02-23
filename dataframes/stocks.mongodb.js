/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/


const collection = "stocks_by_category"
// Select the database to use.
use('market');


// // Insert a few documents into the sales collection.
db.getCollection(collection).insertMany([
    { "category": "CC", "stocks": ["V", "MA"] }, { "category": "Real_Estate", "stocks": ["KBH", "O", "Z"] }, { "category": "Drugs", "stocks": ["PFE", "GILD", "MRNA", "LLY", "WBA"] }, { "category": "Consumer", "stocks": ["TAP", "KOF", "CROX", "LULU", "NKE"] }, { "category": "Cannbis", "stocks": ["TLRY", "CGC", "GRWG", "MJ"] }, { "category": "Financials", "stocks": ["JPM", "GS", "C", "WAL", "KRE", "WFC", "SOFI", "PACW", "SCHW"] }, { "category": "EV", "stocks": ["TSLA", "NIO", "PSNY"] }, { "category": "Streaming", "stocks": ["NFLX", "DIS"] }, { "category": "Crude_Oil", "stocks": ["XLE", "MPC", "SLB", "XOM"] }
]);

