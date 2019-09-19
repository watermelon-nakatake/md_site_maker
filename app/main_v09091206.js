// 例文
const firstMail = {0: 'f00', 1: 'f01', 2: 'f02', 3: 'f03'};
const secondMail = {0: 's00', 1: 's01', 2: 's02'};
const post = {0: 'p00', 1: 'p01', 2: 'p02', 3: 'p03', 4: 'p04'};
const address = {0: 'a00', 1: 'a01'};
const dateMail = {0: 'd00', 1:'d01', 2:'d02'};
const mailList = [firstMail, secondMail, post, address, dateMail];
const mailTextList = {
    f00: 'はじめまして、(herName)。$$(自己紹介)いろんなことを一緒に楽しめる彼女が欲しくて、このサイトに登録しました。$$' +
        '(herName)のプロフィールを見て、素敵な人だなと思ったのでメールを送ってみました。まずはメールからゆっくり仲良くなれたら嬉しいです。$$' +
        '(option1)$$では、お返事待ってますね。[敬語を使って書くことで、誠実な人だという印象を与えます。',
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
        '(option1)$$では、お返事を超期待して待ってますね！',
    s00: '(herName)、(option2)。$$メールありがとうございます。(herName)とはぜひ仲良くなりたいと思っていたので、とても嬉しいです。' +
        'これからよろしくお願いしますね。仲良くしてくださいね。$$(option3)',
    s01: '(herName)、(option2)。$$返信ありがとうございます。(herName)とはぜひお話ししてみたいと思っていたので、とても嬉しいです。' +
        'これからよろしくお願いしますね。$$(以下、相手からの質問への回答とその質問に関係するこちらからの新しい質問)',
    s02: '(herName)、(option2)。$$返信ありがとうございます。(herName)からお返事をもらえてすごく嬉しいです。' +
        'これからよろしくお願いしますね。$$(option1)',
    p00: '書き込みを見てくださってありがとうございます。$$' +
        '仲の良い友達からは「お前に彼女がいないのはおかしい」とか言われるけど、心から大事にできる人とお付き合いしたいと思っているので' +
        'なかなかいい出会いがありません。$$' +
        'ということで、真面目にお付き合いできる女性を探してます。メールからゆっくり仲良くなれたら嬉しいです。$$' +
        '少し自己紹介しますね。(自己紹介)' +
        '普段仕事が忙しいので、休みの日とかは体を動かしたり美味しいものを食べたりしてストレス解消しています。$$' +
        'では、気になる方はお気軽にメールくださいね。$$' +
        'いい方と出会えたらこの書き込みは消しますのでお急ぎください（笑）',
    p01: '書き込みを見てくださってありがとうございます。$$(自己紹介)' +
        '年齢的に最近結婚のことも考えるようになってきたので、将来のことも考えられるような素敵な女性との出会いを探しています。$$かなり真剣です。$$' +
        '優しくて一緒にいろいろなことにチャレンジできるような女性が好きなので、そういう方と知り合えたら嬉しいです。' +
        'まずはメールからゆっくりお話しして、仲良くなりましょう。$$' +
        '本気でお付き合いできる方と知り合えたら、この書き込みは消しますね。$$メールお待ちしています。',
    p02: '書き込みを見てくださってありがとうございます。$$' +
        '純粋にメールだけでやり取りして会話を楽しめる女性のメール友達が欲しくて書き込みをしました。$$' +
        '(趣味)が好きなので、(趣味)についていろいろ語り合えるようなメル友さんができるととても嬉しいです。もちろん(趣味)に興味ない方でもOKです。$$' +
        '「会おう」とかは絶対に言わないので、安心してメールしてきてくださいね。',
    p03: '書き込み見てくださってありがとうございます。$$' +
        '彼女を探しているというわけではないんですが、一緒に遊んだり美味しいものを食べたり、その他のことも楽しめる素敵な女性を探してます。$$' +
        '(自分)は女性に喜んでもらうのが好きなので、いい意味でかなり尽くしますよ！$$' +
        '年齢は気にしないけど、あまりぽっちゃりし過ぎてなくて優しい女性が好きですね。$$' +
        '気になった方は、お気軽にメールをお送りください。期待して待ってます！',
    p04: '最近仕事をがんばり過ぎて、ちょっと疲れがたまってます。こんな時は美味しいお酒と食事で疲れを吹き飛ばしたい･･･。$$' +
        '美味しい料理とお酒が大好きな女の子、いらっしゃったらメールで教えてください！$$' +
        '(自分)と飲みに行きましょう！$$行きたいお店があればそこでもいいですし、特になければ(自分)のおすすめのお店でご馳走します。$$' +
        'お時間はそちらの都合に合わせますよ。$$楽しい飲み会にしたいですね。',
    a00: '(herName)とお話しするのすごく楽しいです。もっとたくさんお話ししたいので、よかったら連絡先を交換して直接やりとりしませんか？$$' +
        'ラインIDでも携帯とかのメールアドレスでもどっちでもいいですよ。でも、嫌な時はもう少しサイト内でメールするから言ってくださいね。',
    a01: '(herName)さんとメールするの、すごく楽しいです。(herName)さんとは気が合いそうです。$$' +
        'もしよかったら、ラインIDとかメアド交換して、直接やり取りしませんか？その方がサイト経由でメールするよりスムーズにやり取りできますし。$$' +
        'もちろん、知り合ったばかりでまだ早いと(heraName)さんが思うなら、まだ全然大丈夫ですよ！',
    d00: '(herName)、もしよかったら来週の土曜日くらいに一緒に映画観に行きませんか？(herName)が観たいって言ってた(oi相手が観たいと言っていた映画))観に行きましょう！',
    d01: '(herName)、もしよかったら来週の土曜日くらいに一緒に？(herName)が観たいって言ってた映画観に行きましょう！'
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
    2: '(herAnswer)がお好きなんですね。確かに美味しいですもんね。(herName)の気持ちよく分かります。' +
        '$$(herName)はお気に入りの美味しい(herAnswer)のお店とかありますか？',
    3: '(herName)、(herAnswer)がお好きなんですね。(自分)も少し聴くけどいいですよね。$$ライブとかにも行ったりされるんですか？',
    4: '(herName)、(herAnswer)が好きなんですか。一緒ですね！(自分)も(herAnswer)好きです。$$' +
        '観るだけじゃなくて、自分でも(herAnswer)されるんですか？',
    5: '(herName)は(herAnswer)によくドライブに行かれるんですね。(自分)もたまに行きます。気持ちいいですよね。$$' +
        'ドライブはご自分で運転していくんですか？それともお友達とかとです？'
};
const optionArray4 = {
    0: '',
    1: '(自分)が映画が好きなので、話のタネにあなたの好きな映画もよかったら教えてくださいね。$$',
    2: '(自分)が食べることが好きなので、話のタネにあなたの好きな食べ物もよかったら教えてくださいね。$$',
    3: '(自分)が音楽を聴くの好きなので、話のタネにあなたの好きなミュージシャンもよかったら教えてくださいね。$$',
    4: '(自分)がスポーツが好きなので、話のタネにあなたの好きなスポーツもよかったら教えてくださいね。$$',
    5: '(自分)がドライブが好きなので、話のタネにあなたの好きなドライブスポットもよかったら教えてくださいね。$$'
};
const optionArray = [optionArray1, optionArray2, optionArray3, optionArray4];
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
    '0': ['出会いの目的', '彼女探し', '婚活', 'メル友探し', 'セフレ探し', '早く会える女性探し'],
    '1': ['相手からのメールの内容', '質問に答えてくれた', '質問に答えずに別の質問してきた', 'そっけない一言メール'],
    '2': ['出会いの目的', '彼女探し', '婚活', 'メル友探し', 'セフレ探し', '早く会える女性探し'],
    '3': ['連絡先交換する口実', 'もっと話しがしたいから', 'ラインの方が便利だから'],
    '4': ['会おうと誘う口実', '食事に誘う', '飲みに誘う', '遊びに誘う']
};
const optionLabel = {
    op1: ['相手が興味あるもの', '特になし', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ'],
    op2: ['メール送信の時間帯', '朝', '昼', '夜'],
    op3: ['会話の話題', '休みにすること', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ'],
    op4: ['女性への質問', '質問しない', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ']
};
const replaceWordList = [['(名前)', 'name'], ['(年齢)', 'age'], ['(地域)', 'area'], ['(職業)', 'job'], ['(自分)', 'me'],
['(趣味)', 'hobby']];
const optionWordList = [['option1', 'op1'], ['option2', 'op2'], ['option3', 'op3'], ['option4', 'op4']];
const insertList = ['herName', 'herAnswer'];
// データ格納
//localStorage.clear();
let dataArray = {step: 0, lv1: 0, lv2: 0, lv3: 0, op1: 0, op2: 0, op3: 0, op4: 0};
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
let hobbyForm = document.getElementById('hobby');
let meForm = document.getElementById('me');

nameForm.onchange = populateStorage;
ageForm.onchange = populateStorage;
areaForm.onchange = populateStorage;
jobForm.onchange = populateStorage;
hobbyForm.onchange = populateStorage;
meForm.onchange = populateStorage;

if (!localStorage.getItem('name')) {
    populateStorage();
} else {
    setStyles();
}

function populateStorage() {
    for (let i = 0;i < replaceWordList.length;i++){
        let replaceWord = replaceWordList[i][1];
        localStorage.setItem(replaceWord, document.getElementById(replaceWord).value);
    }
    setStyles();
}

function setStyles() {
    for (let j = 0;j < replaceWordList.length;j++){
        let setWord = replaceWordList[j][1];
        document.getElementById(setWord).value = localStorage.getItem(setWord);
    }
}

function selfIntroductionMaker() {
    let currentName = localStorage.getItem('name');
    let currentAge = localStorage.getItem('age');
    let currentArea = localStorage.getItem('area');
    let currentJob = localStorage.getItem('job');
    let currentHobby = localStorage.getItem('hobby');
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
    result = result.replace('(趣味)', currentHobby);
    return result
}

// 例文の表示
function replaceAll(str, before, after) {
    return str.split(before).join(after);
}

function baseTextChoice() {
    let dataArray = JSON.parse(localStorage.getItem('dataArray'));
    return mailTextList[mailList[Number(dataArray['step'])][Number(dataArray['lv1'])]]
}

function display_comment(baseText) {
    if (baseText.indexOf('[') !== -1) {
        let textList = baseText.split('[');
        baseText = textList[0];
        document.getElementById('comment').textContent = textList[1]
    }
    return baseText
}

function multipleOptionDisplay(baseText, optionCode) {
    let hAForm = document.getElementById(optionCode + 'Outer');
    if (baseText.indexOf(optionCode) !== -1) {
        hAForm.style.display = 'block';
    } else {
        hAForm.style.display = 'none'
    }
    return baseText
}

function displayText(clickId) {
    let baseText = baseTextChoice();
    let beforeReplace = baseText;
    baseText = display_comment(baseText);
    baseText = optionInsert(baseText);
    baseText = wordReplace(baseText);
    baseText = multipleOptionDisplay(baseText, 'herAnswer');
    if (clickId !== 'herAnswer') {
        document.getElementById('herAnswer').value = ''
    }
    if (baseText.indexOf('(自己紹介)') !== -1) {
        baseText = baseText.replace('(自己紹介)', selfIntroductionMaker())
    }
    baseText = wordInsert(baseText);
    document.getElementById('mailDisplay').innerHTML = '<p>' + replaceAll(baseText, '$$', '<br>')
        + '</p>';
    document.getElementById('mailDisplayD').value = replaceAll(baseText, '$$', '\n');
    return beforeReplace
}

function optionInsert(baseText) {
    let dataArray = JSON.parse(localStorage.getItem('dataArray'));
    for (let i = 0; i < optionWordList.length; i++) {
        if (baseText.indexOf(optionWordList[i][0]) !== -1) {
            let optionValue = Number(dataArray[optionWordList[i][1]]);
            let replaceWord = '(' + optionWordList[i][0] + ')';
            baseText = replaceAll(baseText, replaceWord, optionArray[i][optionValue]);
        }
    }
    return baseText
}

function wordInsert(baseText) {
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
    return baseText
}

function wordReplace(baseText) {
    for (let i = 0; i < replaceWordList.length; i += 1) {
        let replaceWord = replaceWordList[i];
        if (baseText.indexOf(replaceWord[0]) !== -1) {
            baseText = replaceAll(baseText, replaceWord[0], localStorage.getItem(replaceWord[1]))
        }
    }
    return baseText
}

// 各所クリックで例文更新
let selectFormHerName = document.getElementById("herName");
selectFormHerName.onchange = displayTextHA;
let selectFormHerAnswer = document.getElementById("herAnswer");
selectFormHerAnswer.onchange = displayTextHA;
let selectFormTab1 = document.getElementById("tab-1");
selectFormTab1.onclick = displayTextHA;
function displayTextHA () {
    displayText('herAnswer')
}

// selectを表示
let selectFormStep = document.getElementById("step");
let selectFormLv1 = document.getElementById("lv1");
let selectFormOp1 = document.getElementById("op1");
let selectFormOp2 = document.getElementById("op2");
let selectFormOp3 = document.getElementById("op3");
let selectFormOp4 = document.getElementById("op4");

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


function choiceOptionId(optionNum, strArray) {
    let optionStr = '';
    let key = strArray[0];
    let labelId = optionNum + 'Label';
    for (let i = 1; i < strArray.length; i += 1) {
        optionStr += '<option value="' + String(i - 1) + '" selected>' + strArray[i] + '</option>\n';
    }
    document.getElementById(optionNum).innerHTML = optionStr;
    document.getElementById(labelId).textContent = key;
}

function makeOptionStr(optionNum) {
    console.log(optionNum);
    let optionId = optionNum + 'Outer';
    choiceOptionId(optionNum, optionLabel[optionNum]);
    let opForm = document.getElementById(optionNum);
    let opOutForm = document.getElementById(optionId);
    opOutForm.style.display = 'block';
    opForm.options[0].selected = true
}

function makeSelectStr(levelStr) {
    console.log(levelStr);
    let selectOrder = makeSelectOrder(levelStr);
    choiceOptionId(levelStr, labelArray[selectOrder]);
    /*
    let strArray = labelArray[selectOrder];
    let optionStr = '';
    let key = strArray[0];
    let labelId = levelStr + 'Label';
    for (let i = 1; i < strArray.length; i += 1) {
        optionStr += '<option value="' + String(i - 1) + '" selected>' + strArray[i] + '</option>\n';
    }
    document.getElementById(levelStr).innerHTML = optionStr;
    document.getElementById(labelId).textContent = key;
    */
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
    if (arrayData['step'] === 2) {
        document.getElementById('herNameOuter').style.display = 'none'
    } else {
        document.getElementById('herNameOuter').style.display = 'block'
    }
    let currentText = displayText();
    console.log(currentText);
    optionSelectDisplay(currentText)
}

function optionSelectDisplay(currentText) {
    for (let i = 0; i < optionWordList.length; i++) {
        console.log(optionWordList[i][0]);
        console.log(currentText.indexOf(optionWordList[i][0]) !== -1);
        if (currentText.indexOf(optionWordList[i][0]) !== -1) {
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

function selectChangeOp4() {
    console.log('selectChangeOp4 start');
    optionClicked('op4')
}

selectFormStep.onchange = selectChangeStep;
selectFormLv1.onchange = selectChangeLv1;
selectFormOp1.onchange = selectChangeOp1;
selectFormOp2.onchange = selectChangeOp2;
selectFormOp3.onchange = selectChangeOp3;
selectFormOp4.onchange = selectChangeOp4;


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
    document.getElementById('op4').options[Number(currentData['op4'])].selected = true;
}

firstInitialize();

//todo: xcc対策