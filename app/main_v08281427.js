// 例文
const firstMail = {0: 'f00', 1: 'f01', 2: 'f02', 3: 'f03'};
const firstMailText = {
    f00: 'はじめまして、(相手の名前)。$$(自己紹介)いろんなことを一緒に楽しめる彼女が欲しくて、このサイトに登録しました。$$' +
        '(相手の名前)のプロフィールを見て、素敵な人だなと思ったのでメールを送ってみました。まずはメールから仲良くなれたら嬉しいです。$$' +
        '(option1)$$では、お返事待ってますね。',
    f01: 'はじめまして、(相手の名前)。$$(自己紹介)将来のことを考えられるような女性との出会いを探しています。$$' +
        '(相手の名前)のプロフィールを見て、とても素敵な方だなと感じてご連絡差し上げました。まずはメールでいろいろお話しできたらと思います。$$' +
        '(option1)$$では、お返事待ってますね。',
    f02: 'はじめまして、(相手の名前)。$$(自己紹介)実際に会うとかは考えずに純粋にメールのやりとりを楽しめるメル友を探しています。$$' +
        '(相手の名前)のプロフィールを見て、お話しするのが楽しそうだなと思ったのでメールさせてもらいました。よかったらメル友になってください。$$' +
        '(option1)$$では、期待してお返事お待ちします。',
    f03: 'はじめまして、(相手の名前)。$$(自己紹介)彼女とかではなくて、一緒にいろいろ楽しめるような女性との出会いを探しています。$$' +
        '(相手の名前)のプロフィールを見て、とても素敵な方だなと思ったのでメッセージ送ってみました。' +
        'まずはメールでいろいろお話しして、仲良くなったら遊んだり、お酒を飲んだりしましょう。$$' +
        '(option1)$$では、お返事待ってますね。',
    f04: 'はじめまして、(相手の名前)。$$(自己紹介)彼女とかじゃなくて、お互い都合がいいときにちょっと遊んだりできるような相手を探してます。$$' +
        '(相手の名前)のプロフィールを見て、とてもいい感じの人だなと思ったのでメッセージ送ってみました。' +
        'まずはメールでいろいろお話しして、仲良くなったら遊んだり、お酒を飲んだりしましょう。$$' +
        '(option1)$$では、お返事を超期待して待ってますね！'
};

const optionArray1 = {
    0: 'ところで、(相手の名前)はお休みの日とかはどんなことをして過ごされてるんですか？。よかったら教えてください！',
    1: 'プロフィールに書いてあったんですけど、(相手の名前)は映画がお好きなんですね。(自分)も好きです。(相手の名前)は特に好きな映画とかありますか？',
    2: 'プロフ見たんですけど、(相手の名前)は食べることが好きなんですね。(自分)も食べるの好きです。(相手の名前)は特に好きな食べ物とかありますか？',
    3: 'そうそう、(相手の名前)は音楽がお好きなんですね。(自分)も音楽聴くの好きです。(相手の名前)はどんなジャンルの音楽をよくきかれるんですか？'
};
const sFTop = '(自分)は(自分の名前)といいます。';
const selfIntroArray = {
    yyy: '(自分)は(地域)在住の(自分の名前)といいます。(年齢)歳で(職業)をしています。',
    yyn: sFTop + '(年齢)歳で(地域)に住んでいます。',
    yny: sFTop + '(年齢)歳で仕事は(職業)をしています。',
    nyy: sFTop + '(地域)で(職業)をしています。',
    ynn: sFTop + '歳は(年齢)歳です。',
    nyn: sFTop + '(地域)に住んでます。',
    nny: sFTop + '仕事は(職業)をしています。',
    nnn: sFTop
};
// 見出しとselect value
// step 0; first mail  1: second  3: conversation  4: date
const labelArray = {'0': ['目的', '彼女探し', '婚活', 'メル友探し', 'セフレ探し']};
const optionLabel = {op1: ['相手が興味あるもの', '特になし', '映画', 'グルメ', '音楽', 'スポーツ']};
const replaceWordList = [['(名前)', 'name'], ['(年齢)', 'age'], ['(地域)', 'area'], ['(職業)', 'job'], ['(自分)', 'me']];

