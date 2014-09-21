#!/usr/local/bin/perl

#┌─────────────────────────────────
#│  TEXT COUNTER v2.0 (2002/09/17)
#│  日計式テキストカウンタ (SSI式)
#│  Copyright(C) Kent Web 2002
#│  webmaster@kent-web.com
#│  http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'TEXT COUNTER v2.0';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────
#
# [タグの記述例]
#
# <!--#exec cgi="./cgi-bin/txcount.cgi"-->
#
#
# [ディレクトリ構成例]
#
# public_html / index.html ← ここにタグ記述：カウンタ表示
#     |
#     +-- cgi-bin / txcount.cgi [755]
#            |      txcount.tmp [644]
#            |      txcount.log [666]
#            |      txcount.txt [666]
#            |
#            +-- lock [777] /
#
#    ※テンプレートファイル「txcount.tmp」を使用しない場合には
#      「txcount.tmp」は不要 (ファイルが存在しなければ自動的に
#       テキスト表示します）
#
# [チェックモード]
#
# 引数に「check」をつけて呼び出す
#
# 例：http://～～/txcount.cgi?check


#============#
#  設定項目  #
#============#

# ログファイル
$logfile = './txcount.log';

# 日次ファイル
$dayfile = './txcount.txt';

# テンプレートファイル
$tmpfile = './txcount.tmp';

# 桁数 (0 の場合桁数指定なし）
$digit = 0;

# 3桁区切り表示 (0=no 1=yes)
# → カウンタ値4桁以上で有効
$divide = 0;

# ロックファイル機構
#  0 : なし
#  1 : する → symlink関数式
#  2 : する → mkdir関数式（WinNTサーバなど symlinkが使用できない環境用）
$lockkey = 1;

# ロックファイル名
$lockfile = './lock/lock.dat';

# IPアドレスチェック (0=no 1=yes)
# → 重複カウント拒否
$ip_check = 0;

#============#
#  設定完了  #
#============#

# チェックモード
if ($ENV{'QUERY_STRING'} eq "check") { &check; }

# IPアドレス取得
$addr = $ENV{'REMOTE_ADDR'};

# ヘッダ出力
print "Content-type: text/plain\n\n";

# ロック開始
$lockflag=0;
&lock if ($lockkey);

# 記録ログ
open(IN,"$logfile") || &error("Open Error $logfile");
$data1 = <IN>;
close(IN);
($count, $ip) = split(/:/, $data1);

# 日次ログ
open(IN,"$dayfile") || &error("Open Error $dayfile");
$data2 = <IN>;
close(IN);
($day, $yes, $tod) = split(/:/, $data2);

# IPチェック（重複カウント防止）
unless ($ip_check && $addr eq $ip) {

	# 記録ログ
	$count++;
	open(OUT,">$logfile") || &error("Write Error $logfile");
	print OUT "$count\:$addr";
	close(OUT);

	# 本日の日を取得
	$ENV{'TZ'} = "JST-9";
	$mday = (localtime(time))[3];

	# 日替わりの場合
	if ($day != $mday) {
		$yes = $tod;
		$tod = 0;
	}

	# 日次ログ
	$tod++;
	open(OUT,">$dayfile") || &error("Write Error $dayfile");
	print OUT "$mday\:$yes\:$tod";
	close(OUT);
}

# ロック解除
&unlock if ($lockkey);

if (length($count) > 3) { $lenflag=1; }
else { $lenflag=0; }

# 桁数調整
if ($digit != 0) {
	while(length($count) < $digit) { $count = '0' . $count; }
}

# 桁区切り
if ($divide) {
	if ($lenflag) { $count = &divide($count); }
	$yes = &divide($yes);
	$tod = &divide($tod);
}

# テンプレート読み込み
open(IN,"$tmpfile") || &error("Open Error $tmpfile");
while (<IN>) {
	s/<!-- count -->/$count/;
	s/<!-- yesterday -->/$yes/;
	s/<!-- today -->/$tod/;

	print;
}
close(IN);
exit;

#--------------#
#  エラー処理  #
#--------------#
sub error {
	&unlock if ($lockflag);

	print "ERROR : $_[0]";
	exit;
}

#--------------#
#  ロック処理  #
#--------------#
sub lock {
	# 1分以上古いロックは削除する
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	local($retry)=5;
	# symlink関数式ロック
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag=1;
}

#--------------#
#  ロック解除  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
	$lockflag=0;
}

#----------------#
#  桁区切り処理  #
#----------------#
sub divide {
	local($_) = $_[0];
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	$_;
}

#------------------#
#  チェックモード  #
#------------------#
sub check {
	print "Content-type: text/html\n\n",
	"<html><head><title>$ver</title></head>\n",
	"<body><h2>Check Mode : $ver</h2><UL>\n";

	local($i)=0;
	foreach ($logfile, $dayfile, $tmpfile) {
		$i++;

		# パス
		if (-e $_) {
			print "<LI>パス：$_ → OK\n";

			# パーミッション
			if ($i < 3) {
				if (-r $_ && -w $_) {
					print "<LI>パーミッション：$_ → OK\n";
				} else {
					print "<LI>パーミッション：$_ → NG\n";
				}
			}
		} else {
			print "<LI><LI>パス：$_ → NG\n";
		}
	}

	# ロックディレクトリ
	print "<LI>ロック形式：";
	if ($lockkey == 0) { print "ロック設定なし\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }

		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>ロックディレクトリ：$lockdir\n";

		if (-d $lockdir) {
			print "<LI>ロックディレクトリのパス：OK\n";

			if (-r $lockdir && -w $lockdir && -x $lockdir) {
				print "<LI>ロックディレクトリのパーミッション：OK\n";
			} else {
				print "<LI>ロックディレクトリのパーミッション：NG → $lockdir\n";
			}
		} else {
			print "<LI>ロックディレクトリのパス：NG → $lockdir\n";
		}
	}

	print "</UL>\n</body></html>\n";
	exit;
}

__END__

