<?php

$host = "localhost";
$dbname = "gestion_pneus";
$user = "root";
$password = "";

$conn = new PDO(
    "mysql:host=$host;dbname=$dbname;charset=utf8",
    $user,
    $password
);

?>