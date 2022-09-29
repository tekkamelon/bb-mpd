#!/bin/busybox ash

echo "Content-type: text/html"
echo ""

cat << EOS
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width,initial-scale=1.0">
        <title>sh-MPD</title>
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

			$(# 変数展開でクエリを加工,デコードしxargsでmpcに渡す
			echo ${QUERY_STRING#*\=} | urldecode | xargs mpc -q > /dev/null)

    </body>

	<footer>
		<h4>source code</h4>
		<p><a href="https://github.com/tekkamelon/sh-mpd">git repository</a></p>
		<h4>debug info</h4>

			<p>QUERY_STRING: $(echo "$QUERY_STRING")</p>

	</footer>

</html>
EOS

