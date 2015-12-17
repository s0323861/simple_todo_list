#!/usr/bin/perl

use Encode qw(is_utf8);
use CGI qw(:standard);
use Jcode;
use File::Basename;

# フォーム内のどのボタンが押されたのかチェック用
my $button = param("button");

# 未完了と完了タブのHTMLタグ用変数
my($tag1, $tag2);

# 未完了のTODO数をカウントするための変数
my $tag1_cnt = 0;

# 現在日時を取得する
my @youbi = ('日', '月', '火', '水', '木', '金', '土');
my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$year += 1900;
$mon += 1;
my $stamp = $year . "年" . $mon . "月" . $mday . "日(" . $youbi[$wday] . ")";

# 画面に表示される名前
$nickname = "Anonymous";

# タイトル
my $headertitle = $nickname . "さんのToDoリスト";

# 個人のデータファイル名
my $file = "./data/sample.txt";

# データファイルへ書き込む項目(ユニークキー, 完了フラグ(0 OR 1), TODO内容, 完了日)
my($line0, $line1, $line2, $line3);
$line0 = param("code");
$line1 = param("flag");
$line2 = param("todo");
$line3 = param("stamp");
my $line = $line0 . "\t" . $line1 . "\t" . $line2 . "\t" . $line3;

# 新規追加のボタンが押された場合
if($button eq "add" and $line2 ne ""){

  open(OUT, ">>" . $file);
  flock(OUT, 2);
  # ファイルの先頭に移動する
  seek(OUT, 0, 0);
  print OUT &randstr(4) . "\t" . $line1 . "\t" . $line2 . "\t" . $line3 . "\n";
  flock(OUT, 8);
  close(OUT);

# 更新ボタンを押して遷移してきた場合
}elsif($button eq "refresh" and $line2 ne ""){

  # ファイルを開く
  open(IN, $file);
  flock(IN, 1);
  my @all = <IN>;
  close(IN);

  my @up;
  foreach my $bun (@all){
    my($tmp0, $tmp1, $tmp2, $tmp3) = (split(/\t/, $bun));
    if($tmp0 eq $line0){
      push(@up, $line . "\n");
    }else{
      push(@up, $bun);
    }
  }

  # ファイルに書き込む
  open(OUT, ">" . $file);
  flock(OUT, 2);
  truncate(OUT, 0);
  seek(OUT, 0, 0);
  foreach(@up){
    print OUT $_;
  }
  flock(OUT, 8);
  close(OUT);

# 完了ボタンを押した場合
}elsif($button eq "done" and $line2 ne ""){

  # ファイルを開く
  open(IN, $file);
  flock(IN, 1);
  my @all = <IN>;
  close(IN);

  my @up;
  foreach my $bun (@all){
    my($tmp0, $tmp1, $tmp2, $tmp3) = (split(/\t/, $bun));
    if($tmp0 eq $line0){
      push(@up, $line0 . "\t" . "1" . "\t" . $line2 . "\t" . $stamp . "\n");
    }else{
      push(@up, $bun);
    }
  }

  # ファイルに書き込む
  open(OUT, ">" . $file);
  flock(OUT, 2);
  truncate(OUT, 0);
  seek(OUT, 0, 0);
  foreach(@up){
    print OUT $_;
  }
  flock(OUT, 8);
  close(OUT);

# 削除ボタンを押した場合
}elsif($button eq "delete"){

  # ファイルを開く
  open(IN, $file);
  flock(IN, 1);
  my @all = <IN>;
  close(IN);

  my @up;
  foreach my $bun (@all){
    my($tmp0, $tmp1, $tmp2, $tmp3) = (split(/\t/, $bun));
    if($tmp0 eq $line0){

    }else{
      push(@up, $bun);
    }
  }

  # ファイルに書き込む
  open(OUT, ">" . $file);
  flock(OUT, 2);
  truncate(OUT, 0);
  seek(OUT, 0, 0);
  foreach(@up){
    print OUT $_;
  }
  flock(OUT, 8);
  close(OUT);

# 元に戻すボタンを押した場合
}elsif($button eq "return"){

  # ファイルを開く
  open(IN, $file);
  flock(IN, 1);
  my @all = <IN>;
  close(IN);

  my @up;
  foreach my $bun (@all){
    my($tmp0, $tmp1, $tmp2, $tmp3) = (split(/\t/, $bun));
    if($tmp0 eq $line0){
      push(@up, $line0 . "\t" . "0" . "\t" . $tmp2 . "\t" . "\n");
    }else{
      push(@up, $bun);
    }
  }

  # ファイルに書き込む
  open(OUT, ">" . $file);
  flock(OUT, 2);
  truncate(OUT, 0);
  seek(OUT, 0, 0);
  foreach(@up){
    print OUT $_;
  }
  flock(OUT, 8);
  close(OUT);

}

