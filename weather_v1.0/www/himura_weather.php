<?php 

$mysqli = new mysqli('localhost', 'user', 'user');
if ($mysqli->connect_errno) {
    echo "Не удалось подключиться: " + $mysqli->connect_error;
    exit();
}

$mysqli->select_db("himura_weather");

$query = "SELECT * FROM tp ORDER BY Timestamp DESC";
if (isset($_GET['limit'])){
	$query .= " LIMIT ?";
	$stmt = $mysqli->prepare($query);
	$stmt->bind_param("d", $_GET['limit']);
}else{
	$stmt = $mysqli->prepare($query);
}

if ($stmt->execute()) {
	$stmt->bind_result($Timestamp, $Temp, $Pressure);
	
	echo "<table border='1'>
	<tr>
	<th>Время</th>
	<th>Температура</th>
	<th>Давление</th>
	</tr>";
	
	while($stmt->fetch()){
		echo "<tr>";
		echo "<td>" . $Timestamp . "</td>";
		echo "<td>" . $Temp/10 . " °C</td>";
		echo "<td>" . number_format(($Pressure+101325)/100/1.333, 2) . " мм. рт. ст</td>";
		echo "</tr>";
	}
	echo "</table>";
    $stmt->close();
}
else{
	echo $mysqli->error;
}

$mysqli->close();

?>
