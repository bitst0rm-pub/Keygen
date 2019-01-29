<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

if (isset($_POST["t"])) {
    $VERIFYV = "Uuc2UGZ3VibS5zdWJsltZXJnaY2VW1lLWxp";
    $s = htmlspecialchars($_POST["t"]);
    $d = base64_decode($s);
    $p = explode(",", $d);
    $a = array($p[0], $p[3], $p[2], $VERIFYV);
    $v = implode("/", $a);
    $r = sha1($v);

    echo json_encode(array(
        "result" => $r
    ));
} else {
    echo json_encode(array(
        "result" => true
    ));
}

?>
