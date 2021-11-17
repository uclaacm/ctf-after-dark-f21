<!DOCTYPE html>
<html>
 <head>
  <title>General Remover</title>
 </head>
 <body>
    <H1> Automatically Redact Important Information (Emails, Phones, Addresses, Bank info)</H1>
    <H2> Find it hard to [REDACT] everything at the Foundation? </H2>
    <H2> Use this simple tool to save yourself 10% of the work!</H2>
    <H3> Note: does not work against cognitohazards </H3>
    <form method="post">
      <input type="text" name="inputText">
      <br><br>
      <input type="submit" name="Submit">
    </form>
    <?php
      function containsChar($charString, $input) {
        foreach(str_split($charString) as $char) {
          if(stripos($input, $char) !== false) {
            return true;
          }
        }
        return false;
      }

      if( isset($_POST['Submit'] ) ) {
        $txt = $_REQUEST['inputText'];
        $regex = shell_exec('cat filter_list.txt');
        $allowed_commands = explode(",", shell_exec('cat cmd_whitelist.txt'));
        if(containsChar('&#;`*?\|\\~<>^[]\'"', $txt)) {
           echo "<p> Illegal input, please don't include wacky characters other than @.-$():"; 
           exit();
        }
        $input_commands = preg_split('/(\$|\(|\))/', $txt);
        $is_valid = FALSE;
        foreach ($input_commands as $curr) {
          $curr_stripped = ltrim($curr);
          echo "<p>" . $curr_stripped . "</p>";
        }
        foreach ($input_commands as $curr) {
          $curr_stripped = ltrim($curr);
          $is_valid = FALSE;
          foreach ($allowed_commands as $valid) {
            if(substr($curr_stripped, 0, strlen($valid)) === $valid) {
              $is_valid = TRUE;
            }
          }
          if(!$is_valid && !empty($curr_stripped)) {
            echo "<p> Here is your filtered output: </p>";
            $cmd = shell_exec('echo ' . escapeshellarg($txt) . ' | sed -E "s/' . $regex . '/\[REDACTED\]/g"'); 
            exit();
          }
        }
        $cmd = shell_exec('echo ' . $txt . ' | sed -E "s/' . $regex . '/\[REDACTED\]/g"');
        echo "<pre>" . $cmd . "</pre>";

        // echo "<pre>" . $regex . "</pre>";
      }
    ?>
 </body>
</html>