<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $line = "";
    $line += clean($_POST["name"]) + ',';
    $line += clean($_POST["hours"]) + ',';

    $line += clean($_POST["Mon1"]) + ',';
    $line += clean($_POST["Tue1"]) + ',';
    $line += clean($_POST["Wed1"]) + ',';
    $line += clean($_POST["Thu1"]) + ',';
    $line += clean($_POST["Fri1"]) + ',';
    $line += clean($_POST["Sat1"]) + ',';
    $line += clean($_POST["Sun1"]) + ',';
    $line += clean($_POST["Mon2"]) + ',';
    $line += clean($_POST["Tue2"]) + ',';
    $line += clean($_POST["Wed2"]) + ',';
    $line += clean($_POST["Thu2"]) + ',';
    $line += clean($_POST["Fri2"]) + ',';
    $line += clean($_POST["Sat2"]) + ',';
    $line += clean($_POST["Sun2"]) + ',';
    $line += clean($_POST["Mon3"]) + ',';
    $line += clean($_POST["Tue3"]) + ',';
    $line += clean($_POST["Wed3"]) + ',';
    $line += clean($_POST["Thu3"]) + ',';
    $line += clean($_POST["Fri3"]) + ',';
    $line += clean($_POST["Sat3"]) + ',';
    $line += clean($_POST["Sun3"]);


    $fileout = fopen("avail_submits.csv", "a") or die("Unable to open file!");
    fwrite($fileout, "\n". $line);
    fclose($fileout);
  }

function clean($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
  }
?>

