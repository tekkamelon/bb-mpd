#!/bin/busybox ash

# 環境変数で接続先ホスト,ポート番号を設定,データがない場合は"localhost","6600"
export MPD_HOST=$(cat ../bb-sh.conf | sed -n "1p" | grep . || echo "localhost")
export MPD_PORT=$(cat ../bb-sh.conf | sed -n "2p" | grep . || echo "6600")

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

			# クエリに"save"があるかを確認,あれば真,なければ偽
			if echo $QUERY_STRING | grep -q "save" ; then

				# 真の場合はデコードしawkに渡す
				echo $QUERY_STRING | xargs httpd -d | 

				# "=","&"を区切り文字に指定,2,4フィールド目でスペースを挟み,closeを付けて出力
				awk -F'[=&]' '{print $2" "$4"\n""close"}' | 

				# ncに渡す
				nc $MPD_HOST $MPD_PORT

			else 

				# 偽の場合は何もしない
				:
			fi
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

				# POSTを変数展開で加工,先頭の数字のみに
				echo ${cat_post#*=} | 

				# awkで数値にマッチするか判定,"play",スペース,改行,"close"を付与
				awk '/[0-9]/{print "play"" "$0"\n""close"}' |

				# ncに渡す
				nc $MPD_HOST $MPD_PORT |

				# エラー出力ごと表示
				sed "s/$/<br>/g" 2>&1
			)</p>

			<!-- リンク -->
			<button><a href="/cgi-bin/directory/directory.cgi">Directory</a></button>
			<button><a href="/cgi-bin/index.cgi">HOME</a></button>
			<button><a href="/cgi-bin/playlist/playlist.cgi">Playlist</a></button>

			<!-- プレイリストの一覧を表示 -->
			$(# クエリ内に"match&input_string=#任意の1文字以上"があれば真,なければ偽
			echo $QUERY_STRING | grep -q "match&input_string=." 

				search_var=$(# 真の場合はクエリを変数展開で加工

					echo ${QUERY_STRING#*\=match\&input_string\=} |

					# デコード,偽の場合は"."を出力
					xargs busybox httpd -d || echo "."
					)

			# キューされた曲をgrepで検索し結果を表示
			printf "playlist\nclose\n" | nc $MPD_HOST $MPD_PORT | grep -i $search_var |

			# ":"を区切り文字に指定,先頭が"OK"にマッチしない文字列をボタン化
			awk -F':' '!/^OK/{

				# valueに1フィールド目,行全体を表示
				print "<p><button name=button value="$1">"$0"</button>"

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
