# SQLite Browser

Created by [Samuel Sanft](https://github.com/ss7886) and [Merritt Zhang](https://github.com/merrittzhang).


### Installing

Our code requires the following python libraries: 
- `flask`
- `pytest` - Only for testing
- `coverage` - Only for testing

These can be installed using pip:
`pip install flask pytest coverage `


### Running

The server can be run by running `main.py`. The program takes two command line arguments, a path to a valid database (some sample databases are included in `example_dbs/`) and an open port.

Running `python main.py -h` will display the necessary arguments.

Example run command: `python main.py example_dbs/reg.sqlite 3000`

Once the server is online, the web application can be accessed at `localhost:<port>`.


### Using the Site

The following pages can be accessed from the navbar.

- Home - the Home page contains a list of tables in the database. Clicking on one will bring the user to that table's page.
- Table - Each table has it's own page that can be accessed from the home menu or the dropdown menu under tables. From this page a user can view the rows and columns in a table, edit, delete or insert a row. (Attempting to edit multiple rows at a time could have unintended consequences).
- Join - This table allows a user to execute and view join commands. First the user must select a primary table. Then the user selects a table to join onto the primary table. The user must select a column from the first table and a column from the second table on which to perform the join. Pressing join will execute the command and display the results in the right pane. A user can perform multiple joins by pressing the Add Table button. Pressing the Remove button will remove the extra join. (Known bug: If a user adds a form for a second join, removes it, and then adds it again, then the data in the columns selectors will become unresponsive and not update to match the corresponding tables).


### Testing

Testing can be run using the following command:

`python -m pytest`

To perform stress tests with timing:

`python -m pytest --run-stress --durations=0`

To perform coverage testing run:

`python -m coverage run -m pytest`

After running coverage testing:

`python -m coverage report` to view coverage report in terminal.

`python -m coverage html` to generate coverage report viewable in browser (located at `htmlcov/index.py`)
