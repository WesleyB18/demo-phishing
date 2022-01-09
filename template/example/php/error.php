<?php
header('Content-Type: text/html');
{
  $denied = $_POST['Denied'];
  $una = $_POST['Una'];
  $time = $_POST['Time'];
  $unk = $_POST['Unk'];
  $support = 'Geolocation is not supported!';

  if (isset($denied))
  {
    $f = fopen('locate.txt', 'w+');
    fwrite($f, $denied);
    fclose($f);
  }
  elseif (isset($una))
  {
    $f = fopen('locate.txt', 'w+');
    fwrite($f, $una);
    fclose($f);
  }
  elseif (isset($time))
  {
    $f = fopen('locate.txt', 'w+');
    fwrite($f, $time);
    fclose($f);
  }
  elseif (isset($unk))
  {
    $f = fopen('locate.txt', 'w+');
    fwrite($f, $unk);
    fclose($f);
  }
  else
  {
    $f = fopen('locate.txt', 'w+');
    fwrite($f, $support);
    fclose($f);
  }
}
?>