// データ格納
localStorage.clear();
let dataArray = {step: 0, lv1: 0, lv2: 0, lv3: 0, op1: 0};
let storageArray = JSON.parse(localStorage.getItem('dataArray'));
let currentArray = dataArray;
console.log(storageArray);
if (storageArray != null) {
    currentArray = storageArray
}
console.log(currentArray);


// ユーザー情報のlocal storage保存

let nameForm = document.getElementById('name');
let ageForm = document.getElementById('age');
let areaForm = document.getElementById('area');
let jobForm = document.getElementById('job');
let meForm = document.getElementById('me');

if (!localStorage.getItem('name')) {
    populateStorage();
} else {
    setStyles();
}

function populateStorage() {
    localStorage.setItem('name', document.getElementById('name').value);
    localStorage.setItem('age', document.getElementById('age').value);
    localStorage.setItem('area', document.getElementById('area').value);
    localStorage.setItem('job', document.getElementById('job').value);
    localStorage.setItem('me', document.getElementById('me').value);

    setStyles();
}

function setStyles() {
    let currentName = localStorage.getItem('name');
    let currentAge = localStorage.getItem('age');
    let currentArea = localStorage.getItem('area');
    let currentJob = localStorage.getItem('job');
    let currentMe = localStorage.getItem('me');

    document.getElementById('name').value = currentName;
    document.getElementById('age').value = currentAge;
    document.getElementById('area').value = currentArea;
    document.getElementById('job').value = currentJob;
    document.getElementById('me').value = currentMe;

}

nameForm.onchange = populateStorage;
ageForm.onchange = populateStorage;
areaForm.onchange = populateStorage;
jobForm.onchange = populateStorage;
meForm.onchange = populateStorage;

//自己紹介
function selfIntroductionMaker() {
    let currentName = localStorage.getItem('name');
    let currentAge = localStorage.getItem('age');
    let currentArea = localStorage.getItem('area');
    let currentJob = localStorage.getItem('job');
    let currentMe = localStorage.getItem('me');
    let checkItem = [currentAge, currentArea, currentJob];
    let checkBox = '';
    if (!currentName) {
        alert('お名前（ニックネーム）を記入してください。')
    }
    if (!currentMe) {
        currentMe = '私';
    }
    console.log(currentArea);
    for (let i = 0; i < checkItem.length; i += 1) {
        let checkI = checkItem[i];
        if (!checkI) {
            checkBox += 'n'
        } else {
            checkBox += 'y'
        }
    }
    console.log(checkBox);

    let result = selfIntroArray[checkBox].replace('(自分)', currentMe);
    result = result.replace('(自分の名前)', currentName);
    result = result.replace('(年齢)', currentAge);
    result = result.replace('(地域)', currentArea);
    result = result.replace('(職業)', currentJob);
    return result
}

// 例文の表示

function replaceAll(str, before, after) {
    return str.split(before).join(after);
}