# URLからこのファイル名を取得
my $q = CGI->new();
my $url = $q->url;
my $cginame = basename($url);

# ----------------------------
# 未完了と完了のHTMLを作成する
# ----------------------------
if (-e $file){
  open(IN, $file);
  flock(IN, 1);
  my @all = <IN>;
  close(IN);

  my $cnt = 1;
  foreach my $line (@all){
    chomp $line;
    my($tmp1, $tmp2, $tmp3, $tmp4) = (split(/\t/, $line));
    # 未完了のTODOの表示部分を作成
    if($tmp2 == 0){
      $tag1 .= <<EOF;
      <li class="list-group-item">
        <form method="post" action="$cginame" data-toggle="validator">
        <fieldset>
        <div class="form-group">
        <div class="input-group">
          <input type="text" name="todo" class="form-control" value="$tmp3" required>
          <input type="hidden" name="nickname" value="$nickname">
          <input type="hidden" name="code" value="$tmp1">
          <input type="hidden" name="flag" value="0">
          <span class="input-group-btn">
          <button type="submit" class="btn btn-primary" name="button" value="done"><span class="glyphicon glyphicon-ok"></span></button>
          <button type="submit" class="btn btn-warning" name="button" value="refresh"><span class="glyphicon glyphicon-refresh"></span></button>
          <button type="submit" class="btn btn-danger" name="button" value="delete"><span class="glyphicon glyphicon glyphicon-trash"></span></button>
          </span>
        </div>
        </div>
        </fieldset>
        </form>
      </li>
EOF
      $tag1_cnt++;

    # 完了したTODOの表示部分を作成
    }elsif($tmp2 == 1){
      $tag2 .= <<EOF;
      <li class="list-group-item">
        <label><small><span class="glyphicon glyphicon-time"></span> $tmp4</small></label>
        <form method="post" action="$cginame">
        <div class="input-group">
          <input type="hidden" name="nickname" value="$nickname">
          <input type="hidden" name="code" value="$tmp1">
          <input type="hidden" name="flag" value="1">
          <input type="text" name="todo" class="form-control" value="$tmp3" disabled>
          <span class="input-group-btn">
          <button type="submit" class="btn btn-primary" name="button" value="return"><i class="fa fa-reply"></i></button>
          </span>
        </div>
        </form>
      </li>
EOF

    }
  }
}

# 未完了のタスクがまだなかった場合の表示(アコーディオンを閉じる)
my($active1, $active2);
if($tag1_cnt == 0){
  $active1 = "glyphicon-chevron-down";
  $active2 = "";
}else{
  $active1 = "glyphicon-chevron-up";
  $active2 = " in";
}

