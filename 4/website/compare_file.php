<?php
// files
$file_name_in = $_FILES["file"]["name"];
$file_name = explode(".", $file_name_in);

// evaluation scripts
$task_eval = "../scripts/Evaluation.py";
$gen = "../scripts/XMLGeneratorWithoutQuery.py";
$python_result_gen = null;
$python_result_eval = null;

// variables
$system = addslashes($_POST["system_name"]);
$configuration = addslashes($_POST["configuration"]);
if (!empty($_POST["email"])) {
     $email = addslashes($_POST["email"]);
} else {
     $email = "NONE";
}
$task = $_POST["task"];
$type = $_POST["evaluation"];
$err = 0;
$no_name = "true";
$method = 0;

if (isset($_POST["generate"]) && $_POST["generate"])
{
	$method = 1; // for answer generation
}

// save information
$line = $system . " ( " . $configuration . " ) FROM " .$email . " : " . $file_name_in . "\n";
file_put_contents('statistics.txt',$line,FILE_APPEND);

// check file
if ($file_name_in !== "") {

	$ending = 'xml';

	if (strcmp($file_name[1], $ending) == 0)
	{
		$err = 0;
	}
	else
	{
		$err = 1;
		echo "Error: Please upload an XML file.<br /> ";
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
// check system name
if (strcmp($system, "") == 0)
{
	echo "Error: Please provide a system name.<br />";
	exit();
}
else
{
	// create default configuration name if none exists
	if (strcmp($configuration, "") == 0)
	{
		$configuration = "none";
	}
}	

// upload file
if ($err != 1)
{
	// trying to find individual file name	
	$timestamp = mktime(time());	
	for ($timestamp; (strcmp($no_name, "true") == 0); $timestamp++)
	{
		$server_target = "upload/" . $file_name[0] . "_" . $timestamp . "." . $file_name[1];
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
				echo "Error: Could not upload file. Please try again later.<br />";
				exit();
			}
		}
	}
}

// generate file
if ($method == 1)
{
 	@exec(escapeshellcmd('python ' . $gen . ' "' . $server_target . '"'), $python_result_gen);
	// check type of file (html or txt)
	$type_of_file = substr($python_result_gen[0], -3);
	if (strcmp($type_of_file, "xml") == 0)
	{
		// further evaluation with given xml file
		$server_target = $python_result_gen[0];			
	}
	else
	{
		// show error message of python script
 	        echo system('python ' . $gen . ' "' . $server_target . '" 2>&1');
		exit();
	}
}

// compare file
if ($err != 1)
{
	// test and training

	//chmod($server_target,0666);
	// execute python file
	$cmd = 'python ' . $task_eval . ' "' . $server_target . '" ' . $type . ' ' . $task . ' "' . $system . '" "' . $configuration . '"';
	@exec(escapeshellcmd($cmd),$python_result_eval);
        //chmod($server_target,0644);

	// check type of file (html or txt)
	$type_of_file = substr($python_result_eval[0], -4);
	if (strcmp($type_of_file,"html"))
	{
	   // show error message of python script
	   echo system($cmd . ' 2>&1');
	   exit();
	}
	else 
	{
           if (isset($python_result_eval[0])) 
	   { 
	     Header("Location: $python_result_eval[0]"); 
	   }
	   else {
	     echo "I'm puzzled. There was no result.";
	   }
	}
	
}
exit();
?>
