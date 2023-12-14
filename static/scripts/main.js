function mainSetup() {
    document.title = siteTitle;
    history.pushState(null, null, "/");

    $('#bodyDiv').empty();
    $('<h2/>').text("Tables:").appendTo('#bodyDiv');
    var list = $('<ul/>').appendTo($('#bodyDiv'));
    for (const table of tables) {
        list.append($("<li/>").append($('<a/>', {href: "/tables/" + table}).text(table)));
    }
}