'use strict'

// const sampleDict = {
//     '00': 'はじめまして。こんにちは。ありがとうございます。((１))３((年齢))え((る))あ((お))い((かか))00',
//     '01': 'はじめまして。こんにちは。ありがとうございます。((も))01',
//     '02': 'はじめまして。こんにちは。ありがとうございます。自分は((名前))です。住んでいるのは((住所))です。02',
//     '03': 'はじめまして。こんにちは。ありがとうございます。03',
//     '10': 'はじめまして。こんにちは。ありがとうございます。10',
//     '11': 'はじめまして。こんにちは。ありがとうございます。11',
//     '12': 'はじめまして。こんにちは。ありがとうございます。12',
//     '13': 'はじめまして。こんにちは。ありがとうございます。13'
// };　/*自動生成*/
// const maxSelectLength = 5;  /*自動生成*/
// const optionDict = {
//     '00': '普通のプロフィール', '01': '婚活用プロフィール', '02': '恋活用プロフィール', '03': 'メル友プロフ',
//     '10': '普通のメール', '11': '婚活用メール', '12': '恋活用メール', '13': 'メル友メール',
//     '000': '真面目な感じ', '001': 'フランクな感じ', '002': 'シンプルな感じ', '003': '誠実な感じ'
// }  /*自動生成*/
// const labelDict = {'0': 'プロフィールの目的', '1': 'メールの目的', '00': 'どんな感じで？'};

const inputFormLength = 5;
const profileFormLength = 7;

// const profileDataIndex = {'name': '名前', 'age': '年齢', 'area': '住所', 'hobby': '趣味', 'sex': '性別'};　/*profの対照用*/
const testProfData = {'名前': 'ごろう', '年齢': '33才', '趣味': 'ゲーム', '性別': '男'};  /*テスト用の仮データ*/
const profileListBase = ['名前', '年齢', '住所', '性別', '自分']; 　/*profデータに入れるべき項目のリスト*/
const cnfList = ['saveMail', 'lineSpacing', 'saveName', 'accessWay'];

let viewObj = {
    initialView: function () {
        let inputData = modelObj.inputData;
        for (let i = 1; i < inputData.length; i++) {
            this.makeSelectStr(inputData.slice(0, i))
        }
        if (inputData in sampleDict) {
            this.mailTextDisplay(inputData)
        }
        this.selectFill();
        this.makeProfileForm();
        this.makeConfigForm()
    },

    makeSelectStr: function (preCode) {
        // selectを変更した際に次以降のselectボックスを消す
        const selectID = 'sO' + String(preCode.length)
        console.log('selectID : ' + selectID);
        let optStr = '<option value="s" selected hidden>選択してください</option>';
        for (let orderNum = 0; orderNum < maxSelectLength; orderNum += 1) {
            if (preCode + String(orderNum) in optionDict) {
                optStr += '<option value="' + preCode + String(orderNum) + '">' + optionDict[preCode + String(orderNum)]
                    + "</option>\n"
            }
        }
        // console.log(optStr)
        document.getElementById(selectID).innerHTML = optStr;
        document.getElementById(selectID + 'Label').textContent = labelDict[preCode];
        document.getElementById(selectID + 'Outer').style.display = 'block';
    },

    selectFill: function () {
        let inputData = modelObj.inputData;
        for (let i = 0; i < inputData.length; i++) {
            document.getElementById('sO' + String(i)).options[Number(inputData[i]) + 1].selected = true
        }
    },

    makeInputForm: function (blankList) {
        for (let i = 0; i < inputFormLength; i++) {
            if (i < blankList.length) {
                let blankName = blankList[i].replace('((', '').replace('))', '');
                document.getElementById('ip' + String(i) + 'Label').textContent
                    = blankName;
                document.getElementById('ip' + String(i) + 'Outer').style.display = 'block'
                if (blankName === '相手の名前' && modelObj.configData['saveName'] && modelObj.partnerName !== '') {
                    document.getElementById('ip' + String(i)).value = modelObj.partnerName
                }
            } else {
                document.getElementById('ip' + String(i) + 'Outer').style.display = 'none'
            }
        }
    },

    delInputValue: function () {
        for (let i = 0; i < inputFormLength; i++) {
            document.getElementById('ip' + String(i)).value = ''
        }
    },

    makeProfileForm: function () {
        for (let i = 0; i < profileFormLength; i++) {
            if (i < modelObj.profileList.length) {
                document.getElementById('pr' + String(i) + 'Label').textContent = modelObj.profileList[i];
                document.getElementById('pr' + String(i) + 'Outer').style.display = 'block'
                if (modelObj.profileList[i] in modelObj.profData) {
                    document.getElementById('pr' + String(i)).value = modelObj.profData[modelObj.profileList[i]];
                }
            } else {
                document.getElementById('pr' + String(i) + 'Outer').style.display = 'none'
            }
        }
    },

    makeConfigForm: function () {
        for (let i = 0; i < cnfList.length; i++) {
            document.getElementById(cnfList[i]).checked = modelObj.configData[cnfList[i]]
        }

    },

    mailTextDisplay: function () {
        console.log('mail display');
        let dspStr = modelObj.mailStr;
        console.log(dspStr);
        if (dspStr.indexOf('(comment)') !== -1) {
            let spList = dspStr.split('(comment)');
            dspStr = spList[0];
            let commentStr = spList[1];
            commentStr = commentStr.split('$$$').join('</p><p>');
            commentStr = commentStr.split('$$').join('<br>')
            document.getElementById('commentText').innerHTML = commentStr
        }
        if (dspStr.indexOf('((') !== -1) {
            dspStr = dspStr.split('((').join('(')
            dspStr = dspStr.split('))').join(')')
        }
        if (modelObj.configData['lineSpacing']) {
            dspStr = dspStr.split('$$$').join('</p><p>');
            dspStr = dspStr.split('$$').join('<br>')
        } else {
            dspStr = dspStr.split('$$$').join('<br>');
            dspStr = dspStr.split('$$').join('')
        }
        this.insertCopyText(dspStr);

        if (dspStr.indexOf('<<') !== -1) {
            dspStr = dspStr.split('<<').join('<span class="replaced">')
            dspStr = dspStr.split('>>').join('</span>')
        }
        dspStr = '<p>' + dspStr + '</p>'
        console.log(dspStr);
        document.getElementById('mailText').innerHTML = dspStr
    },

    insertCopyText: function (dspStr) {
        dspStr = dspStr.split('</p><p>').join('\n\n');
        dspStr = dspStr.split('<br>').join('\n');
        dspStr = dspStr.split('<<').join('');
        dspStr = dspStr.split('>>').join('');
        document.getElementById('mailDisplay').value = dspStr
    },

    delMailText: function () {
        document.getElementById('mailText').textContent = '例文'
    },

    changeTab: function (clicked) {
        for (let i = 1; i < 4; i++) {
            let cID = 'tab' + String(i)
            if (clicked === cID) {
                if (!(document.getElementById(cID).classList.contains('active'))) {
                    document.getElementById(cID).classList.add('active')
                }
                document.getElementById(cID + 'c').style.display = 'block'
            } else {
                document.getElementById(cID).classList.remove('active')
                document.getElementById(cID + 'c').style.display = 'none'
            }
        }
    }
}

