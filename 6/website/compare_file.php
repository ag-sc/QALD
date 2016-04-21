<?php
// files
$file_name_in = $_FILES["file"]["name"];
$file_name = explode(".", $file_name_in);
error_reporting(E_ALL);
// evaluation result
//$eval_result = null;

// variables
$system = addslashes($_POST["system_name"]);
$configuration = addslashes($_POST["configuration"]);
$email = addslashes($_POST["email"]);
$team = addslashes($_POST["team"]);
$affiliation = addslashes($_POST["affiliation"]);
$type = $_POST["evaluation"];
$err = 0;
$no_name = "true";
$method = 0;

// check file
if ($file_name_in !== "") {

	$ending = 'json';

	if (strcmp($file_name[1], $ending) == 0)
	{
		$err = 0;
	}
	else
	{
		$err = 1;
		echo "Error: Please upload a JSON file.<br /> ";
		exit();		
	}
}
else {
	$err = 1;
	echo "Error: No file specified.";
	exit();
}


// check system name and configuration for quotes
if (preg_match("/\"/", $system) || preg_match("/\"/", $configuration)) 
{
	echo "Error: Double quotation marks are not allowed.<br />";
	exit();
}

if (strcmp($type,"test") == 0) 
{
  // check system name
  if (strcmp($system, "") == 0)
  {
	echo "Error: Please provide a system name.<br />";
	exit();
  }
  // check team name
  if (strcmp($team, "") == 0)
  {
	echo "Error: Please provide a developer or team name.<br />";
	exit();
  } 
  // check email
  if (strcmp($email, "") == 0)
  {
	echo "Error: Please provide an email address.<br />";
	exit();
  } 
  // check affiliation
  if (strcmp($affiliation, "") == 0)
  {
	echo "Error: Please provide an affiliation.<br />";
	exit();
  }   
}

// create default configuration name if none exists
if (strcmp($configuration, "") == 0)
{
	$configuration = "none";
}
	
// upload file
if ($err != 1)
{
	// trying to find individual file name	
	$timestamp = mktime(time());	
	for ($timestamp; (strcmp($no_name, "true") == 0); $timestamp++)
	{
		$server_target = "upload/" . $system . "_" . $file_name[0] . "_" . $timestamp . "." . $file_name[1];
                file_put_contents('statistics.txt',"     " . $server_target,FILE_APPEND);
		
		if (!file_exists($server_target))
		{
			$no_name = "false";
			if (@move_uploaded_file($_FILES["file"]["tmp_name"], $server_target))
			{
				$err = 0;
			} 
			else
			{
				$err = 1;
				echo "Error: Could not upload file. Please try again later or contact Christina (cunger[at]cit-ec.uni-bielefeld.de).<br />";
				exit();
			}
		}
	}
}


// save information
$line = PHP_EOL . $system . " ( " . $configuration . " )" . PHP_EOL . $team . " FROM " . $affiliation . " (" . $email . "):" . PHP_EOL ;
file_put_contents('statistics.txt',$line,FILE_APPEND);


// compare file
if ($err != 1)
{
	// test and training

	//chmod($server_target,0666);
	// execute python file
	$cmd = 'ruby2.0 ../scripts/evaluation.rb "' . $server_target . '" "' . $system . '" "' . $configuration . '"';
	@exec(escapeshellcmd($cmd),$eval_result);
        //chmod($server_target,0644);

        if (isset($eval_result[0])) 
        {
           if (strcmp($type, "training") == 0) 
	   {
               include($eval_result[0]); 
	   }
	   if (strcmp($type, "test") == 0) 
	   { 
	       //echo "Thanks for submitting! Evaluation results will be made available on April 20.";
	       include($eval_result[0]);
	   }
	}
	else {
	   // show error message of evaluation script
	   echo system($cmd . ' 2>&1');
	   exit();
	}
	
}
exit();
?>