function displayText() {
    console.log(dataArray);
    let dataArrayD = currentArray;
    let step = dataArrayD['step'];
    let lv1 = dataArrayD['lv1'];
    let op1 = dataArrayD['op1'];
    let baseText = firstMailText[firstMail[lv1]];
    if (baseText.indexOf('(option1)') !== -1) {
        console.log(dataArrayD['op1']);
        console.log(optionArray1[dataArrayD['op1']]);
        baseText = replaceAll(baseText, '(option1)', optionArray1[op1])
    }
    for (let i = 0; i < replaceWordList.length; i += 1) {
        let replaceWord = replaceWordList[i];
        if (baseText.indexOf(replaceWord[0]) !== -1) {
            baseText = replaceAll(baseText, replaceWord[0], localStorage.getItem(replaceWord[1]))
        }
    }
    //自己紹介挿入
    if (baseText.indexOf('(自己紹介)') !== -1) {
        baseText = baseText.replace('(自己紹介)', selfIntroductionMaker())
    }
    //相手の名前の置換
    if (baseText.indexOf('(相手の名前)') !== -1) {
        let herNameText = document.getElementById('herName').value;
        if (herNameText) {
            baseText = replaceAll(baseText, '(相手の名前)', herNameText)
        }
    }
    document.getElementById('mailDisplay').innerHTML = '<p>' + replaceAll(baseText, '$$', '<br>')
        + '</p>';
    document.getElementById('mailDisplayD').value = replaceAll(baseText, '$$', '\n')
}
// 各所クリックで例文更新
let selectFormHerName = document.getElementById("herName");
selectFormHerName.onchange = displayText;
let selectFormTab1 = document.getElementById("tab-1");
selectFormTab1.onclick = displayText;

// selectを表示
let selectFormLv1 = document.getElementById("lv1");
let selectFormOp1 = document.getElementById("op1");

function makeSelectStr(level) {
    let strArray = [];
    let lvStr = '';
    console.log(level);
    if (level.indexOf('op') >= 0) {
        strArray = optionLabel[level];
        lvStr = level;
    } else {
        strArray = labelArray[level];
        lvStr = 'lv' + String(level.length);
    }
    console.log(strArray);
    let outerId = lvStr + 'Outer';
    let optionStr = '';
    let key = strArray[0];
    strArray.shift();
    for (let i = 0; i < strArray.length; i += 1) {
        optionStr += '<option value="' + String(i) + '" selected>' + strArray[i] + '</option>\n';
    }
    console.log(optionStr);
    document.getElementById(outerId).innerHTML = '<label for="' + lvStr + '">' + key + '</label>\n<select id="' +
        lvStr + '" class="select_i">\n' + optionStr + '</select>';
}

function dataArrayOrder(level, value) {
    let arrayData = currentArray;
    if (level === 'step') {
        arrayData['step'] = Number(value);
        arrayData['lv1'] = 0;
        arrayData['lv2'] = 0;
        arrayData['lv3'] = 0;
    } else if (level === 'lv1') {
        arrayData['lv1'] = Number(value);
        arrayData['lv2'] = 0;
        arrayData['lv3'] = 0;
    } else if (level === 'op1') {
        arrayData['op1'] = Number(value);
    }
    return arrayData
}


function selectChange(level) {
    let selectedValue = document.getElementById(level).value;
    let arrayData = dataArrayOrder(level, selectedValue);
    console.log(selectedValue);
    console.log(arrayData);
    localStorage.setItem('dataArray', JSON.stringify(arrayData));
    displayText()
}

function selectChangeLv1() {
    selectChange('lv1')
}

function selectChangeOp1() {
    selectChange('op1')
}

selectFormLv1.onchange = selectChangeLv1;
selectFormOp1.onchange = selectChangeOp1;



// テキストのコピー
function execCopy(string) {

    // 空div 生成
    let tmp = document.createElement("div");
    // 選択用のタグ生成
    let pre = document.createElement('pre');

    tmp.appendChild(pre).textContent = string;

    // 要素を画面外へ
    let s = tmp.style;
    s.position = 'fixed';
    s.right = '200%';

    // body に追加
    document.body.appendChild(tmp);
    // 要素を選択
    document.getSelection().selectAllChildren(tmp);

    // クリップボードにコピー
    let result = document.execCommand("copy");

    // 要素削除
    document.body.removeChild(tmp);
    return result;
}

let textarea = document.getElementById('mailDisplayD');
let button = document.getElementById('copyButton');

button.onclick = function () {
    if (execCopy(textarea.value)) {
        alert('コピーできました!');
    } else {
        alert('このブラウザでは対応していません!');
    }
};

//リンクのクリックカウントとURL変更
let clickCountW = 0;

function clickCounter(siteName) {

}

//最初の処理
//displayText();
