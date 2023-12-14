async function tableSetup() {
    document.title = siteTitle + " - " + activeTable;
    history.pushState(null, null, "/tables/" + activeTable);

    $('#bodyDiv').empty();
    $('<h2/>').text(activeTable).appendTo($('#bodyDiv'));

    var request = await fetch("/api/tables/" + activeTable);
    const response = await request.json();

    let columns = response["columns"];
    console.log(columns);
    let data = response["data"];

    let table = $('<table/>', {class: "table table-striped m-3"}).appendTo($('#bodyDiv'));
    let head = $('<thead/>').appendTo(table);
    head = $('<tr/>').appendTo(head);

    for (const col of columns) {
        $('<th/>').text(col).appendTo(head);
    }

    let body = $('<tbody/>').appendTo(table);
    let even = false;

    for (const row of data) {
        let tableRow = $('<tr />').appendTo(body);

        for (const col of columns) {
            $('<th/>').text(row[col]).appendTo(tableRow);
        }
    }
}