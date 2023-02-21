<?php
  session_start();

  // if you have more session-vars that are needed for login, also check 
  // if they are set and refresh them as well
  if (isset($_SESSION['token'])) { 
    $_SESSION['token'] = $_SESSION['token'];
  }
?>