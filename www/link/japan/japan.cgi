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
    $name
    <ul><li><a href="$url">$url</a></li><li>$comment</li></ul>
EOF
    } else {
      print << "EOF";
<ul>
  <li>
    $name
    <img style="float: left; margin-right: 3em;" src="http://capture.heartrails.com/200x150/cool?$url" alt="$name" width="128" height="128" />
    <ul>
      <li><a href="$url">$url</a></li>
      $comment
    </ul>
  </li>
</ul>
<br style="clear: both;"/>
EOF
    }
  }
}

close(IN);
exit(0);





