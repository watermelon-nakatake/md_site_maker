// 例文
const firstMail = {
    0: 'はじめまして、(相手の名前)。$$(自己紹介)$$いろんなことを一緒に楽しめる彼女を探してこのサイトに登録しました。' +
        '(相手の名前)のプロフィールを見て、素敵な人だなと思ったのでメールを送ってみました。まずはメールから仲良くなれたら嬉しいです。$$' +
        '(option1)$$では、お返事待ってますね。', 1: '(相手の名前)、(自分)と結婚してください',

    2: '(相手の名前)、(自分)のメル友になってください', 3: '(相手の名前)、(自分)のフレンドになってください'
};
const optionArray1 = {
    0: '(相手の名前)はお休みの日とかはどんなことをして過ごされてるんですか？。',
    1: '(相手の名前)は映画がお好きなんですね。(自分)も好きです。(相手の名前)は特に好きな映画とかありますか？',
    2: '(相手の名前)は食べることが好きなんですね。(自分)も食べるの好きです。(相手の名前)は特に好きな食べ物とかありますか？',
    3: '(相手の名前)は音楽がお好きなんですね。(自分)も音楽聴くの好きです。(相手の名前)はどんなジャンルの音楽をよくきかれるんですか？'
};
const selfIntroArray = {
    yyy: '(自分)は(地域)在住の(自分の名前)といいます。(年齢)歳で(職業)をしています。',
    yyn: '(自分)は(自分の名前)といいます。(年齢)歳で(地域)に住んでいます',
    yny: '(自分)は(自分の名前)といいます。(年齢)歳で仕事は(職業)をしています。',
    nyy: '', ynn: '', nyn: '', nny: '', nnn: ''
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
    for (let checkI in checkItem) {
        if (checkI) {
            checkBox += 'y'
        } else {
            checkBox += 'n'
        }
    }
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
    let baseText = firstMail[lv1];
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

//最初の処理
displayText();
