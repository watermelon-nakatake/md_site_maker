let dataList = {};

dataList['ac'] = document.getElementById('form1').select;
dataList['bc'] = document.getElementById('form2').select;
dataList['cc'] = document.getElementById('form3').select;

document.getElementById('dis1').textContent = dataList[dataList['c1']];

sampleMail = {'a1': {'b1': {'c1': 'あああああ', 'c2': 'ああああい'}}, 'a2': {'b1': {'c1': 'あああああ', 'c2': 'ああああい'}},
'a3': {'b1': {'c1': 'あああああ', 'c2': 'ああああい'}}};
lastText = sampleMail[dataList['ac']][dataList['bc']][dataList['cc']];
document.getElementById('textBox').textContent = 'テキストボックス';

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
