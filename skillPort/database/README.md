<h1>データベースのインポート方法</h1>
  <ol>
    <li>XAMPPを起動させる</li>
    <li>mysqlにログインする</li>
    <li><b>CREATE DATABASE skillport_db;</b> をmysqlに入力する</li>
    <li><b>USE skillport_db;</b> で使用するデータベースを選択する</li>
    <li>schema.sqlの内容を全コピー(Ctrl+A)して、mysqlに貼り付けて、Enterを押す</li>
    <li><b>SHOW TABLES;</b> でテーブルがちゃんと作成できたかを確認</li>
    <li>テーブルの情報を抽出してみる</li>
    <li>問題なければこれで終わり</li>
  </ol>

<h3>Macを使っている人はたまにデータベースが動かずにエラーが出る。対処法は以下通り</h3>
<ol>
  <li>VSCodeでviewsというフォルダー内のdb.pyを開く</li>
  <li><b>def fetch_query(sql, fetch_one=false):</b>のところを見る</li>
  <li>host="localhost"の下に<b>port="8889"</b>を追加する</li>
  <li><b>passwd="root"</b>にする</li>
  <li>それで動くはず。エラーが出たら沈まで連絡を</li>
</ol>

<p>・db.sqlは何もしない。念のためアップしたけど触らないでください。</p>
