// 例文
const firstMail = {0: 'f00', 1: 'f01', 2: 'f02', 3: 'f03'};
const firstMailText = {
    f00: 'はじめまして、(herName)。$$(自己紹介)いろんなことを一緒に楽しめる彼女が欲しくて、このサイトに登録しました。$$' +
        '(herName)のプロフィールを見て、素敵な人だなと思ったのでメールを送ってみました。まずはメールからゆっくり仲良くなれたら嬉しいです。$$' +
        '(option1)$$では、お返事待ってますね。',
    f01: 'はじめまして、(herName)。$$(自己紹介)将来のことを考えられるような女性との出会いを探しています。$$' +
        '(herName)のプロフィールを見て、とても素敵な方だなと感じてご連絡差し上げました。まずはメールでいろいろお話しできたらと思います。$$' +
        '(option1)$$では、お返事待ってますね。',
    f02: 'はじめまして、(herName)。$$(自己紹介)実際に会うとかは考えずに純粋にメールのやりとりを楽しめるメル友を探しています。$$' +
        '(herName)のプロフィールを見て、お話しするのが楽しそうだなと思ったのでメールさせてもらいました。よかったらメル友になってください。$$' +
        '(option1)$$では、期待してお返事お待ちします。',
    f03: 'はじめまして、(herName)。$$(自己紹介)彼女とかではなくて、一緒にいろいろ楽しめるような女性との出会いを探しています。$$' +
        '(herName)のプロフィールを見て、とても素敵な方だなと思ったのでメッセージ送ってみました。' +
        'まずはメールでいろいろお話しして、仲良くなったら遊んだり、お酒を飲んだりしましょう。$$' +
        '(option1)$$では、お返事待ってますね。',
    f04: 'はじめまして、(herName)。$$(自己紹介)彼女とかじゃなくて、お互い都合がいいときにちょっと遊んだりできるような相手を探してます。$$' +
        '(herName)のプロフィールを見て、とてもいい感じの人だなと思ったのでメッセージ送ってみました。' +
        'まずはメールでいろいろお話しして、仲良くなったら遊んだり、お酒を飲んだりしましょう。$$' +
        '(option1)$$では、お返事を超期待して待ってますね！'
};
const secondMail = {0: 's00', 1: 's01', 2: 's02'};
const secondMailText = {
    s00: '(herName)、(option2)。$$メールありがとうございます。(herName)とはぜひ仲良くなりたいと思っていたので、とても嬉しいです。' +
        'これからよろしくお願いしますね。仲良くしてくださいね。$$(option3)',
    s01: '(herName)、(option2)。$$返信ありがとうございます。(herName)とはぜひお話ししてみたいと思っていたので、とても嬉しいです。' +
        'これからよろしくお願いしますね。$$(以下、相手からの質問への回答とその質問に関係するこちらからの新しい質問)',
    s02: '(herName)、(option2)。$$返信ありがとうございます。(herName)からお返事をもらえてすごく嬉しいです。' +
        'これからよろしくお願いしますね。$$(option1)'
};

