<strong>Let's make some noise!</strong><br/><br/>
Please send the request pattern in the url.<br/>
See for example: <i>?pattern=4:0.5-3:0.5-2:0.5-1:0.5-0:1-0:1</i><br/>
Mary had a Little Lamb: <i>?pattern=1:1.5-2:0.5-3:1-2:1-1:1-1:1-1:2-2:1-2:1-2:2-1:1-4:1-4:2-1:1.5-2:0.5-3:1-2:1-1:1-1:1-1:1-1:1-2:1-2:1-1:1-2:1-3:4</i><br/><br/>

<?php
$pattern = $_REQUEST['pattern'];
if(!validatePattern($pattern)) {
	echo "<strong>Invalid pattern! Please see the example.</strong>";
	exit;
}

echo "<strong>Current request:</strong> ".$pattern;

/* Run the pattern without waiting for response */
exec('python /home/pi/Python/chimeClient.py "'. $pattern .'" > /dev/null 2>/dev/null &');

/* Run the pattern and wait for the response 
exec('python /home/pi/Python/chimeClient.py "'. $pattern .'" ',$output,$return);
echo "<pre>";
foreach($output as $line)
	echo $line."\n";
echo "</pre>";
*/

function validatePattern($pattern) {
	if(preg_match('/^([0-4]{1}:\d{1}(\.\d{1,2}|)(-|$))+$/', $pattern))
		return true;
	else
		return false;
}

?> 