//todo 格納する変数定義
let dataList = {};

//todo selectから条件の取得
dataList['ac'] = document.getElementById('form1').select;
dataList['bc'] = document.getElementById('form2').select;
dataList['cc'] = document.getElementById('form3').select;

//todo 選択された条件でそのあとのselectを変更
document.getElementById('dis1').textContent = dataList[dataList['c1']];

//todo 最終的な文字列の表示
sampleMail = {'a1': {'b1': {'c1': 'あああああ', 'c2': 'ああああい'}}, 'a2': {'b1': {'c1': 'あああああ', 'c2': 'ああああい'}},
'a3': {'b1': {'c1': 'あああああ', 'c2': 'ああああい'}}};
lastText = sampleMail[dataList['ac']][dataList['bc']][dataList['cc']];
document.getElementById('textBox').textContent = 'テキストボックス';



//todo コピーボタンの設置

        function copyToClipboard() {
            // コピー対象をJavaScript上で変数として定義する
            let copyTarget = document.getElementById("textBox");
            // コピー対象のテキストを選択する
            copyTarget.select();
            // 選択しているテキストをクリップボードにコピーする
            document.execCommand("Copy");
            // コピーをお知らせする
            // alert("コピーできました！ : " + copyTarget.value);
        }

document.getElementById('copyButton').onclick = function () {
    
}


//todo 保存する項目へのジャンプ
//todo 保存する項目の入力
//todo 保存項目の保存
//todo 保存項目の編集

//todo タブで表示切り替え
//todo 他サイトへのリンク表示
//todo 定型入力情報のコーナー