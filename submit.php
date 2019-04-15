<?php

function clean($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
  }

function check_get($name) {
	if (isset($_POST[$name])) {
		return '1,';
	} else {
		return '0,';
	}
}


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $line = "";
    $line = $line . (clean($_POST["firstname"]));
    $line = $line . " ";
    $line = $line . (clean($_POST["lastname"] . ','));
    
    $line = $line . (clean($_POST["hours"] . ','));

    $line = $line . check_get("Aldershot");
    $line = $line . check_get("Tansley");
    $line = $line . check_get("Centennial");

    $line = $line . check_get("Mon1");
    $line = $line . check_get("Mon2");
    $line = $line . check_get("Mon3");
    $line = $line . check_get("Tue1");
    $line = $line . check_get("Tue2");
    $line = $line . check_get("Tue3");
    $line = $line . check_get("Wed1");
    $line = $line . check_get("Wed2");
    $line = $line . check_get("Wed3");
    $line = $line . check_get("Thu1");
    $line = $line . check_get("Thu2");
    $line = $line . check_get("Thu3");
    $line = $line . check_get("Fri1");
    $line = $line . check_get("Fri2");
    $line = $line . check_get("Fri3");
    $line = $line . check_get("Sat1");
    $line = $line . check_get("Sat2");
    $line = $line . check_get("Sat3");
    $line = $line . check_get("Sun1");
    $line = $line . check_get("Sun2");
    $line = $line . check_get("Sun3");

    $fileout = fopen(".submissions.csv", "a") or die("Unable to open file!");
    fwrite($fileout, $line.'\n');
    fclose($fileout);

    header("location:./submitted.html");
  }

?>

