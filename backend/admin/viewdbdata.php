<?php
session_start();
include 'settings.php';
  $db_conn = pg_connect(" host = $hostname port = $port dbname = $dbname user = $username password = $pass ") or die ("Could not connect to server \n");
?>
<!DOCTYPE html>
<html>
<head>
	<title>Activities' Visualization Admin Panel</title>
	<link rel="stylesheet" type="text/css" href="css/sortable-table.css">
	<link rel="stylesheet" type="text/css" href="css/menu_css.css">
	<link href="https://fonts.googleapis.com/css2?family=Jost:wght@500&display=swap" rel="stylesheet">
</head>

<body>
	<div class="main">  	
		<div>
			<table>
				<tr>
					<td align ="left" style="width:80%;">
						<label>Welcome user: 
							<?php 
							if (!$db_conn){
								echo "Error: Unable to open database\n:";
							}
							else
							{
								$query = "SELECT fullname FROM adminusers WHERE id = ". $_SESSION['user'];
								$result = pg_query($db_conn, $query);
								$row = pg_fetch_row($result);
								echo $row[0];
							}
							?>
						</label>
					</td>
					<td align ="right" style="width:20%;">
						<form action="changepass.php" method="post" align ="right">
							<button type="submit" class="logoutbtn" align ="right">Change password</button>
						</form>
					</td>
					<td align ="right" style="width:20%;">
						<form action="logout.php" method="post" align ="right">
							<button type="submit" class="logoutbtn" align ="right">Logout</button>
						</form>
					</td>
				</tr>
			</table>
		</div>
			<table table width="95%">
				<tr>
				<th colspan="3">Users' Management</th>
			</tr>
		</table>
		<form action="userstodb.php" method="post">
			<table width="100%" border="1" class="sortable">
				<thead>
					<tr>
						<th><button type="button"class="sortbtn">ID<span aria-hidden="true"></span></button></th>
						<th aria-sort="ascending"><button class="sortbtn">Activity ID<span aria-hidden="true"></span></button></th>
						<th><button type="button"class="sortbtn">Activity Data from DB<span aria-hidden="true"></span></button></th>
						<th><button type="button"class="sortbtn">User Data<span aria-hidden="true"></span></button></th>
						<th><button type="button"class="sortbtn">Activity Data<span aria-hidden="true"></span></button></th>
						<th><button type="button"class="sortbtn">Created At<span aria-hidden="true"></span></button></th>
						<th><button type="button"class="sortbtn">Updated At<span aria-hidden="true"></span></button></th>
					</tr>
				</thead>
				<tbody>
					<?php
					if (!$db_conn){
						echo "Error: Unable to open database\n:";
					}
					else
					{
						$query = "SELECT * FROM activitiesdata ORDER BY id";
						$result = pg_query($db_conn, $query);
						while ($row = pg_fetch_row($result))
						{
							if ($row[0] !=0) {
							echo '
								<tr>
									<td>'.$row[0].'</td>
									<td>'.$row[2].'</td>
									<td>'.$row[3].'</td>
									<td>'.$row[4].'</td>
									<td>'.$row[5].'</td>
									<td>'.$row[6].'</td>
									<td>'.$row[7].'</td>
								</tr>';
							}
						}
					}
					?>
				</tbody>
			</table>
		</form>
    <br>
		<form action="mainpage.php" method="post">	
      <button type="submit" id="back" name="back">Back</button>
		</form>
	</div>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	<script type="text/javascript">
		setInterval(function(){
			$.post('refresh_session.php');
		},600000); //refreshes the session every 10 minutes
	</script>
	<script>
	
	/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 *
 *   File:   sortable-table.js
 *
 *   Desc:   Adds sorting to a HTML data table that implements ARIA Authoring Practices
 */

'use strict';

