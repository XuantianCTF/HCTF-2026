<?php

$flag = getenv('FLAG');
if ($flag === false || $flag === '') {
    $flag = 'flag{headers_are_more_useful_than_you_think}';
}

header('X-CTF-Flag: ' . $flag);
header('X-Challenge-Hint: inspect-the-redirect-chain');
header('Location: /final.php', true, 302);
exit;