let controllerObj = {
    currentID: '',
    currentValue: '',
    currentLabel: '',
    currentPrfID: '',
    currentPrfValue: '',
    currentPrfLabel: '',
    currentCnfID: '',
    currentCnfValue: true,

    changeSelect: function (selectID) {
        this.currentID = selectID;
        this.currentValue = document.getElementById(selectID).value;
        console.log('changeSelect => preCode : ' + this.currentValue);
        modelObj.changeSelect(this.currentValue)
    },

    changeInput: function (inputID) {
        console.log('start changeInput');
        console.log(inputID);
        this.currentID = inputID;
        this.currentValue = document.getElementById(inputID).value;
        this.currentLabel = document.getElementById(inputID + 'Label').textContent;
        console.log(this.currentValue);
        modelObj.changeInput()
    },

    changeProfile: function (inputID) {
        console.log('start changeProfile');
        console.log(inputID);
        this.currentPrfID = inputID;
        this.currentPrfValue = document.getElementById(inputID).value;
        this.currentPrfLabel = document.getElementById(inputID + 'Label').textContent;
        console.log(this.currentPrfValue);
        modelObj.changeProfile()
    },

    changeConfig: function (inputID) {
        console.log('start changeConfig');
        this.currentCnfID = inputID;
        this.currentCnfValue = document.getElementById(inputID).checked;
        modelObj.changeConfig()
    },

    copyButton: function (clickID) {
        console.log("push copy");
        modelObj.copyText(clickID)
    }
}

