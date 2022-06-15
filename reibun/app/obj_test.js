'use strict'

const sampleDict = {
    '00': 'はじめまして。こんにちは。ありがとうございます。((１))３((年齢))え((る))あ((お))い((かか))00',
    '01': 'はじめまして。こんにちは。ありがとうございます。((も))01',
    '02': 'はじめまして。こんにちは。ありがとうございます。自分は((名前))です。住んでいるのは((住所))です。02',
    '03': 'はじめまして。こんにちは。ありがとうございます。03',
    '10': 'はじめまして。こんにちは。ありがとうございます。10',
    '11': 'はじめまして。こんにちは。ありがとうございます。11',
    '12': 'はじめまして。こんにちは。ありがとうございます。12',
    '13': 'はじめまして。こんにちは。ありがとうございます。13'
};
const maxSelectLength = 5;
const inputFormLength = 5;
const optionDict = {
    '00': '普通のプロフィール', '01': '婚活用プロフィール', '02': '恋活用プロフィール', '03': 'メル友プロフ',
    '10': '普通のメール', '11': '婚活用メール', '12': '恋活用メール', '13': 'メル友メール',
    '000': '真面目な感じ', '001': 'フランクな感じ', '002': 'シンプルな感じ', '003': '誠実な感じ'
}
const labelDict = {'0': 'プロフィールの目的', '1': 'メールの目的', '00': 'どんな感じで？'};
const mailInputDict = {'001': ['趣味']};
const mailSelectDict = {'001': ['映画', '料理', 'スポーツ', '読書']};
const profileDataIndex = {'name': '名前', 'age': '年齢', 'area': '住所', 'hobby': '趣味', 'sex': '性別'};
const testProfData = {'name': 'ごろう', 'age': '33才', 'hobby': 'ゲーム', 'sex': '男'};

let inputData = '';

let viewObj = {
    initialView: function () {
        if (inputData === '') {
            inputData = '0'
        } else {
            for (let i = 1; i < inputData.length; i++) {
                viewObj.makeOptionStr(inputData.slice(i))
            }
            if (inputData in sampleDict) {
                viewObj.mailSampleDisplay(inputData)
            }
        }
    },
    makeOptionStr: function (preCode) {
        const selectID = 'sO' + String(preCode.length)
        console.log('selectID : ' + selectID);
        let optStr = "";
        for (let orderNum = 0; orderNum < maxSelectLength; orderNum += 1) {
            if (preCode + orderNum in optionDict) {
                optStr += '<option value="' + preCode + String(orderNum) + '">' + optionDict[preCode + String(orderNum)]
                    + "</option>\n"
            }
        }
        console.log(optStr)
        // console.log(document.getElementById(selectID + 'Label'))
        document.getElementById(selectID).innerHTML = optStr;
        document.getElementById(selectID + 'Label').textContent = labelDict[preCode];
        document.getElementById(selectID + 'Outer').style.display = 'block'
    },
    makeInputForm: function (mailText) {
        if (mailText.indexOf('((') !== -1) {
            let matchList = mailText.match(/\(\(.*?\)\)/g);
            console.log(matchList);
            for (let i = 0; i < inputFormLength; i++) {
                if (i < matchList.length) {
                    document.getElementById('ip' + String(i) + 'Label').textContent
                        = matchList[i].replace('((', '').replace('))', '');
                    document.getElementById('ip' + String(i) + 'Outer').style.display = 'block'
                } else {
                    document.getElementById('ip' + String(i) + 'Outer').style.display = 'none'
                }
            }
        } else {
            for (let i = 0; i < inputFormLength; i++) {
                document.getElementById('ip' + String(i) + 'Outer').style.display = 'none'
            }
        }
    },
    mailSampleDisplay: function (preCode) {
        modelObj.choiceMailStr(preCode)
        let mailText = modelObj.insertProfileData();
        viewObj.makeInputForm(mailText);
        document.getElementById('mailText').textContent = mailText
    }
};

let controllerObj = {
    changeOption: function (selectID) {
        let preCode = document.getElementById(selectID).value;
        console.log('changeOption => preCode : ' + preCode);
        inputData = preCode;
        if (preCode in sampleDict) {
            viewObj.mailSampleDisplay(preCode)
        } else {
            viewObj.makeOptionStr(preCode);
            document.getElementById('mailText').textContent = '例文本文';
        }
    }
}

let modelObj = {
    mailStr: '',
    choiceMailStr: function (preCode){
        this.mailStr = sampleDict[preCode];
        return this.mailStr
    },
    insertProfileData: function () {
        for (let key in profileDataIndex) {
            if (this.mailStr.indexOf('((' + profileDataIndex[key] + '))') !== -1) {
                if (key in testProfData) {
                    this.mailStr = this.mailStr.replace('((' + profileDataIndex[key] + '))', testProfData[key])
                } else {
                    this.mailStr = this.mailStr.replace('((' + profileDataIndex[key] + '))',
                        '(' + profileDataIndex[key] + ')')
                }
            }
        }
        return this.mailStr
    }
}
// viewObj.makeOptionStr('sO1', '00');
viewObj.initialView()