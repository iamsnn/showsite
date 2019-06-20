function CMSNewsList() {

}

CMSNewsList.prototype.initDatePicker = function () {
    var startPicker = $("#start-picker");
    var endPicker = $("#end-picker");

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();

    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2019/1/1',
        'endDate': todayStr,
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true
    };
    startPicker.datepicker(options);
    endPicker.datepicker(options);
};

CMSNewsList.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        //当前按钮
        var btn = $(this);
        //绑定pk
        var news_id = btn.attr('data-news-id');
        xfzalert.alertConfirm({
            'text': '您是否要删除这篇新闻吗？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/delete_news/',
                    'data': {
                        'news_id': news_id
                    },
                    'success': function (result) {
                        if(result['code'] === 200){
                            //强制刷新
                            window.location = window.location.href;
                        }
                    }
                });
            }
        });
    });
};


CMSNewsList.prototype.run = function () {
    this.initDatePicker();
    this.listenDeleteEvent();
};

$(function () {
    var newsList = new CMSNewsList();
    newsList.run();
});