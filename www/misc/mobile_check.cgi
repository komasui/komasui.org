#!/usr/local/bin/perl

# USER_AGENTが携帯っぽかったら"_m"を吐く。
# それだけ。SSIからの利用を想定。

$agent = $ENV{'HTTP_USER_AGENT'};

if ($agent =~ /(DoCoMo|J-PHONE|ASTEL|KDDI)/){
  print "Content-type: text/html\n\n";
  print "_m";
}else{
  print "Content-type: text/html\n\n";
}
exit 0;