$(document).ready(setup);

async function setup() {
    const response = await fetch("/api/get_tables");
    tables = await response.json();
    console.log(tables);

    $('#tablesList').empty();
    var list = $('<ul/>').appendTo($('#tablesList'));
    for (const table of tables) {
        list.append($('<li/>').text(table));
    }
}