class SortableTable {
  constructor(tableNode) {
    this.tableNode = tableNode;

    this.columnHeaders = tableNode.querySelectorAll('thead th');

    this.sortColumns = [];

    for (var i = 0; i < this.columnHeaders.length; i++) {
      var ch = this.columnHeaders[i];
      var buttonNode = ch.querySelector('button');
      if (buttonNode) {
        this.sortColumns.push(i);
        buttonNode.setAttribute('data-column-index', i);
        buttonNode.addEventListener('click', this.handleClick.bind(this));
      }
    }

    this.optionCheckbox = document.querySelector(
      'input[type="checkbox"][value="show-unsorted-icon"]'
    );

    if (this.optionCheckbox) {
      this.optionCheckbox.addEventListener(
        'change',
        this.handleOptionChange.bind(this)
      );
      if (this.optionCheckbox.checked) {
        this.tableNode.classList.add('show-unsorted-icon');
      }
    }
  }

  setColumnHeaderSort(columnIndex) {
    if (typeof columnIndex === 'string') {
      columnIndex = parseInt(columnIndex);
    }

    for (var i = 0; i < this.columnHeaders.length; i++) {
      var ch = this.columnHeaders[i];
      var buttonNode = ch.querySelector('button');
      if (i === columnIndex) {
        var value = ch.getAttribute('aria-sort');
        if (value === 'descending') {
          ch.setAttribute('aria-sort', 'ascending');
          this.sortColumn(
            columnIndex,
            'ascending',
            ch.classList.contains('num')
          );
        } else {
          ch.setAttribute('aria-sort', 'descending');
          this.sortColumn(
            columnIndex,
            'descending',
            ch.classList.contains('num')
          );
        }
      } else {
        if (ch.hasAttribute('aria-sort') && buttonNode) {
          ch.removeAttribute('aria-sort');
        }
      }
    }
  }

  sortColumn(columnIndex, sortValue, isNumber) {
    function compareValues(a, b) {
      if (sortValue === 'ascending') {
        if (a.value === b.value) {
          return 0;
        } else {
          if (isNumber) {
            return a.value - b.value;
          } else {
            return a.value < b.value ? -1 : 1;
          }
        }
      } else {
        if (a.value === b.value) {
          return 0;
        } else {
          if (isNumber) {
            return b.value - a.value;
          } else {
            return a.value > b.value ? -1 : 1;
          }
        }
      }
    }

    if (typeof isNumber !== 'boolean') {
      isNumber = false;
    }

    var tbodyNode = this.tableNode.querySelector('tbody');
    var rowNodes = [];
    var dataCells = [];

    var rowNode = tbodyNode.firstElementChild;

    var index = 0;
    while (rowNode) {
      rowNodes.push(rowNode);
      var rowCells = rowNode.querySelectorAll('th, td');
      var dataCell = rowCells[columnIndex];

      var data = {};
      data.index = index;
      data.value = dataCell.textContent.toLowerCase().trim();
      if (isNumber) {
        data.value = parseFloat(data.value);
      }
      dataCells.push(data);
      rowNode = rowNode.nextElementSibling;
      index += 1;
    }

    dataCells.sort(compareValues);

    // remove rows
    while (tbodyNode.firstChild) {
      tbodyNode.removeChild(tbodyNode.lastChild);
    }

    // add sorted rows
    for (var i = 0; i < dataCells.length; i += 1) {
      tbodyNode.appendChild(rowNodes[dataCells[i].index]);
    }
  }

  /* EVENT HANDLERS */

  handleClick(event) {
    var tgt = event.currentTarget;
    this.setColumnHeaderSort(tgt.getAttribute('data-column-index'));
  }

  handleOptionChange(event) {
    var tgt = event.currentTarget;

    if (tgt.checked) {
      this.tableNode.classList.add('show-unsorted-icon');
    } else {
      this.tableNode.classList.remove('show-unsorted-icon');
    }
  }
}

// Initialize sortable table buttons
window.addEventListener('load', function () {
  var sortableTables = document.querySelectorAll('table.sortable');
  for (var i = 0; i < sortableTables.length; i++) {
    new SortableTable(sortableTables[i]);
  }
});
	</script>
</body>
</html>