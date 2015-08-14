<meta charset="utf-8">
<?php

$mysqli = new mysqli('localhost', 'user', 'user');
if ($mysqli->connect_errno) {
    echo "Не удалось подключиться: " + $mysqli->connect_error;
    exit();
}
$mysqli->select_db("meteopi");
$query = "SELECT * FROM tttphl ORDER BY Timestamp DESC";
if (isset($_GET['limit'])){
	$query .= " LIMIT ?";
	$stmt = $mysqli->prepare($query);
	$stmt->bind_param("d", $_GET['limit']);
}
else {
	$stmt = $mysqli->prepare($query);
}

if ($stmt->execute()) {
	$stmt->bind_result($Timestamp, $TempOut, $TempIn, $TempAtt, $Pressure, $Humidity, $Lightness);
	
	echo "<table border='1'>
	<tr>
	<th>Время</th>
	<th>Температура<br />на улице</th>
	<th>Температура<br />в комнате</th>
	<th>Температура<br />на чердаке</th>
	<th>Давление</th>
	<th>Влажность</th>
	<th>Уровень<br />освещенности</th>
	</tr>";
	
	while($stmt->fetch()){
		echo "<tr>";
		echo "<td>" . $Timestamp . "</td>";
		echo "<td>" . number_format($TempOut, 2) . " °C</td>";
		echo "<td>" . number_format($TempIn, 1) . " °C</td>";
		echo "<td>" . number_format($TempAtt, 1) . " °C</td>";
		echo "<td>" . number_format($Pressure/1.333, 2) . " мм. рт. ст</td>";
		echo "<td>" . number_format($Humidity, 1) . " %</td>";
		echo "<td>" . number_format($Lightness, 3) . " Lux</td>";
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
