#!/usr/bin/perl

my $agent = $ENV{'HTTP_USER_AGENT'};
my $is_mobile = FALSE;

if ($agent =~ /(DoCoMo|J-PHONE|ASTEL|KDDI)/){
  $is_mobile = TRUE;
}

my $file = 'japan.csv';
print "Cntent-Type: text/plain\n\n";

open(IN, "<$file");
while(my $line = <IN>) {
  chomp($line);
  my ($city, $name, $url, $comment) = split(/,/, $line, 4);
  if($comment ne "") {
    $comment = "<li>$comment</li>";
  }
  if($city eq $ARGV[0]) {
    if($is_mobile eq TRUE) {
      print << "EOF";
  <li>
    $name
    <ul><li><a href="$url">$url</a></li>$comment</ul>
  </li>
EOF
    } else {
      print << "EOF";
  <li>
    $name
    <ul><li><a href="$url">$url</a></li>$comment<li style="list-style:none;"><a href="$url"><img src="http://capture.heartrails.com/free/shorten?$url" alt="$name" width="128" height="128" /></a></li></ul>
  </li>
EOF
    }
  }
}

close(IN);
exit(0);
