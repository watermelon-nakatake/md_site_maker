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
};　/*自動生成*/
const maxSelectLength = 5;  /*自動生成*/
const inputFormLength = 5;  /*自動生成*/
const optionDict = {
    '00': '普通のプロフィール', '01': '婚活用プロフィール', '02': '恋活用プロフィール', '03': 'メル友プロフ',
    '10': '普通のメール', '11': '婚活用メール', '12': '恋活用メール', '13': 'メル友メール',
    '000': '真面目な感じ', '001': 'フランクな感じ', '002': 'シンプルな感じ', '003': '誠実な感じ'
}  /*自動生成*/
const labelDict = {'0': 'プロフィールの目的', '1': 'メールの目的', '00': 'どんな感じで？'};
const mailInputDict = {'001': ['趣味']};
const mailSelectDict = {'001': ['映画', '料理', 'スポーツ', '読書']};
const profileDataIndex = {'name': '名前', 'age': '年齢', 'area': '住所', 'hobby': '趣味', 'sex': '性別'};　/*profの対照用*/
const testProfData = {'name': 'ごろう', 'age': '33才', 'hobby': 'ゲーム', 'sex': '男'};  /*テスト用の仮データ*/
const profileList = ['名前', '年齢', '住所', '性別'] 　/*profデータに入れるべき項目のリスト 自動生成*/

let viewObj = {
    initialView: function () {
        for (let i = 1; i < modelObj.inputData.length; i++) {
            this.makeOptionStr(modelObj.inputData.slice(i))
        }
        if (modelObj.inputData in sampleDict) {
            this.mailSampleDisplay(modelObj.inputData)
        }
    },
    makeOptionStr: function (preCode) {
        const selectID = 'sO' + String(preCode.length)
        console.log('selectID : ' + selectID);
        let optStr = '<option value="s" selected hidden>選択してください</option>';
        for (let orderNum = 0; orderNum < maxSelectLength; orderNum += 1) {
            if (preCode + orderNum in optionDict) {
                optStr += '<option value="' + preCode + String(orderNum) + '">' + optionDict[preCode + String(orderNum)]
                    + "</option>\n"
            }
        }
        // console.log(optStr)
        document.getElementById(selectID).innerHTML = optStr;
        document.getElementById(selectID + 'Label').textContent = labelDict[preCode];
        document.getElementById(selectID + 'Outer').style.display = 'block'
    },
    makeInputForm: function () {
        console.log(modelObj.mailStr);
        if (modelObj.mailStr.indexOf('((') !== -1) {
            let matchList = modelObj.mailStr.match(/\(\(.*?\)\)/g);
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
    mailSampleDisplay: function () {
        let dspStr = modelObj.mailStr;
        if (dspStr.indexOf('((') !== -1){
            dspStr = dspStr.split('((').join('(')
            dspStr = dspStr.split('))').join(')')
        }
        document.getElementById('mailText').textContent = dspStr
    },

    inputDisplay: function (beforeW, afterW) {
        modelObj.replaceWord(beforeW, afterW);
        document.getElementById('mailText').textContent = modelObj.mailStr
    }
};

let controllerObj = {
    currentID : '',
    currentValue : '',
    currentLabel : '',
    changeSelect: function (selectID) {
        this.currentID = selectID;
        this.currentValue = document.getElementById(selectID).value;
        console.log('changeOption => preCode : ' + this.currentValue);
        modelObj.changeSelect()
    },
    changeInput: function (inputID) {
        console.log('start changeInputOption');
        this.currentID = inputID;
        this.currentValue = document.getElementById(inputID).value;
        this.currentLabel = document.getElementById(inputID + 'Label').textContent;
        modelObj.changeInput()
    }
}

let modelObj = {
    inputData: '',
    profData: {},
    optionData: {},
    mailStr: '',
    displayMailStr: function () {
        this.mailStr = sampleDict[viewObj.inputData];
        this.insertProfileData();
        viewObj.makeInputForm();
        viewObj.mailSampleDisplay()
    },
    
    changeSelect: function () {
        let preCode = controllerObj.currentValue;
        console.log(preCode);
        viewObj.inputData = preCode;
        if (preCode in sampleDict) {
            this.mailStr = sampleDict[preCode];
            this.insertProfileData();

        } else {
            viewObj.makeOptionStr(preCode);
            this.mailStr = '例文本文';
        }
        viewObj.makeInputForm();
        viewObj.mailSampleDisplay()
    },

    changeInput: function (){
        let inputLabel = controllerObj.currentLabel
        if (inputLabel in profileList) {
            viewObj.profData[inputLabel] = this.inputData
        }
        viewObj.inputDisplay(inputLabel, this.inputData);
        console.log(viewObj.profData)
        this.replaceWord()
    },
    insertProfileData: function () {
        for (let key in profileDataIndex) {
            if (this.mailStr.indexOf('((' + profileDataIndex[key] + '))') !== -1 && key in testProfData) {
                this.mailStr = this.mailStr.replace('((' + profileDataIndex[key] + '))', testProfData[key])
            }
        }
    },
    checkBlank: function () {

    },
    initializeSession: function () {
        let inputData = JSON.parse(localStorage.getItem("inputData"));
        if (inputData !== null) {
            viewObj.inputData = inputData
        } else {
            viewObj.inputData = '0'
        }
        console.log(viewObj.inputData);
        let profData = JSON.parse(localStorage.getItem("profData"));
        if (profData !== null) {
            viewObj.profData = profData
        } else {
            viewObj.profData = {}
        }
        console.log(viewObj.profData);
        let optionData = JSON.parse(localStorage.getItem("optionData"));
        if (optionData !== null) {
            viewObj.optionData = optionData
        } else {
            viewObj.optionData = {}
        }
        console.log(viewObj.optionData);
    },

    removeLocalStorage: function () {
        const lsDataList = ['inputData', 'profData', 'optionData'];
        for (let i = 0; i < lsDataList.length; i++) {
            localStorage.removeItem(lsDataList[i])
        }
    },
    replaceWord: function (beforeW, afterW){
        let sStr = this.mailStr.split('((' + beforeW + '))');
        this.mailStr = sStr.join(afterW)
    },

    rewriteInputData: function () {
        localStorage.setItem("inputData", JSON.stringify(viewObj.inputData))
    },

    rewriteProfData: function () {
        localStorage.setItem("profData", JSON.stringify(viewObj.profData))
    },

    rewriteOptionData: function () {
        localStorage.setItem("optionData", JSON.stringify(viewObj.optionData))
    }
}

// viewObj.makeOptionStr('sO1', '00');
// modelObj.removeLocalStorage();
modelObj.initializeSession();
viewObj.initialView()