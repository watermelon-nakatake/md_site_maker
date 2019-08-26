// 例文

const firstMail = {
    彼女探し: {
        特になし:'彼女になって',
        趣味: '趣味が合うので彼女になってください',
        食べ物: '好きなものが一緒だから彼女になって',
        映画: '好きな映画が一緒だから彼女になって'
    },
    婚活: {
        特になし:'結婚してください',
        趣味: '趣味が合うので奥さんになってください',
        食べ物: '好きなものが一緒だから奥さんになって',
        映画: '好きな映画が一緒だから奥さんになって'},
    セフレ: {
        特になし:'セフレになってください',
        趣味: '趣味が合うのでセフレになってください',
        食べ物: '好きなものが一緒だからセフレになって',
        映画: '好きな映画が一緒だからセフレになって'}
};
const fMLabel = {1:'目的', 2:'相手が興味あること'};
/*
const secondMail = [['こんにちは']];
const conversationMail = [['そういえば']];
const datemail = [['会いませんか']];
*/

// ユーザー情報のlocal storage保存

let nameForm = document.getElementById('name');
let ageForm = document.getElementById('age');
let areaForm = document.getElementById('area');
let jobForm = document.getElementById('job');

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

    setStyles();
}

function setStyles() {
    let currentName = localStorage.getItem('name');
    let currentAge = localStorage.getItem('age');
    let currentArea = localStorage.getItem('area');
    let currentJob = localStorage.getItem('job');

    document.getElementById('name').value = currentName;
    document.getElementById('age').value = currentAge;
    document.getElementById('area').value = currentArea;
    document.getElementById('job').value = currentJob;

}

nameForm.onchange = populateStorage;
ageForm.onchange = populateStorage;
areaForm.onchange = populateStorage;
jobForm.onchange = populateStorage;


// 選択項目の表示
let selectList = {0: '', 1: '', 2: 1, 3: 1, 4: 1, 5: 1};
let stepForm1 = document.getElementById("lv1");
let stepForm2 = document.getElementById("lv2");
let stepForm3 = document.getElementById("lv3");
console.log(stepForm1);


function makeSelectStr(level, array, key) {
    let levelStr = 'lv' + String(level);
    let outerId = 'lv' + String(level) + 'Outer';
    let strBox = '';
    for (let selectValue in array) {
        console.log(selectValue);
        strBox = strBox + '<option value="' + selectValue + '" selected>' + selectValue + '</option>\n';
    }
    document.getElementById(outerId).innerHTML = '<label for="' + levelStr + '">' + key + '</label>\n<select id="' +
        levelStr + '" class="select_i">\n' + strBox + '</select>';
}

function selectChoice(level) {
    let thisLevelStr = 'lv' + String(level);
    let nextLevel = level + 1;
    let selectedValue = document.getElementById(thisLevelStr).value;
    localStorage.setItem('lv1Value', selectedValue);
    let key = fMLabel[level + 1];
    let array = firstMail[key];
    makeSelectStr(nextLevel, array, key)
}

function selectChoice1() {
    selectChoice(1)
}

function selectChoice2() {
    selectChoice(2)
}

function selectChoice3() {
    selectChoice(3)
}

// ストレージのselectを表示



stepForm1.onchange = selectChoice1;
stepForm2.onchange = selectChoice2;
stepForm3.onchange = selectChoice3;


//todo: functionの引数に配列の該当する中身と階層を渡す
//todo: 中身をhtmlに入れて表示　forでselectを作る


// const textLabel = [['choice'], [], []]
// let chosenStep = document.getElementById('tier1');
// document.getElementById('t2s1').textContent = textLabel[0][0];

/*
// 選ばれた例文の表示
const replaceWordList = [['name', 'name', 'replaceWord'], ['age', 'age', 'replaceAge']];
const stepForm = document.getElementById("step");
const purposeForm = document.getElementById("purpose");
const sampleNoForm = document.getElementById("sampleNo");
const mailSample = {
    fm: {
        gf: ['gf mail sample 1 replaceWord replaceAge', 'gf mail sample 2 replaceWord replaceAge',
            'gf mail sample 3 replaceWord replaceAge'],
        mr: [
            ['marriage mail sample 1 replaceWord replaceAge', ['herName', 'herName'], ['hobby', 'hobby']],
            ['marriage mail sample 2 replaceWord replaceAge'],
            ['marriage mail sample 3 replaceWord replaceAge']
        ]
    },
    sm: {
        gf: ['gf second mail sample 1 replaceWord replaceAge', 'gf second mail sample 2 replaceWord replaceAge',
            'gf second mail sample 3 replaceWord replaceAge'],
        mr: ['marriage second mail sample 1 replaceWord replaceAge',
            'marriage second mail sample 2 replaceWord replaceAge',
            'marriage second mail sample 3 replaceWord replaceAge']
    }
};

function replaceWordFunc(word1, word2, word3, text) {
    let currentItem = localStorage.getItem(word1);
    console.log(currentItem);
    if (currentItem !== word2) {
        text = text.replace(word3, currentItem);
    }
    return text
}

function changeMailText() {
    let step = document.getElementById("step").value;
    let purpose = document.getElementById("purpose").value;
    let sampleNo = document.getElementById("sampleNo").value;
    let currentText = mailSample[step][purpose][Number(sampleNo)];

    console.log(step);
    console.log(purpose);
    console.log(sampleNo);
    console.log(Number(sampleNo));
    console.log(mailSample[step][purpose][Number(sampleNo)]);

    for (let i = 0; i < replaceWordList.length; i++) {
        console.log(i);
        currentText = replaceWordFunc(replaceWordList[i][0], replaceWordList[i][1],
            replaceWordList[i][2], currentText)
    }
    document.getElementById("mailDisplay").value = currentText;
}

stepForm.onchange = changeMailText;
purposeForm.onchange = changeMailText;
sampleNoForm.onchange = changeMailText;


 */


// 例文に個別情報挿入


// テキストのコピー

function execCopy(string) {

    // 空div 生成
    let tmp = document.createElement("div");
    // 選択用のタグ生成
    let pre = document.createElement('pre');

    // 親要素のCSSで user-select: none だとコピーできないので書き換える
    pre.style.webkitUserSelect = 'auto';
    pre.style.userSelect = 'auto';

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

let textarea = document.getElementById('mailDisplay');
let button = document.getElementById('copyButton');
console.log(textarea)
button.onclick = function () {
    if (execCopy(textarea.value)) {
        alert('コピーできました');
    } else {
        alert('このブラウザでは対応していません');
    }
};

// installボタンの表示
let installPromptEvent;

window.addEventListener('beforeinstallprompt', (event) => {
    // Chrome67以前で自動的にプロンプトを表示しないようにする?
    event.preventDefault();

    // イベントを変数に保存する
    installPromptEvent = event;

    // #btnを活性に
    document.querySelector('#installBtn').disabled = false;
});

// #btnをクリックした時にプロンプトを表示させる
document.querySelector('#installBtn').addEventListener('click', () => {
    // #btnを非活性に
    document.querySelector('#installBtn').disabled = true;

    // 　ホーム画面に追加のダイアログを表示させる
    installPromptEvent.prompt();

    // ダイアログの結果をプロミスで受け取る
    installPromptEvent.userChoice.then((choice) => {
        if (choice.outcome === 'accepted') {
            console.log('User accepted the A2HS prompt');
        } else {
            console.log('User dismissed the A2HS prompt');
        }
        // Update the install UI to notify the user app can be installed
        installPromptEvent = null;
    });
});
