function News() {

}

News.prototype.initUEditor = function(){

    window.ue = UE.getEditor('editor',{
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });

};

News.prototype.listenUploadFileEvent = function(){
    var self = this;
    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            'processData':false,
            'contentType':false,
            'success':function (result) {
               if(result['code']===200){
                   var url = result['data']['url'];
                   //输入框
                   var thumbnailInput = $('#thumbnail-form');
                   thumbnailInput.val(url);

               }
            }
        });
    });
};
News.prototype.listenSubmitEvent = function(){
    var self = this;
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var pk = btn.attr('data-news-id');

        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();

        var url = '';
        if(pk){
            url = '/cms/edit_news/';
        }else{
            url = '/cms/write_news/';
        }

        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'pk': pk
            },
            'success': function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('新闻发表成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
};


News.prototype.run = function () {
    var self = this;
    self.listenUploadFileEvent();
    self.initUEditor();
    self.listenSubmitEvent();
};

$(function () {
   var news = new News();
   news.run();
});