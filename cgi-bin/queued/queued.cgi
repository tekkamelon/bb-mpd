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
		<h1>Queued</h1>
	</header>

    <body>
		<h4>$(echo "host:$MPD_HOST<br>port:$MPD_PORT<br>")</h4>
		<!-- playlistの処理 -->
		<form name="FORM" method="GET" >
			
			<p>$(# playlistのセーブ

			# クエリを変数展開で加工
			echo ${QUERY_STRING#*\=} | 

			# "&input_string="をスペースに置換,デコードしxargsでmpcに渡す
			sed "s/\&input_string\=/ /g" | busybox httpd -d | xargs mpc -q > /dev/null
			)</p>

			<!-- クエリの表示 -->
			<p>debug:$(echo $QUERY_STRING)</p>
				<p>
					<!-- ドロップダウンリスト -->
	             	<select name="button">
						
						<!-- 検索 -->
						<option value="match">match</option>

						<!-- 保存 -->
						<option value="save">save playlist</option>
		            </select>

					<!-- playlistの名前,検索ワードの入力欄 -->
					<span>
						<input type="text" name="input_string">
					</span>
				</p>
		</form>

		<form name="music" method="POST" >
			
			<p>$(# 曲の再生部分

			# POSTで受け取った文字列を変数に代入
			cat_post=$(cat)
		
			# POSTに"http"が含まれていれば真,なければ偽
			if echo "${cat_post}" | grep -q "http" ; then

				# 真の場合,デコードし次の曲に追加,成功時のみ再生
				echo ${cat_post} | busybox httpd -d | mpc insert && mpc next | sed "s/$/<br>/g" 2>&1
			
			else

				# 偽の場合,POSTを変数展開で加工,デコードしてmpcに渡す
				echo ${cat_post} | busybox httpd -d | xargs mpc searchplay | sed "s/$/<br>/g" 2>&1 

			fi
			)</p>

			<!-- リンク -->
			<button><a href="/cgi-bin/directory/directory.cgi">Directory</a></button>
			<button><a href="/cgi-bin/index.cgi">HOME</a></button>
			<button><a href="/cgi-bin/playlist/playlist.cgi">Playlist</a></button>

			<!-- プレイリストの一覧を表示 -->
			$(# クエリ内に"match"があるかどうかを判断

			# クエリを変数展開で加工,デコードしgrepの終了ステータスで文字列があるかどうかを判断
			search_var=$(echo ${QUERY_STRING#*\=match&input_string\=} | busybox httpd -d | grep .) ||

			# 偽の場合は"."で全てにマッチングする行を表示
			search_var="."

			# キューされた曲をgrepで検索し結果を表示
			printf "playlist\nclose\n" | nc -w 3 $MPD_HOST $MPD_PORT | grep -i ${search_var} |

			# "/"と" - "を区切り文字に指定,先頭が"http"にマッチしない文字列をボタン化
			awk -F':' '!/^http/{

				# １番目のフィールドをボタン化
				print "<p><button name=button value="$1">"$0"</button>";

				# 最終フィールドをボタン化
				# "<button name=button value="$NF">"$NF"</button></p>"
			}

			# 先頭が"http"にマッチする文字列をボタン化
			/^http/{
				print "<p><button name=button value="$1">"$0"</button></p>"
			}' |

			# 重複行を削除
			awk '!a[$0]++{
				print $0
			}'
			)

		</form>
	</body>

	<footer>	
		<!-- リンク -->
		<button><a href="/cgi-bin/directory/directory.cgi">Directory</a></button>
		<button><a href="/cgi-bin/index.cgi">HOME</a></button>
		<button><a href="/cgi-bin/playlist/playlist.cgi">Playlist</a></button>
	</footer>	

</html>
