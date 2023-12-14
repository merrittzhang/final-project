$(document).ready(setup);
tables = [];
activeTable = null;
siteTitle = "SQLite Web Browser";

async function setup() {
    let path = window.location.pathname;
    let path_split = path.split("/");

    var response = await fetch("/api/get_tables");
    tables = await response.json();
    console.log(tables);

    if (path == '/') {
        mainSetup();
    } else if (path_split[1] == 'tables') {
        if (path_split.length != 3) {
            console.log("Invalid path");
            mainSetup();
        }
        let table = path_split[2];
        if (!tables.includes(table)) {
            console.log("Invalid path");
            mainSetup();
        }

        activeTable = table;
        tableSetup();
    }
}