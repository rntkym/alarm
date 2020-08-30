//警報通知スプレッドシート
var spreadsheet = SpreadsheetApp.openById('スプレッドシートID');
var sheet = spreadsheet.getSheetByName('シート名');
var lastRow = sheet.getLastRow();

//年間カレンダー（1年の予定が縦1列に表示されたスプレッドシート）
var spreadsheet2 = SpreadsheetApp.openById(sheet.getRange('I2').getValue());
var sheet2 = spreadsheet2.getSheetByName(sheet.getRange('I3').getValue());
var start = sheet.getRange('I4').getValue();
var firstRow = sheet.getRange('I5').getValue();
var day = 24 * 60 * 60 * 1000;

//通知したい警報の種類
var wordList = ['暴風雪', '暴風', '大雨', '洪水', '大雪'];

//全ての警報をまとめて通知するチャンネルのWebhookURL
var generalUrl = 'チャンネルのWebhookURL';

//毎日午後7~8時のどこかで翌日7時ののトリガーをセット
function setTrigger() {
  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var row = Math.floor((tomorrow - start) / day) + firstRow;
  var status = sheet2.getRange('Y' + row).getValue();

  //翌日が休日でない場合のみセット
  if(status.indexOf('休日') == -1){
    tomorrow.setHours(7);
    tomorrow.setMinutes(00);
    ScriptApp.newTrigger('alarm').timeBased().at(tomorrow).create();
  }
}

function postMessage(message, webhookUrl) {
  var jsonData =
  {
     "username" : "警報通知",
     "text" : message
  };
  var payload = JSON.stringify(jsonData);

  var options =
  {
    "method" : "post",
    "contentType" : "application/json",
    "payload" : payload
  };
  UrlFetchApp.fetch(webhookUrl, options);
}

function alarm() {
  var messageList = '';

  for(var i = 2; i < lastRow + 1; i++){
    var id = sheet.getRange('B' + i).getValue();
    var place1 = sheet.getRange('C' + i).getValue();
    var place2 = sheet.getRange('D' + i).getValue();
    var webhookUrl = sheet.getRange('F' + i).getValue();
    var html = UrlFetchApp.fetch('https://www.jma.go.jp/jp/warn/f_' + id + '.html').getContentText();
    //最初のWarnTextTableを取得
    var warnTextTable = Parser.data(html).from('<table class="WarnTextTable" cellspacing="0">').to('</table>').build();
    var alarm = Parser.data(warnTextTable).from('<span style="color:#FF2800">').to('</span>').iterate();
    var message = '';

    for(var j = 0; j < alarm.length; j++){
      if(alarm[0].indexOf('警報') == -1){
        break;
      }
      for(var k = 0; k < wordList.length; k++){
        if(alarm[j].indexOf(wordList[k]) != -1){
          message += (wordList[k] + ', ');
        }
      }
    }
    if(message.length){
      message = message.slice(0, -2);
      messageList += place2 + '：' + message + '警報\n';
      message = '<!channel>\n午前7時現在、' + place1 + place2 + 'に' + message + '警報が発令中です。'
      postMessage(message, webhookUrl);
    }
    sleep();
  }
  if(messageList.length){
    messageList = '<!channel>\n' + messageList;
    postMessage(messageList, generalUrl);
  }
}

function sleep(){
  var d1 = new Date().getTime();
  var d2 = new Date().getTime();
  while(d2 < d1 + 1000){
    d2 = new Date().getTime();
  }
}
