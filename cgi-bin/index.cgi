#!/bin/busybox ash

export MPD_HOST=$(cat bb-sh.conf | sed -n "1p" | grep . || echo "localhost")
export MPD_PORT=$(cat bb-sh.conf | sed -n "2p" | grep . || echo "6600")

echo "Content-type: text/html"
echo ""

cat << EOS
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width,initial-scale=1.0">
        <title>bb-MPD</title>
    </head>

	<header>
		<pre> 
    __    __          __  _______  ____ 
   / /_  / /_        /  |/  / __ \\/ __ \\
  / __ \/ __ \______/ /|_/ / /_/ / / / /
 / /_/ / /_/ /_____/ /  / / ____/ /_/ / 
/_.___/_.___/     /_/  /_/_/   /_____/  
                                        
<span>
MPD UI using busybox shellscript and CGi
</span>
	    </pre>

	</header>

    <body>
		<!-- 入力フォーム -->
		<form name="FORM" method="GET" >

			<p>$(echo "host:$MPD_HOST<br>port:$MPD_PORT<br>")</p>
			<!-- 音楽の操作ボタンをtableでレイアウト -->
			<table border="1" cellspacing="5">

				<!-- ヘッダ行 -->
				<thead>
					<tr>
						<th colspan=4>control button</th>
					</tr>
				</thead>

				<!-- 1行目 -->
				<tr>
					<td>
				 		<button name="button" value="status">status</button>
					</td>
					<td>
				 		<button name="button" value="volume -100">mute</button>
					</td>
					<td>
				 		<button name="button" value="volume -5">volume -5</button>
					</td>
					<td>
				 		<button name="button" value="volume +5">volume +5</button>
				</tr>	

				<!-- 2行目 -->
				<tr>
					<td>
						<button name="button" value="previous">previous</button>
					</td>
					<td>
				 		<button name="button" value="pause" >play/pause</button>
					</td>
					<td>
				 		<button name="button" value="stop">stop</button>
					</td>
					<td>
				 		<button name="button" value="next">next</button>
					</td>
				</tr>
				 
				<!-- 3行目 -->
				<tr>
					<td>
				 		<button name="button" value="repeat">repeat</button>
					</td>
					<td>
				 		<button name="button" value="random">random</button>
					</td>
					<td>
				 		<button name="button" value="single">single</button>
					</td>
					<td>
				 		<button name="button" value="shuffle">shuffle</button>
					</td>
				</tr>

				<!-- 4行目 -->
				<tr>
					<td>
				 		<button name="button" value="clear">clear</button>
					</td>
					<td>
				 		<button name="button" value="update">update</button>
					</td>
					<td>
				 		<button name="button" value="seek -5%">seek -5%</button>
					</td>
					<td>
				 		<button name="button" value="seek +5%">seek +5%</button>
					</td>
				</tr>
			</table>

			$(# cutでクエリを加工,デコードしxargsでbusybox httpdでデコード
			echo $QUERY_STRING | cut -d"=" -f2 | xargs busybox httpd -d | 

			# デコードした文字列をprintfでncに渡す
			xargs -I{} printf "{}\nstatus\nclose\n" | nc -w 3 $MPD_HOST 6600 | 

			# "OK"にマッチしない文字列をボタン化
			awk '!/OK/{
				print "<p><button name=button value="$0">"$0"</button></p>"
			}

			# "OK"にマッチする文字列を"<p>"タグ付きで出力
			/OK/{
				print "<p>"$0"</p>"
			}' |

			# 重複行を削除
			awk '!a[$0]++{
				print $0
			}' 

			)

		<!-- リンク -->
		<button><a href="queued/queued.cgi">Queued</a></button>
		<button><a href="directory/directory.cgi">Directoty</a></button>
		<button><a href="playlist/playlist.cgi">Playlist</a></button>
		<button><a href="settings/settings.cgi">Settings</a></button>

    </body>

	<footer>
		<h4>source code</h4>
		<p><a href="https://github.com/tekkamelon/bb-mpd">git repository</a></p>
		<h4>debug info</h4>

			<p>QUERY_STRING: $(echo $QUERY_STRING | cut -d"," -f2 | xargs busybox httpd -d)</p>

	</footer>

</html>
EOS

