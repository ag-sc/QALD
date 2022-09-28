<html>
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
   <title>Question Answering over Linked Data</title>
   <link rel="stylesheet" type="text/css" href="qald.css">
<!--   <link rel="icon" href="images/qald_icon.png" type="image/png" /> -->
</head>
<body>

<?php

if (isset($_GET['q'])) {
    $q = $_GET['q']; }
 else {
    $q = "home"; }
 if (isset($_GET['x'])) {
    $x = htmlspecialchars($_GET['x']);
 }
 else {
    if ($q == "home") { $x = "home"; }
    else { $x = "motivation"; }
 }

 $link = $q . "/website/" . $x . ".html";

?>

<div id="container">

<div id="menu">

 <p> <a href='index.php?x=home&q=home'>Home</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> &nbsp; </p>

 <?php
 if ($q == "home") {
 echo "
 <p> <a href='index.php?x=benchmark&q=".$q."'>Benchmark</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=publications&q=".$q."'>Publications</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=contact&q=".$q."'>Contact</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> &nbsp; </p>";
 }
 if ($q == "10") {
  header("location:https://www.nliwod.org/challenge");
   }
if ($q == "9") {
    header("location:https://www.nliwod.org/past-workshops/2018/home.html");
     }
if ($q == "8") {
    header("location:https://project-hobbit.eu/challenges/qald-8-challenge/");
     }

if ($q == "7") {
    header("location:https://project-hobbit.eu/challenges/qald2017/");
     }
     
 if ($q == "6") {
 echo "
 <p> <a href='index.php?x=motivation&q=".$q."'>Motivation</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=organization&q=".$q."'>Organization</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=challenge&q=".$q."'>Challenge overview</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=evaltool&q=".$q."'>Evaluation tool</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=submission&q=".$q."'>Paper submission</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=proceedings&q=".$q."'>Proceedings</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=contact&q=".$q."'>Contact</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> &nbsp; </p>";
 }
 if ($q == "5") {
 echo "
 <p> <a href='index.php?x=motivation&q=".$q."'>Motivation</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=organization&q=".$q."'>Organization</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=challenge&q=".$q."'>Lab overview</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=evaltool&q=".$q."'>Evaluation tool</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=proceedings&q=".$q."'>Proceedings</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=contact&q=".$q."'>Contact</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> &nbsp; </p>";
 }
 if ($q == "4") {
 echo "
 <p> <a href='index.php?x=motivation&q=".$q."'>Motivation</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=organization&q=".$q."'>Organization</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=challenge&q=".$q."'>Lab overview</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=task1&q=".$q."'>Task 1</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=task2&q=".$q."'>Task 2</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=task3&q=".$q."'>Task 3</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=evaltool&q=".$q."'>Evaluation tool</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=proceedings&q=".$q."'>Proceedings</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=contact&q=".$q."'>Contact</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> &nbsp; </p>";
 }
 if ($q == "3") {
 echo "
 <p> <a href='index.php?x=motivation&q=".$q."'>Motivation</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=organization&q=".$q."'>Organization</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=program&q=".$q."'>Program</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=challenge&q=".$q."'>Lab overview</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=task1&q=".$q."'>Task 1</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=task2&q=".$q."'>Task 2</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=evaltool&q=".$q."'>Evaluation tool</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=proceedings&q=".$q."'>Proceedings</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=contact&q=".$q."'>Contact</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> &nbsp; </p>";
 }
 if ($q == "2" || $q == "1") {
 echo "
 <p> <a href='index.php?x=motivation&q=".$q."'>Motivation</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=organization&q=".$q."'>Organization</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=cfp&q=".$q."'>Call for Papers</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=submission&q=".$q."'>Submission</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=challenge&q=".$q."'>Open Challenge</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=evaltool&q=".$q."'>Evaluation tool</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=program&q=".$q."'>Program</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=proceedings&q=".$q."'>Proceedings</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=contact&q=".$q."'>Contact</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> &nbsp; </p>";
 }
 ?>

 <?php
 echo "<p><b>Current challenge:</b></p>
 <p> <a href='index.php?x=".$x."&q=10'>QALD-10</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p><b>Previous challenges:</b></p>
 <p> <a href='index.php?x=".$x."&q=9'>QALD-9</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=8'>QALD-8</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=7'>QALD-7</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=6'>QALD-6</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=5'>QALD-5</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=4'>QALD-4</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=3'>QALD-3</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=2'>QALD-2</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p> <a href='index.php?x=".$x."&q=1'>QALD-1</a> <img src='pictures/list_arrow_gray.gif'> </p>
 <p>&nbsp;</p>
 <p><b>Sponsor:</b></p>
 <p>
 <a href='http://www.orange.com/en/home'><img src='pictures/orange_logo.png' width='60px' border='0' alt='Orange' /></a>
 </p>
 <p>&nbsp;</p>";
 ?>