# ==================================
# ユニークなキーを作成するための関数
# ==================================
sub randstr {
  my $length = $_[0];

  my @char_tmp=();

  # 配列にランダム生成する対象の文字列を格納
  # (以下は、小文字のa～z、大文字のA～Z、数字の0～9)
  push @char_tmp, ('a'..'z');
  push @char_tmp, (0..9);

  # 指定文字数分、ランダム文字列を生成する
  my $rand_str_tmp = '';
  my $i;
  for ($i=1; $i<=$length; $i++) {
    $rand_str_tmp .= $char_tmp[int(rand($#char_tmp+1))];
  }

  return $rand_str_tmp;
}

my $html = <<HTML;
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ToDoリスト - シンプルなタスク管理ツール</title>
<link rel="shortcut icon" href="favicon.ico">
<!-- Bootstrap -->
<link rel="stylesheet" href="./css/bootstrap.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">

<!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
  <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
<![endif]-->

<style type="text/css">
body { padding-top: 80px; }
\@media ( min-width: 768px ) {
  #banner {
    min-height: 200px;
    border-bottom: none;
  }
  .bs-docs-section {
    margin-top: 8em;
  }
  .bs-component {
    position: relative;
  }
  .bs-component .modal {
    position: relative;
    top: auto;
    right: auto;
    left: auto;
    bottom: auto;
    z-index: 1;
    display: block;
  }
  .bs-component .modal-dialog {
    width: 90%;
  }
  .bs-component .popover {
    position: relative;
    display: inline-block;
    width: 220px;
    margin: 20px;
  }
  .nav-tabs {
    margin-bottom: 15px;
  }
}
</style>

</head>
<body>

<header>
<div class="navbar navbar-default navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
    <a href="./" class="navbar-brand"><i class="fa fa-list-alt"></i> ToDoリスト</a>
    <button class="navbar-toggle" type="button" data-toggle="collapse" data-target="#navbar-main">
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
      <span class="icon-bar"></span>
    </button>
    </div>
    <div class="navbar-collapse collapse" id="navbar-main">
    </div>
  </div>
</div>
</header>

<div class="container">

  <div class="row">
    <div class="col-lg-12">
    <h1>$headertitle</h1>
    </div>
  </div>

  <div class="row">

    <form method="post" action="$cginame" data-toggle="validator">
    <div class="col-lg-12">
      <div class="well input-group">
        <input type="text" name="todo" class="form-control" placeholder="タスクの追加" required>
        <input type="hidden" name="nickname" value="$nickname">
        <input type="hidden" name="flag" value="0">
        <span class="input-group-btn">
        <button type="submit" class="btn btn-primary" name="button" value="add"><span class="glyphicon glyphicon-plus"></span></button>
        </span>
      </div><!-- /input-group -->
    </div>
    </form>

  </div>

  <div class="row">

    <div class="col-lg-12">

      <div id="menu">
        <div class="panel list-group">

          <a href="#menuOne" class="list-group-item" data-toggle="collapse" data-target="#menuOne" data-parent="#menu">
          <i class="fa fa-tasks"></i> 実行中のタスク
          <span class="glyphicon $active1 pull-right"></span>
          </a>
          <div id="menuOne" class="sublinks collapse$active2">
            <ul class="list-group">

$tag1

            </ul>
          </div>

          <a href="#menuTwo" class="list-group-item" data-toggle="collapse" data-target="#menuTwo" data-parent="#menu">
          <span class="glyphicon glyphicon-ok"></span> 完了したタスク
          <span class="glyphicon glyphicon-chevron-down pull-right"></span>
          </a>
          <div id="menuTwo" class="sublinks collapse">
            <ul class="list-group">

$tag2

            </ul>
          </div>

        </div>
      </div>

    </div>

  </div>

  <hr>

  <!-- Footer -->
  <footer>
  <div class="row">
    <div class="col-lg-12">
    <p>Copyright (C) 2015 <a href="http://tsukuba42195.top/">Akira Mukai</a><br>
    Released under the MIT license<br>
    <a href="http://opensource.org/licenses/mit-license.php" target="_blank">http://opensource.org/licenses/mit-license.php</a>
    </p>
    </div>
    <!-- /.col-lg-12 -->
  </div>
  <!-- /.row -->
  </footer>

</div> <!-- /container -->

<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<script src="./js/bootstrap.min.js"></script>
<script src="./js/validator.js"></script>

<script>
\$(function(){

  // Collapseイベント
  \$('#menuOne, #menuTwo')
  .on('show.bs.collapse', function() { //< 折り畳み開く処理
    \$('a[href="#' + this.id + '"]').find('span.glyphicon-chevron-down')
    .removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
  })
  .on('hide.bs.collapse', function() { //< 折り畳み閉じる処理
    \$('a[href="#' + this.id + '"]').find('span.glyphicon-chevron-up')
    .removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
  });
  // ハッシュリンクキャンセル
  \$('a[href="#menuOne"], a[href="#menuTwo"]').on('click', function(event) {
    event.preventDefault();
  });

});
</script>

</body>
</html>
HTML

print header( -type => 'text/html',-charset => 'UTF-8');
print $html;
