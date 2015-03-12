<?php
// files
$file_name_in = $_FILES["xml_file"]["name"];
$file_name = explode(".", $file_name_in);

// evaluation script
$eval = "../scripts/Evaluation.py";
$gen = "../scripts/XMLGenerator.py";
$python_result_gen = null;
$python_result_eval = null;

// variables
$system = addslashes($_POST["system_name"]);
$configuration = addslashes($_POST["configuration"]);
$type = $_POST["evaluation"];
$err = 0;
$no_name = "true";
$method = 0; // for evaluate

// generate button clicked?
if (isset($_POST["generate"]))
{
	$method = 1; // for generate
}

// test or training
if (strcmp($type, "test") == 0)
{
	if (preg_match("/\"/", $system) || preg_match("/\"/", $configuration)) 
	{
		echo "Double quotation marks are not allowed.<br />";
		exit();
	}
	// check system name
	if (strcmp($system, "") == 0)
	{
		echo "Please fill out the system name.<br />";
		exit();
	}
	else
	{
		// create default configuration name if none exists
		if (strcmp($configuration, "") == 0)
		{
			$configuration = "empty";
		}
		// check if names are individual
		$query = "SELECT * FROM `qald`.`overall_evaluation` WHERE system_name = '" . $system . "' AND config_name = '" . $configuration . "'";
		include("connect.php");
		$result = @mysql_query($query);
		if ($ligne = @mysql_fetch_object($result)) {
			mysql_free_result($result);
			echo "This combination of system name and configuration already exists. Please choose another configuration.<br />";
			exit();
		}
		mysql_close($db);
	}	
}

// check data and input file
$xml = "xml";
if (strcmp($xml, $file_name[1]) == 0)
{
	$err = 0;
}
else
{
	$err = 1;
	echo "Please upload a correct xml file.<br />";
	exit();		
}

// upload file
if ($err != 1)
{
	// trying to find individual file name	
	$timestamp = mktime(time());	
	for ($timestamp; (strcmp($no_name, "true") == 0); $timestamp++)
	{	
		$server_target = "upload/" . $file_name[0] . "_" . $timestamp . ".xml";
		if (!file_exists($server_target))
		{
			$no_name = "false";
			if (@move_uploaded_file($_FILES["xml_file"]["tmp_name"], $server_target))
			{
				$err = 0;
			} 
			else
			{
				$err = 1;
				echo "Could not upload file. Please try again later.<br />";
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
	$type_of_file = substr($python_result_gen[1], -3);
	if (strcmp($type_of_file, "xml") == 0)
	{
		// further evaluation with given xml file
		$server_target = $python_result_gen[1];			
	}
	else
	{
		// show error message of python script
		Header("Location: " . $python_result_gen[0]);
		exit();
	}
}

// compare file
if ($err != 1)
{
	// test or training
	if (strcmp($type, "test") == 0)
	{
		// execute python file
		@exec(escapeshellcmd('python ' . $eval . ' "' . $server_target . '" "1" "' . $system . '" "' . $configuration . '"'), $python_result_eval);

		// routine for reading file entries
		// connect to database
		include("connect.php");

		// check type of file (html or txt)
		$type_of_file = substr($python_result_eval[0], -4);
		if (strcmp($type_of_file, "html") == 0)
		{
			// show error message of python script
			Header("Location: " . $python_result_eval[0]);
			exit();
		}

		// open file
		$file = @fopen($python_result_eval[0],'r') or die ("Cannot read file."); 

		// declare overall variables
		$input_file = $server_target;
		$output_file = $python_result_eval[0];
		$system_name = "";
		$config_name = "";
		$number_total = 0;
		$number_right = 0;
		$number_wrong = 0;
		$precision = 0.0;
		$recall = 0.0;
		$f_measure = 0.0;
		$system_id = 0;
		$err = 0;

		// read file, save variables, save to database
		$count = 0;	
		while ($content = fgets($file,1024))
		{		
			// explode line
			$entry = explode(";", $content);

			// system name and configuration
			if ($count == 0)
			{
				$system_name = stripslashes(trim($entry[0]));
				$config_name = stripslashes(trim($entry[1]));
			}

			// overall evaluation
			else if ($count == 1)
			{
				// get variables
				$number_total = trim($entry[0]);
				$number_right = trim($entry[1]);
				$number_wrong = trim($entry[2]);
				$precision = trim($entry[3]);
				$recall = trim($entry[4]);
				$f_measure = trim($entry[5]);
	
				// save to database
				$column = "`system_name`, `config_name`, `input_file_name`, `output_file_name`, `number_total`, `number_right`, `number_wrong`, `precision`, `recall`, `f_measure`";
				$entries = "'$system_name', '$config_name', '$input_file', '$output_file', '$number_total', '$number_right', '$number_wrong', '$precision', '$recall', '$f_measure'";
				$overall_insert = "INSERT INTO `qald`.`overall_evaluation` ($column) VALUES ($entries)";
				@mysql_query($overall_insert);
			
				// get system id
				$find_out_id = "SELECT id FROM `qald`.`overall_evaluation` WHERE system_name = '" . $system_name . "' AND config_name = '" . $config_name . "'";
				$result = @mysql_query($find_out_id);
				if ($ligne = @mysql_fetch_object($result))
				{
					$system_id = $ligne->id; 
				}
				else
				{
					echo "A problem occured. Please report this to the qald organization team.";
					$err = 1;
					exit();
				}
			}

			// single evaluation
			else
			{
				// get variables
				$question_id = trim($entry[0]);
				$question = trim($entry[1]);
				$precision = trim($entry[2]);
				$recall = trim($entry[3]);
				$f_measure = trim($entry[4]);
	
				// save to database
				$column = "`system_id`, `question_id`, `question`, `precision`, `recall`, `f_measure`";
				$entries = "'$system_id', '$question_id', '$question', '$precision', '$recall', '$f_measure'";
				$single_insert = "INSERT INTO `qald`.`single_evaluation` ($column) VALUES ($entries)";
				@mysql_query($single_insert);
			}
			$count++;
		}

		fclose($file);

		// close database
		@mysql_close($db); 

		if ($err == 0)
		{
			echo "Thank you for taking part in this contest.";
		}
	}
	else
	{
		// execute python file
		@exec(escapeshellcmd("python " . $eval . " '" . $server_target . "' '0' 'system' 'config'"), $python_result_eval);
		# print_r($python_result_eval);
		$out = $python_result_eval[0];
		Header("Location: $out");
	}
}
exit();
?>