const optionArray1 = {
    0: 'ところで、(herName)はお休みの日とかはどんなことをして過ごされてるんですか？。よかったら教えてください！',
    1: 'プロフィールに書いてあったんですけど、(herName)は映画がお好きなんですね。(自分)も好きです。(herName)は特に好きな映画とかありますか？',
    2: 'プロフ見たんですけど、(herName)は食べることが好きなんですね。(自分)も食べるの好きです。(herName)は特に好きな食べ物とかありますか？',
    3: 'そうそう、(herName)は音楽がお好きなんですね。(自分)も音楽聴くの好きです。(herName)はどんなジャンルの音楽をよくきかれるんですか？',
    4: '(herName)、スポーツがお好きなんですね。(自分)も体動かすのも見るのも好きです。(herName)が特に好きなスポーツって何ですか？',
    5: '(herName)のプロフィールを見たら、ドライブが好きって書いてあったんですけど、どの辺りによくドライブに行かれるんですか？'
};
const optionArray2 = {
    0: 'おはようございます！',
    1: 'こんにちは！',
    2: 'こんばんは！'
};
const optionArray3 = {
    0: '(herName)はお休みの日は(herAnswer)されてるんですね。(自分)も(herAnswer)することよくあります。$$' +
        'どんな(herAnswer)が特にお気に入りですか？',
    1: '(herName)、(herAnswer)がお気に入りなんですね。(自分)も観ましたけど、(herAnswer)いいですよね〜。$$' +
        '映画は劇場でご覧になることが多いですか？それとも自宅で？',
    2: '(herAnswer)がお好きなんですね。確かに美味しいですもんね。(herName)の気持ちよく分かります。',
    3: 'そうそう、(herName)は音楽がお好きなんですね。(自分)も音楽聴くの好きです。(herName)はどんなジャンルの音楽をよくきかれるんですか？',
    4: '(herName)、スポーツがお好きなんですね。(自分)も体動かすのも見るのも好きです。(herName)が特に好きなスポーツって何ですか？',
    5: '(herName)さんのプロフィールを見たら、ドライブが好きって書いてあったんですけど、どの辺りによくドライブに行かれるんですか？'
};
const optionList = ['option1', 'option2', 'option3'];
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
const labelArray = {
    '0': ['目的', '彼女探し', '婚活', 'メル友探し', 'セフレ探し'],
    '1': ['状況', '質問の回答した', '答えずに質問してきた', 'そっけない一言メール']
};
const optionLabel = {
    op1: ['相手が興味あるもの', '特になし', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ'],
    op2: ['メール送信の時間帯', '朝', '昼', '夜'],
    op3: ['会話の話題', '休みにすること', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ']
};
const replaceWordList = [['(名前)', 'name'], ['(年齢)', 'age'], ['(地域)', 'area'], ['(職業)', 'job'], ['(自分)', 'me']];
const optionWordList = [['option1', 'op1'], ['option2', 'op2'], ['option3', 'op3']];
const insertList = ['herName', 'herAnswer'];
// データ格納
//localStorage.clear();
let dataArray = {step: 0, lv1: 0, lv2: 0, lv3: 0, op1: 0, op2: 0, op3: 0};
let storageArray = JSON.parse(localStorage.getItem('dataArray'));
let currentArray = dataArray;
if (storageArray != null) {
    currentArray = storageArray
}

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
        currentName = '◯◯'
    }
    if (!currentMe) {
        currentMe = '私'
    }
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
    let dataArrayD = JSON.parse(localStorage.getItem('dataArray'));
    let step = dataArrayD['step'];
    let lv1 = dataArrayD['lv1'];
    let op1 = dataArrayD['op1'];
    let op2 = dataArrayD['op2'];
    let op3 = dataArrayD['op3'];
    let baseText = '';
    switch (step) {
        case 0:
            baseText = firstMailText[firstMail[lv1]];
            break;
        case 1:
            baseText = secondMailText[secondMail[lv1]];
            break;
        default:
            baseText = firstMailText[firstMail[lv1]]
    }
    let beforeReplace = baseText;
    console.log(baseText);
    if (baseText.indexOf('(option1)') !== -1) {
        console.log('option1のreplace');
        baseText = replaceAll(baseText, '(option1)', optionArray1[op1]);
        console.log(baseText)
    }
    if (baseText.indexOf('(option2)') !== -1) {
        baseText = replaceAll(baseText, '(option2)', optionArray2[op2])
    }
    if (baseText.indexOf('(option3)') !== -1) {
        baseText = replaceAll(baseText, '(option3)', optionArray3[op3])
    }
    for (let i = 0; i < replaceWordList.length; i += 1) {
        let replaceWord = replaceWordList[i];
        if (baseText.indexOf(replaceWord[0]) !== -1) {
            baseText = replaceAll(baseText, replaceWord[0], localStorage.getItem(replaceWord[1]))
        }
    }
    let hAForm = document.getElementById('herAnswerOuter');
    console.log(baseText);
    console.log(baseText.indexOf('herAnswer') !== -1);
    if (baseText.indexOf('herAnswer') !== -1) {
        hAForm.style.display = 'block';
        document.getElementById('herAnswer').value = '';
    } else {
        hAForm.style.display = 'none'
    }
    //自己紹介挿入
    if (baseText.indexOf('(自己紹介)') !== -1) {
        baseText = baseText.replace('(自己紹介)', selfIntroductionMaker())
    }
    for (let i = 0; i < insertList.length; i++) {
        let insertStr = insertList[i];
        let searchStr = '(' + insertStr + ')';
        //相手の名前の置換
        if (baseText.indexOf(searchStr) !== -1) {
            let herNameText = document.getElementById(insertStr).value;
            if (herNameText) {
                baseText = replaceAll(baseText, searchStr, herNameText)
            }
        }
    }

    document.getElementById('mailDisplay').innerHTML = '<p>' + replaceAll(baseText, '$$', '<br>')
        + '</p>';
    document.getElementById('mailDisplayD').value = replaceAll(baseText, '$$', '\n');


    return beforeReplace
}

