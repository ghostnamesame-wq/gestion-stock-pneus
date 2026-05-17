<?php
include("config.php");

$req = $conn->query("SELECT * FROM stock_pneus");

?>

<!DOCTYPE html>

<html>

<head>

<title>Gestion Stock Pneus</title>

<style>

body{
    font-family: Arial;
    background:#f2f2f2;
    padding:20px;
}

table{
    width:100%;
    background:white;
    border-collapse: collapse;
}

th, td{
    border:1px solid #ccc;
    padding:10px;
    text-align:center;
}

th{
    background:#333;
    color:white;
}

</style>

</head>

<body>

<h1>Gestion Stock Pneus</h1>

<table>

<tr>
    <th>ID</th>
    <th>Marque</th>
    <th>Dimension</th>
    <th>Type</th>
    <th>Quantité</th>
    <th>Prix</th>
</tr>

<?php while($row = $req->fetch()) { ?>

<tr>

<td><?= $row['id'] ?></td>
<td><?= $row['marque'] ?></td>
<td><?= $row['dimension'] ?></td>
<td><?= $row['type_pneu'] ?></td>
<td><?= $row['quantite'] ?></td>
<td><?= $row['prix'] ?> €</td>

</tr>

<?php } ?>

</table>

</body>

</html>