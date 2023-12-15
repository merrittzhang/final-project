async function tableSetup() {
    document.title = siteTitle + " - " + activeTable;
    history.pushState(null, null, "/tables/" + activeTable);

    $('#bodyDiv').empty();
    $('<h2/>').text("Join Tables: " + activeTable).appendTo($('#bodyDiv'));

    var request = await fetch("/api/get_all/" + activeTable);
    const response = await request.json();

    let columns = response["columns"];
    let data = response["data"];

    let tableContainer = $('<div/>', {class: "flex-grow-1 d-flex overflow-auto border border-primary rounded-3"}).appendTo($('#bodyDiv'))

    let table = $('<table/>', {class: "table table-striped"}).appendTo(tableContainer);
    let head = $('<thead/>').appendTo(table);
    head = $('<tr/>').appendTo(head);

    for (const col of columns) {
        $('<th/>').text(col).appendTo(head);
    }

    let body = $('<tbody/>').appendTo(table);

    for (const row of data) {
        let tableRow = $('<tr />').appendTo(body);

        for (const col of columns) {
            $('<th/>').text(row[col]).appendTo(tableRow);
        }
    }
}