// 各所クリックで例文更新
let selectFormHerName = document.getElementById("herName");
selectFormHerName.onchange = displayText;
let selectFormHerAnswer = document.getElementById("herAnswer");
selectFormHerAnswer.onchange = displayText;
let selectFormTab1 = document.getElementById("tab-1");
selectFormTab1.onclick = displayText;

// selectを表示
let selectFormStep = document.getElementById("step");
let selectFormLv1 = document.getElementById("lv1");
//let selectFormLv2 = document.getElementById("lv2");
let selectFormOp1 = document.getElementById("op1");
let selectFormOp2 = document.getElementById("op2");
let selectFormOp3 = document.getElementById("op3");

function makeSelectOrder(levelStr) {
    let selectOrder = '';
    let currentArray = JSON.parse(localStorage.getItem('dataArray'));
    if (!currentArray) {
        currentArray = dataArray;
    }
    console.log(currentArray);
    switch (levelStr) {
        case 'lv1':
            selectOrder = String(currentArray['step']);
            break;
        case 'lv2':
            selectOrder = String(currentArray['step']) + String(currentArray['lv1']);
            break;
        default:
            selectOrder = '0'
    }
    console.log(selectOrder);
    return selectOrder
}


function makeOptionStr(optionNum) {
    console.log(optionNum);
    let strArray = optionLabel[optionNum];

    let optionStr = '<option value="" disabled>select</option>';
    let key = strArray[0];
    let labelId = optionNum + 'Label';
    let optionId = optionNum + 'Outer';
    for (let i = 1; i < strArray.length; i += 1) {
        optionStr += '<option value="' + String(i - 1) + '" selected>' + strArray[i] + '</option>\n';
    }
    document.getElementById(optionNum).innerHTML = optionStr;
    document.getElementById(labelId).textContent = key;
    let opForm = document.getElementById(optionNum);
    opForm.style.display = 'block';
    opForm.options[0].selected = true
}
//todo: 共通部分をfunctionに

function makeSelectStr(levelStr) {
    console.log(levelStr);
    let selectOrder = makeSelectOrder(levelStr);
    let strArray = labelArray[selectOrder];
    let optionStr = '<option value="" disabled>select</option>';
    let key = strArray[0];
    let labelId = levelStr + 'Label';
    for (let i = 1; i < strArray.length; i += 1) {
        optionStr += '<option value="' + String(i - 1) + '" selected>' + strArray[i] + '</option>\n';
    }
    document.getElementById(levelStr).innerHTML = optionStr;
    document.getElementById(labelId).textContent = key;
    document.getElementById(levelStr).options[0].selected = true
}


function dataArrayOrder(level, valueO) {
    let arrayData = currentArray;
    console.log(valueO);
    if (level === 'step') {
        arrayData['step'] = Number(valueO);
        arrayData['lv1'] = 0;
    } else if (level === 'lv1') {
        arrayData['lv1'] = Number(valueO);
    }
    return arrayData
}

function selectChange(level) {
    let selectedValue = document.getElementById(level).value;
    let arrayData = dataArrayOrder(level, selectedValue);
    console.log(selectedValue);
    console.log(arrayData);
    localStorage.setItem('dataArray', JSON.stringify(arrayData));
    let currentText = displayText();
    console.log(currentText);
    optionSelectDisplay(currentText)
}

