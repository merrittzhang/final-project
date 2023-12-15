async function tableSetup() {
    document.title = siteTitle + " - " + activeTable;
    history.pushState(null, null, "/tables/" + activeTable);

    $('#bodyDiv').empty();
    $('<h2/>').text("Table: " + activeTable).appendTo($('#bodyDiv'));

    var request = await fetch("/api/get_all/" + activeTable);
    const response = await request.json();

    let columns = response["columns"];
    let data = response["data"];
    let types = response["types"];

    let tableContainer = $('<div/>', {class: "flex-grow-1 d-flex overflow-auto border border-primary rounded-3"}).appendTo($('#bodyDiv'))

    $('<table/>', {id: "mainTable", class: "table table-striped"}).appendTo(tableContainer);
    fillTable(columns, types, data);

    let addButton = $('<button/>', {id: "addButton", class: "btn btn-success"}).text("Insert Row").appendTo($('#bodyDiv'));

    addButton.click(() => {
        insertRow(columns, types);
        tableContainer.scrollTop(tableContainer.prop("scrollHeight"));
        addButton.hide();
    })
}

function fillTable(columns, types, data) {
    $('#mainTable').empty();
    let head = $('<thead/>').appendTo($('#mainTable'));
    head = $('<tr/>').appendTo(head);

    $('<th/>').text("Modify").appendTo(head);

    for (const col of columns) {
        $('<th/>').text(col).appendTo(head);
    }

    let body = $('<tbody/>', {id: "tableBody"}).appendTo($('#mainTable'));

    for (const row of data) {
        let tableRow = $('<tr />').appendTo(body);
        makeRow(columns, types, tableRow, row);        
    }
}

function makeRow(columns, types, tableRow, row) {
    let buttonsCell = $('<th/>').appendTo(tableRow);
    let buttonsDiv = $('<div/>', {class: "d-flex"}).appendTo(buttonsCell);
    let editButton = $('<button/>', {class: "btn btn-circle-sm btn-warning"}).text("Edit").appendTo(buttonsDiv);
    let deleteButton = $('<button/>', {class: "btn btn-circle-sm btn-danger"}).text("Delete").appendTo(buttonsDiv);

    for (const col of columns) {
        $('<th/>').text(row[col]).appendTo(tableRow);
    }

    editButton.click(() => {
        editRow(columns, types, tableRow, row);
    })

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
                fillTable(newColumns, types, newData);
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

function insertRow(columns, types) {
    let tableRow = $('<tr/>').appendTo($('#tableBody'));
    let buttonsCell = $('<th/>').appendTo(tableRow);
    let buttonsDiv = $('<div/>', {class: "d-flex"}).appendTo(buttonsCell);
    let submitButton = $('<button/>', {class: "btn btn-circle-sm btn-primary"}).text("Save").appendTo(buttonsDiv);
    let cancelButton = $('<button/>', {class: "btn btn-circle-sm btn-secondary"}).text("Cancel").appendTo(buttonsDiv);

    for (const col of columns) {
        let cell = $('<th/>').appendTo(tableRow);
        $('<input/>', {id: "input_insert" + col, type: "text", class: "form-control", placeholder: col}).appendTo(cell);
    }

    submitButton.click(() => {
        submitRow(columns, types, null, "insert");
    })
    
    cancelButton.click(() => {
        tableRow.remove();
        $('#addButton').show();
    })
}

function editRow(columns, types, tableRow, row) {
    tableRow.empty();

    let buttonsCell = $('<th/>').appendTo(tableRow);
    let buttonsDiv = $('<div/>', {class: "d-flex"}).appendTo(buttonsCell);
    let submitButton = $('<button/>', {class: "btn btn-circle-sm btn-primary"}).text("Save").appendTo(buttonsDiv);
    let cancelButton = $('<button/>', {class: "btn btn-circle-sm btn-secondary"}).text("Cancel").appendTo(buttonsDiv);

    for (const col of columns) {
        let cell = $('<th/>').appendTo(tableRow);
        $('<input/>', {id: "input_update" + col, type: "text", class: "form-control", value: row[col]}).appendTo(cell);
    }

    submitButton.click(() => {
        submitRow(columns, types, row, "update")
    })

    cancelButton.click(() => {
        tableRow.empty();
        makeRow(columns, types, tableRow, row);
    });
}

function submitRow(columns, types, row, action) {
    console.log("submitting")
    let values = {}
    for (const col of columns) {
        console.log(col);
        let input = $('#input_' + action + col).val();
        console.log(input);
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
    let data;
    if (action == "insert") {
        data = values;
    } else {
        data = {"values": values, "identifiers": row};
    }
    let requestData = {
        type: 'POST',
        url: "/api/" + action + "/" + activeTable,
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: async function () {
            console.log("Successfully received data");
            var request = await fetch("/api/get_all/" + activeTable);
            const response = await request.json();

            let newColumns = response["columns"];
            let newData = response["data"];
            $('#addButton').show();
            fillTable(newColumns, types, newData);
            return;
        },
        error: function () {
            console.log("Request failed");
            alert("Request failed");
            return;
        }
    };
    $.ajax(requestData);
}
