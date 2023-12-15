async function tableSetup() {
    document.title = siteTitle + " - " + activeTable;
    history.pushState(null, null, "/tables/" + activeTable);

    $('#bodyDiv').empty();
    $('<h2/>').text("Join Tables: " + activeTable).appendTo($('#bodyDiv'));

    var request = await fetch("/api/get_all/" + activeTable);
    const response = await request.json();

    let columns = response["columns"];
    let data = response["data"];
    let types = response["types"];

    let tableContainer = $('<div/>', {class: "flex-grow-1 d-flex overflow-auto border border-primary rounded-3"}).appendTo($('#bodyDiv'))

    let table = $('<table/>', {id: "mainTable", class: "table table-striped"}).appendTo(tableContainer);
    fillTable(table, columns, data);

    let addButton = $('<button/>', {id: "addButton", class: "btn btn-success"}).text("Insert Row").appendTo($('#bodyDiv'));

    addButton.click(() => {
        insertRow(columns, types);
        tableContainer.scrollTop(tableContainer.prop("scrollHeight"));
        addButton.hide();
    })
}

function fillTable(table, columns, data) {
    table.empty();
    let head = $('<thead/>').appendTo($(table));
    head = $('<tr/>').appendTo(head);

    $('<th/>').text("Modify").appendTo(head);

    for (const col of columns) {
        $('<th/>').text(col).appendTo(head);
    }

    let body = $('<tbody/>', {id: "tableBody"}).appendTo($(table));

    for (const row of data) {
        let tableRow = $('<tr />').appendTo(body);

        let buttonsCell = $('<th/>').appendTo(tableRow);
        let buttonsDiv = $('<div/>', {class: "d-flex"}).appendTo(buttonsCell);
        let editButton = $('<button/>', {class: "btn btn-circle-sm btn-warning"}).text("Edit").appendTo(buttonsDiv);
        let deleteButton = $('<button/>', {class: "btn btn-circle-sm btn-danger"}).text("Delete").appendTo(buttonsDiv);

        for (const col of columns) {
            $('<th/>').text(row[col]).appendTo(tableRow);
        }

        deleteButton.click(() => {
            let identifiers = row;
            console.log(row);
            let requestData = {
                type: 'POST',
                url: "/api/delete/" + activeTable,
                data: JSON.stringify(identifiers),
                contentType: 'application/json',
                success: async function () {
                    console.log("Successfully received data");
                    var request = await fetch("/api/get_all/" + activeTable);
                    const response = await request.json();

                    let newColumns = response["columns"];
                    let newData = response["data"];
                    fillTable(table, newColumns, newData);
                    $('#addButton').show();
                    return;
                },
                error: function () {
                    console.log("Request failed");
                    alert("Request failed");
                    return;
                }
            };
            $.ajax(requestData);
        })
    }
}

function insertRow(columns, types) {
    let tableRow = $('<tr/>').appendTo($('#tableBody'));
    let buttonsCell = $('<th/>').appendTo(tableRow);
    let buttonsDiv = $('<div/>', {class: "d-flex"}).appendTo(buttonsCell);
    let submitButton = $('<button/>', {class: "btn btn-circle-sm btn-primary"}).text("Save").appendTo(buttonsDiv);
    let cancelButton = $('<button/>', {class: "btn btn-circle-sm btn-secondary"}).text("Cancel").appendTo(buttonsDiv);

    for (const col of columns) {
        let cell = $('<th/>').appendTo(tableRow);
        $('<input/>', {id: "input" + col, type: "text", class: "form-control", placeholder: col}).appendTo(cell);
    }

    submitButton.click(() => {
        console.log("submitting")
        let values = {}
        for (const col of columns) {
            console.log(col);
            let input = $('#input' + col).val();
            if (input == '') {
                alert("Input field for " + col + " is empty!");
                return;
            }
            if (types[col] == "INTEGER") {
                input = parseInt(input);
                if (isNaN(input)) {
                    alert("Input field for " + col + " must be an integer!");
                    return;
                }                
            } else if (types[col] == "REAL") {
                input = parseFloat(input);
                if (isNaN(input)) {
                    alert("Input field for " + col + " must be a float!");
                    return;
                }
            }
            values[col] = input;
        }
        console.log(values);
        let requestData = {
            type: 'POST',
            url: "/api/insert/" + activeTable,
            data: JSON.stringify(values),
            contentType: 'application/json',
            success: async function () {
                console.log("Successfully received data");
                var request = await fetch("/api/get_all/" + activeTable);
                const response = await request.json();

                let newColumns = response["columns"];
                let newData = response["data"];
                $('#addButton').show();
                fillTable($('#mainTable'), newColumns, newData);
                return;
            },
            error: function () {
                console.log("Request failed");
                alert("Request failed");
                return;
            }
        };
        $.ajax(requestData);
    })
    
    cancelButton.click(() => {
        tableRow.remove();
        $('#addButton').show();
    })
}
