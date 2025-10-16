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