let modelObj = {
    inputData: '',
    profData: {},
    configData: {'saveMail': false, 'lineSpacing': false, 'saveName': false, 'accessWay': false},
    currentInputDict: {},
    insertList: [],
    profileList: [],
    partnerName: '',
    baseStr: '例文',
    mailStr: '例文',

    displayMailStr: function () {
        const blankList = this.insertBlank();
        viewObj.makeInputForm(blankList);
        viewObj.mailTextDisplay()
    },

    copyText: function (targetID) {
        let copyTarget = document.getElementById(targetID);
        copyTarget.select();
        document.execCommand("Copy");
        alert("コピーできました")
    },

    changeSelect: function (preCode) {
        this.inputData = preCode;
        this.rewriteInputData();
        this.currentInputDict = {};
        this.insertList = []
        viewObj.delInputValue();
        if (preCode in sampleDict) {
            this.baseStr = sampleDict[preCode];
            this.mailStr = sampleDict[preCode];
            this.displayMailStr()
        } else {
            viewObj.makeSelectStr(preCode);
            this.baseStr = '例文';
            this.mailStr = '例文';
            viewObj.delMailText()
        }
    },

    changeInput: function () {
        let inputLabel = controllerObj.currentLabel;
        if (this.profileList.indexOf(inputLabel) !== -1) {
            this.profData[inputLabel] = controllerObj.currentValue;
            this.rewriteProfData();
            viewObj.makeProfileForm()
        } else if (inputLabel === '相手の名前' && this.configData['saveName'] === true) {
            this.partnerName = controllerObj.currentValue;
            this.rewritePartnerName();
            console.log(this.partnerName);
        }
        this.currentInputDict[inputLabel] = controllerObj.currentValue;
        console.log(this.profData);
        this.displayMailStr()
    },

    changeProfile: function () {
        let inputLabel = controllerObj.currentPrfLabel;
        this.profData[inputLabel] = controllerObj.currentPrfValue;
        if (this.baseStr !== '例文' && this.insertList.indexOf(inputLabel) !== -1) {
            this.currentInputDict[inputLabel] = controllerObj.currentPrfValue;
            this.displayMailStr()
        }
        this.rewriteProfData();
        console.log(this.profData);
    },

    changeConfig: function () {
        let inputLabel = controllerObj.currentCnfID;
        this.configData[inputLabel] = controllerObj.currentCnfValue;
        if (inputLabel === 'saveName' && controllerObj.currentCnfValue === false){
            this.partnerName = ''
        }
        if (this.baseStr !== '例文') {
            this.displayMailStr()
        }
        this.rewriteConfigData();
        console.log(this.configData);
    },

    insertBlank: function () {
        let matchList = this.baseStr.match(/\(\(.*?\)\)/g);
        console.log(matchList)
        this.insertList = matchList;
        let blankList = [];
        if (matchList !== null) {
            let newStr = this.baseStr;
            for (let i = 0; i < matchList.length; i++) {
                let cLabel = matchList[i].replace('((', '').replace('))',
                    '');
                if (this.profileList.indexOf(cLabel) !== -1 && cLabel in this.profData) {
                    newStr = newStr.replace(matchList[i], '<<' + this.profData[cLabel] + '>>')
                } else if (cLabel === '相手の名前' && this.configData['saveName'] === true && this.partnerName !== '') {
                    newStr = newStr.replace('((相手の名前))', '<<' + this.partnerName + '>>');
                    if (blankList.indexOf('相手の名前') === -1) {
                        blankList.push('相手の名前')
                    }
                    console.log(this.partnerName)
                } else if (cLabel === 'メール') {
                    if (this.configData['accessWay']) {
                        newStr = newStr.replace('((メール))', '<<いいね>>')
                    } else {
                        newStr = newStr.replace('((メール))', '<<メール>>')
                    }
                } else {
                    if (cLabel in this.currentInputDict) {
                        newStr = newStr.replace(matchList[i], '<<' + this.currentInputDict[cLabel] + '>>')
                    }
                    if (blankList.indexOf(cLabel) === -1) {
                        blankList.push(cLabel);
                        console.log(blankList)
                    }
                }
            }
            modelObj.mailStr = newStr
        }
        return blankList
    },

    initializeSession: function () {
        let profData = JSON.parse(localStorage.getItem("profData"));
        console.log(profData);
        if (profData !== null) {
            this.profData = profData
        } else {
            this.profData = {}
        }
        // this.profData = testProfData;  /*テスト*/
        console.log(this.profData);
        let confData = JSON.parse(localStorage.getItem("configData"));
        if (confData !== null) {
            this.configData = confData
        } else {
            this.configData = {'saveMail': false, 'lineSpacing': false, 'saveName': false, 'accessWay': false}
        }
        console.log(this.configData);
        let prfList = JSON.parse(localStorage.getItem("profileList"));
        if (prfList !== null) {
            this.profileList = confData
        } else {
            this.profileList = profileListBase
        }
        console.log(this.profileList);
        let partnerN = localStorage.getItem("partnerName");
        if (partnerN !== null) {
            this.partnerName = partnerN
        } else {
            this.partnerName = ''
        }
        console.log(this.configData);
        console.log(this.partnerName)
        let inputData = JSON.parse(localStorage.getItem("inputData"));
        if (inputData !== null && inputData in sampleDict && this.configData['saveMail'] === true) {
            this.inputData = inputData;
            this.baseStr = sampleDict[inputData];
            this.mailStr = sampleDict[inputData];
            let blankList = this.insertBlank();
            viewObj.makeInputForm(blankList)
        } else {
            this.inputData = '0';
            console.log(this.inputData);
        }
        viewObj.initialView()
    },

    removeLocalStorage: function () {
        const lsDataList = ['inputData', 'profData', 'configData'];
        for (let i = 0; i < lsDataList.length; i++) {
            localStorage.removeItem(lsDataList[i])
        }
    },

    rewriteInputData: function () {
        localStorage.setItem("inputData", JSON.stringify(this.inputData))
    },

    rewriteProfData: function () {
        localStorage.setItem("profData", JSON.stringify(this.profData))
    },

    rewriteConfigData: function () {
        localStorage.setItem("configData", JSON.stringify(this.configData))
    },

    rewritePartnerName: function () {
        localStorage.setItem("partnerName", this.partnerName)
    }
}


// viewObj.makeOptionStr('sO1', '00');
// modelObj.removeLocalStorage();
modelObj.initializeSession();