function optionSelectDisplay(currentText) {
    for (let i = 0; i < optionList.length; i++) {
        console.log(optionList[i]);
        console.log(currentText.indexOf(optionList[i]) !== -1);
        if (currentText.indexOf(optionList[i]) !== -1) {
            makeOptionStr(optionWordList[i][1])
        } else {
            let opForm = document.getElementById(optionWordList[i][1] + 'Outer');
            opForm.style.display = 'none'
        }
    }
}

function optionClicked(optionId) {
    let optionNum = Number(document.getElementById(optionId).value);
    console.log(optionNum);
    let dataArray = JSON.parse(localStorage.getItem('dataArray'));
    console.log(dataArray);
    dataArray[optionId] = optionNum;
    console.log(dataArray);
    localStorage.setItem('dataArray', JSON.stringify(dataArray));
    console.log(JSON.parse(localStorage.getItem('dataArray')));
    displayText();
}

function selectChangeStep() {
    console.log('selectChangeStep start');
    selectChange('step');
    makeSelectStr('lv1')
}

function selectChangeLv1() {
    console.log('selectChangeLv1 start');
    selectChange('lv1');
}

function selectChangeOp2() {
    console.log('selectChangeOp2 start');
    optionClicked('op2')
}

function selectChangeOp1() {
    console.log('selectChangeOp1 start');
    optionClicked('op1')
}

function selectChangeOp3() {
    console.log('selectChangeOp3 start');
    optionClicked('op3')
}

selectFormStep.onchange = selectChangeStep;
selectFormLv1.onchange = selectChangeLv1;
selectFormOp1.onchange = selectChangeOp1;
selectFormOp2.onchange = selectChangeOp2;
selectFormOp3.onchange = selectChangeOp3;


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
        alert('コピーできました!')
    } else {
        alert('このブラウザでは対応していません!')
    }
};


//リンクのクリックカウントとURL変更
//初期化
let formDSWk = document.getElementById('countWk');
let formDSHm = document.getElementById('countHm');
let formDSMj = document.getElementById('countMj');
let formDSPc = document.getElementById('countPc');

let countW = Number(localStorage.getItem('countWk'));
if (countW === null) {
    localStorage.setItem('countWk', '0');
}

function initializeSiteCounter() {
    const siteIdList = ['countWk', 'countHm', 'countMj', 'countPc'];
    for (let i = 0; i < siteIdList.length; i += 1) {
        let siteID = siteIdList[i];
        let countNum = Number(localStorage.getItem(siteID));
        if (countNum === null) {
            localStorage.setItem(siteID, '0')
        }
    }
}

function clickCounter(siteId) {
    let counter = Number(localStorage.getItem(siteId));
    counter++;
    console.log(siteId + 'クリック数: ' + String(counter));
    localStorage.setItem(siteId, String(counter));
    redirectChoice(counter, siteId)
}

function redirectChoice(count, siteId) {
    if (count > 10) {
        let currentDir = document.getElementById(siteId).href;
        if (currentDir.slice(-1) !== 'p') {
            let altDir = currentDir + 'p';
            console.log('リダイレクト先: ' + altDir);
            document.getElementById(siteId).href = altDir
        }
    }
}

function clickAHWk() {
    clickCounter('countWk')
}

function clickAHHm() {
    clickCounter('countHm')
}

function clickAHMj() {
    clickCounter('countMj')
}

function clickAHPc() {
    clickCounter('countPc')
}

formDSWk.onclick = clickAHWk;
formDSHm.onclick = clickAHHm;
formDSMj.onclick = clickAHMj;
formDSPc.onclick = clickAHPc;

//最初の処理
function firstInitialize() {
    console.log('re-start');
    let currentData = JSON.parse(localStorage.getItem('dataArray'));
    console.log(currentData);
    initializeSiteCounter();
    document.getElementById('step').options[Number(currentData['step']) + 1].selected = true;
    makeSelectStr('lv1');
    document.getElementById('lv1').options[Number(currentData['lv1'])].selected = true;
    let beforeText = displayText();
    optionSelectDisplay(beforeText);
    document.getElementById('op1').options[Number(currentData['op1'])].selected = true;
    document.getElementById('op2').options[Number(currentData['op2'])].selected = true;
    document.getElementById('op3').options[Number(currentData['op3'])].selected = true;
}

firstInitialize();