</div>

<div id="total">

 <div id="head">
 <?php
{
   echo "<img src='pictures/qald_header.png' width='800px' height='250px' border='0'
         alt='QALD : Question Answering Over Linked Data' />"; }
 ?>
</div>

 <div id="bar">

 <div class="alignleft">
 <?php
  switch ($x) {
  	case "cfp": $nav = "Call for Papers"; break;
	case "challenge": $nav = "Open Challenge"; break;
	case "evaltool": $nav = "Evaluation Tool"; break;
	default: $nav = ucfirst($x);
  }

  if ($q == "1") { echo "&nbsp;&nbsp;QALD-1 &raquo; " . $nav ; }
  if ($q == "2") { echo "&nbsp;&nbsp;QALD-2 &raquo; " . $nav ; }
  if ($q == "3") { echo "&nbsp;&nbsp;QALD-3 &raquo; " . $nav ; }
  if ($q == "4") { echo "&nbsp;&nbsp;QALD-4 &raquo; " . $nav ; }
  if ($q == "5") { echo "&nbsp;&nbsp;QALD-5 &raquo; " . $nav ; }
 ?>
 </div>
 <div class="alignright">

 <?php
  if ($q == "1")
    echo "May 30, 2011 &sdot; Co-located with: <a href='http://www.eswc2011.org' class='sel'><b>ESWC 2011&nbsp;&nbsp;</b></a>";
  if ($q == "2")
    echo "May 28, 2012 &sdot; Co-located with: <a href='http://2012.eswc-conferences.org' class='sel'><b>ESWC 2012&nbsp;&nbsp;</b></a>";
  if ($q == "3")
    echo "September 2013 &sdot; Co-located with: <a href='http://celct.fbk.eu/clef2013/index.php' class='sel'><b>CLEF 2013&nbsp;&nbsp;</b></a>";
  if ($q == "4")
    echo "September 2014 &sdot; Part of: <a href='http://nlp.uned.es/clef-qa/' class='sel'><b>QA Track at CLEF 2014&nbsp;&nbsp;</b></a>";
  if ($q == "5")
    echo "September 2015 &sdot; Part of: <a href='http://nlp.uned.es/clef-qa/' class='sel'><b>QA Track at CLEF 2015&nbsp;&nbsp;</b></a>";
  if ($q == "7")
    echo "May 2017 &sdot; Part of: <a href='http://2017.eswc-conferences.org/' class='sel'><b>Challenge at ESWC 2017&nbsp;&nbsp;</b></a>";
  if ($q == "8")
    echo "October 2017 &sdot; Part of: <a href='http://iswc2017.semanticweb.org' class='sel'><b>Part of NLIWOD workshop at ISWC 2017&nbsp;&nbsp;</b></a>";
  if ($q == "9")
    echo "October 2018 &sdot; Part of: <a href='http://iswc2018.semanticweb.org' class='sel'><b>Part of NLIWOD workshop at ISWC 2018&nbsp;&nbsp;</b></a>";
  if ($q == "10")
    echo "May 2022 &sdot; Part of: <a href='https://www.nliwod.org/challenge' class='sel'><b>Part of NLIWOD workshop at ESWC 2022&nbsp;&nbsp;</b></a>";

 ?>
 </div>
 <div style="clear: both;"></div>

 </div>

 <div id="main">
 <!-- MAIN CONTENT -->

 <?php

  if ($q == "3" and ($x == "submission" or $x == "cfp")) {
      $link = "3/website/motivation.html";
  }
  if (($q == "1" or $q == "2") and ($x == "task1" or $x == "task2")) {
      $link = $q . "/website/motivation.html";
  }
  if ($q != "home" and ($x == "home" or $x == "benchmark" or $x == "publications")) {
     $link = $q . "/website/motivation.html";
  }

  include $link;
 ?>
 </div>

</div> <!-- total -->

</div> <!-- container -->

</body>
</html>
