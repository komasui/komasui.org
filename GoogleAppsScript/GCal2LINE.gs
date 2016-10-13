// via http://developers.linecorp.com/blog/ja/?p=3784
// via http://qiita.com/shibukk/items/c26a64c63e26d0d5a967
// via http://qiita.com/Yuki_BB3/items/457fdba9dcb523f1069d

var AuthorizationCode ='Bearer 【ここにアクセストークンを入れる】';
var CalendarById = '【ここにカレンダーアイディーを入れる】';

function myFunction() {
  var msg = getCalendarEvent();
  if(msg){sendHttpPost(msg);}
}

// 翌日の日付を{year:'yyyy', month:'mm', date:'dd'}の形式で返す
function nextDate(year, month, date) {
    var d = new Date(year, month - 1, date);
    d.setDate(d.getDate() + 1);
    return {
        year: d.getFullYear(),
        month: d.getMonth() + 1,
        date: d.getDate()
    };
}

// Calendarから予定翌日の予定を取得し、メッセージとして返却する
function getCalendarEvent(){
  var message;
  // 翌日の日付を取得
  var today = new Date();
  var yyyy = today.getFullYear();
  var mm = today.getMonth()+1;
  var dd = today.getDate();
  var td = nextDate(yyyy, mm, dd);
  var targetDate = td.year + '/' + td.month + '/' + td.date;

  // 翌日の曜日を取得
  var week = ['日', '月', '火', '水', '木', '金', '土'];
  var ww = '(' + week[new Date(targetDate).getDay()] + ')';
  
  // GoogleCalendarからeventTitleを取得
  var myCals=CalendarApp.getCalendarById(CalendarById);
  var myEvents=myCals.getEventsForDay(new Date(targetDate));

  var strBody = td.month + '/' + td.date + ww + '\n';

  // eventがあればメッセージに格納
  if(myEvents){
      if (myEvents.length == 0) {
        return;
      }

      for(var i=0;i<myEvents.length;i++){
        var strTitle = myEvents[i].getTitle();
        var strStartTime = myEvents[i].getStartTime();
        var strEndTime = myEvents[i].getEndTime();
        var strLocation = myEvents[i].getLocation();
        var strDescription = myEvents[i].getDescription();

        
        if (myEvents[i].isAllDayEvent()) {
          strStartTime = "終日";
        } else {
          strStartTime = Utilities.formatDate(strStartTime, "GMT+0900", "HH:mm");
          strStartTime += Utilities.formatDate(strEndTime, "GMT+0900", "〜HH:mm ");
        }


        strBody = strBody + '\n'
                + '内容： ' + strTitle + '\n'
                + '日時： ' + strStartTime + '\n'
                + '場所： ' + strLocation + '\n'
                + '概要：\n' + strDescription + '\n'
                ; 
      }
    message = strBody;
  }
  return message;
}

// LINE NotifyにHTTP POSTでメッセージを送信する
function sendHttpPost(postMassage) {
   var payload ={
     "message": postMassage
   };

   var options ={
     "method" : "post",
     "headers": {
       Authorization: AuthorizationCode,
     },
     "payload" : payload
   };
   UrlFetchApp.fetch("https://notify-api.line.me/api/notify", options);
 }
