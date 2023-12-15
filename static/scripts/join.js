async function joinSetup() {
    document.title = siteTitle + " - Join";
    history.pushState(null, null, "/join");

    var request = await fetch("/api/get_columns");
    const columns = await request.json();

    $('#bodyDiv').empty();
    $('<h2/>').text("Join Tables:").appendTo($('#bodyDiv'));

    let container = $('<div/>', {class: "mh-100 d-flex overflow-hidden"}).appendTo($('#bodyDiv'));

    let joinDiv = $('<div/>', {class: "mh-100 overflow-auto col-3", id: "leftCol"}).appendTo(container);
    $('<div/>', {class: "mh-100 col-9 d-flex flex-column overflow-hidden", id: "rightCol"}).appendTo(container);

    $('<h4/>').text("Primary Table").appendTo(joinDiv);
    let selectPrim = $('<select/>', {class: "form-select", "aria-label": "Select a Table"}).appendTo(joinDiv);
    for (let table of tables) {
        $('<option/>', {value: table}).text(table).appendTo(selectPrim);
    }

    let secondaryTablesDiv = $('<div/>', {class: "secondaryTables"}).appendTo($(joinDiv));
    let numTables = 1;
    let secondaryTables = [];

    if (tables.length < 2) {
        $("<h6/>", {class: "text-danger"}).text("Not enough tables in db to join!").appendTo(secondaryTablesDiv);
        return;
    }

    let joinForm = getJoinForm(0, columns);
    secondaryTables.push(joinForm);
    secondaryTablesDiv.append(secondaryTables[0]);

    let buttonsDiv = $('<div/>', {class: "d-flex"}).appendTo(joinDiv);
    let addButton = $('<button/>', {class: "btn btn-success"}).text("Add Table").appendTo(buttonsDiv);
    let deleteButton = $('<button/>', {class: "btn btn-danger"}).text("Remove Table").appendTo(buttonsDiv);

    deleteButton.hide();

    if (tables.length == 2) {
        addButton.hide();
    }

    addButton.click(() => {
        let joinForm = getJoinForm(numTables, columns);
        secondaryTables.push(joinForm);
        secondaryTablesDiv.append(secondaryTables[numTables]);

        numTables += 1;
        deleteButton.show();
        if (tables.length == numTables + 1) {
            addButton.hide();
        }
    });

    deleteButton.click(() => {
        numTables -= 1;

        secondaryTables[numTables].remove();
        addButton.show();
        if (numTables == 1){
            deleteButton.hide();
        }
    })

    let joinButton = $('<button/>', {class: "btn btn-primary"}).text("Join").appendTo(joinDiv);

    joinButton.click(() => {
        let prim_table = selectPrim.val();
        let tables = [];
        let identifiers = [];

        for (let i = 0; i < numTables; i++) {
            tables.push($('#secondaryTable' + i).val());
            let table1 = $('#table1' + i).val();
            let col1 = $('#col1' + i).val();
            let table2 = $('#table2' + i).val();
            let col2 = $('#col2' + i).val();
            identifiers.push([[table1, col1, table2, col2]]);
        }
        console.log(prim_table);
        console.log(tables);
        console.log(identifiers);

        let requestData = {
            type: 'POSt',
            url: "/api/join",
            data: JSON.stringify({"prim_table": prim_table, "tables": tables, "identifiers": identifiers}),
            contentType: 'application/json',
            success: function (data) {
                console.log("Successfully received data");
                makeTable(data);
                return;
            },
            error: function () {
                console.log("Request failed");
                $("#rightCol").empty();
                $("<h2/>", {class: "text-danger"}).text("Server Error").appendTo($("#rightCol"));
                return;
            }
        };
        $.ajax(requestData);
    })
}

function getJoinForm(index, columns) {
    let item = $("<div/>", {id: "secondaryDiv" + index});
    $("<h4/>").text("Join").appendTo(item);
    let selectSecondary = $('<select/>', {id: "secondaryTable" + index, class: "form-select", "aria-label": "Select a Table"}).appendTo(item);
    for (let table of tables) {
        $('<option/>', {value: table}).text(table).appendTo(selectSecondary);
    }
    $("<h4/>").text("On").appendTo(item);
    let selectorsDiv1 = $("<div/>", {class: "d-flex"}).appendTo(item);
    let table1 = $('<select/>', {id: "table1" + index, class: "form-select", "aria-label": "Select a Table"}).appendTo(selectorsDiv1);
    selectorsDiv1.append($("<p/>").text("."));
    let col1 = $('<select/>', {id: "col1" + index, class: "form-select", "aria-label": "Select a Table"}).appendTo(selectorsDiv1);
    $("<p/>").text("=").appendTo(item);
    selectorsDiv2 = $("<div/>", {class: "d-flex"}).appendTo(item);
    let table2 = $('<select/>', {id: "table2" + index, class: "form-select", "aria-label": "Select a Table"}).appendTo(selectorsDiv2);
    selectorsDiv2.append($("<p/>").text("."));
    let col2 = $('<select/>', {id: "col2" + index, class: "form-select", "aria-label": "Select a Table"}).appendTo(selectorsDiv2);

    for (let col of columns[tables[0]]) {
        $('<option/>', {value: col}).text(col).appendTo(col1);
        $('<option/>', {value: col}).text(col).appendTo(col2);
    }

    table1.change(() => {
        console.log("Join " + index + " - Table 1 change");
        let table = table1.val();
        col1.empty();
        for (let col of columns[table]) {
            $('<option/>', {value: col}).text(col).appendTo(col1);
        }
    });

    table2.change(() => {
        console.log("Join " + index + " - Table 2 change");
        let table = table2.val();
        col2.empty();
        for (let col of columns[table]) {
            $('<option/>', {value: col}).text(col).appendTo(col2);
        }
    });

    for (let table of tables) {
        $('<option/>', {value: table}).text(table).appendTo(table1);
        $('<option/>', {value: table}).text(table).appendTo(table2);
    }

    console.log(item);
    return item;
}

function makeTable(data) {
    $('#rightCol').empty();
    if (data.length == 0) {
        return;
    }

    let tableContainer = $('<div/>', {class: "flex-grow-1 d-flex overflow-auto border border-primary rounded-3"}).appendTo($('#rightCol'))

    let table = $('<table/>', {class: "table table-striped"}).appendTo(tableContainer);
    let head = $('<thead/>').appendTo(table);
    head = $('<tr/>').appendTo(head);

    columns = Object.keys(data[0]);

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
