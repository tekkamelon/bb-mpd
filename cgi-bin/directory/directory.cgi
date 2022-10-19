#!/bin/busybox ash

# 環境変数で接続先ホスト,ポート番号を設定,データがない場合は"localhost","6600"
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
		<h1>Directory</h1>
	</header>

    <body>
		<h4>$(echo "host:$MPD_HOST<br>port:$MPD_PORT<br>")</h4>
		<form name="FORM" method="GET" >

			debug_info:$(echo ${QUERY_STRING} | xargs busybox httpd -d)
				
					<!-- 検索ワードの入力欄 -->
						<p>search_word:<input type="text" name="search_word"></p>
				
		</form>
	
		<!-- mpd.confで設定されたディレクトリ配下を表示 --> 
		<form name="music" method="POST" >

				<p>$(# POSTで受け取った文字列を変数に代入
				cat_post=$(cat)

				# POSTを変数展開で加工,空でない場合に真,空の場合に偽
				if [ -n "${cat_post#*\=}" ] ; then

					# 真の場合,POSTを変数展開で加工,デコードしxargsでmpcに渡しキューに追加
					echo ${cat_post#*\=} | xargs busybox httpd  -d | mpc insert && 
	
					# "mpc insert"で挿入した曲を再生
					mpc next | sed "s/$/<br>/g" 2>&1

				else

					# 偽の場合は何もせず終了
					:

				fi
				)</p>

				<!-- リンク -->
				<button><a href="/cgi-bin/queued/queued.cgi">Queued</a></button>
				<button><a href="/cgi-bin/index.cgi">HOME</a></button>
				<button><a href="/cgi-bin/playlist/playlist.cgi">Playlist</a></button>

				<!-- mpc管理下のディレクトリを再帰的に表示,awkで出力をボタン化 -->
				$(# クエリを変数展開で加工,空でない場合に真,空の場合に偽
				if [ -n "${QUERY_STRING#*\=}" ] ; then 

					# 真の場合はクエリを変数展開で加工,デコード
					search_var=$(echo ${QUERY_STRING#*\=} | urldecode)
					
				else

					# 偽の場合は"."で全てにマッチングする行を表示
					search_var="." 

				fi
				printf "listall\nclose\n" | nc -w 3 $MPD_HOST $MPD_PORT | grep -i ${search_var} |
				awk '{print "<p><button name=button value="$0">"$0"</button></p>"}'
				)

		</form>
	</body>

	<footer>
		<!-- リンク -->
		<button><a href="/cgi-bin/queued/queued.cgi">Queued</a></button>
		<button><a href="/cgi-bin/index.cgi">HOME</a></button>
		<button><a href="/cgi-bin/playlist/playlist.cgi">Playlist</a></button>
	</footer>

</html>
EOS
