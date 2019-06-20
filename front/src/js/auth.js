// $(function () {
//     // $("#btn").click(function () {
//     //     $(".mask-wrapper").show();
//     //
//     // });
//     // $(".close-btn").click(function () {
//     //     $(".mask-wrapper").hide();
//     // });
// });

$(function () {
    $(".switch").click(function () {
        var scrollWrapper = $(".scroll-wrapper");
        var currentLeft = scrollWrapper.css("left");
        currentLeft = parseInt(currentLeft);

        if(currentLeft<0) scrollWrapper.animate({"left":"0"})
        else scrollWrapper.animate({"left":"-400px"})
    });
});

function Auth() {
    var self = this;
    self.maskWrapper = $('.mask-wrapper');
    self.scrollWrapper = $(".scroll-wrapper");
}

Auth.prototype.showEvent = function(){
    var self = this;
    self.maskWrapper.show();
};
Auth.prototype.hideEvent = function(){
    var self = this;
    self.maskWrapper.hide();
};
Auth.prototype.listenShowHideEvent = function(){
    var self =this;
    var signinBtn = $('.signin-btn');
    var signupBtn = $('.signup-btn');
    var closeBtn = $('.close-btn');

    signinBtn.click(function () {
        self.showEvent();
        self.scrollWrapper.css({"left":0});
    });
    signupBtn.click(function () {
        self.showEvent();
        self.scrollWrapper.css({"left":"-400px"});
    });
    closeBtn.click(function () {
        self.hideEvent();
    })

};
Auth.prototype.listenSwitchEvent = function(){
    var self =this;
    var switcher = $('.switch');

    switcher.click(function () {
        var currentLeft = self.scrollWrapper.css("left");
        currentLeft = parseInt(currentLeft);

        if(currentLeft<0) self.scrollWrapper.animate({"left":"0"})
        else self.scrollWrapper.animate({"left":"-400px"})
    });
};
Auth.prototype.listenSigninEvent = function() {
    var self =this;
    var signingroup = $('.signin-group');
    var telephone = signingroup.find("input[name='telephone']");
    var password = signingroup.find("input[name='password']");
    var remember = signingroup.find("input[name='remember']");

    var submitbtn = signingroup.find(".submit-btn");
    submitbtn.click(function () {

        var telephoneInput = telephone.val();
        var passwordInput = password.val();
        var rememberInput = remember.prop("checked");

        xfzajax.post({
           "url":"/account/login/",
           'data':{
               'telephone':telephoneInput,
               'password':passwordInput,
               'remember':rememberInput?1:0,
           },
            'success':function(result) {
                if(result['code'] == 200){
                    self.hideEvent();
                    window.location.reload();
                }
                else{
                    var messageObject = result['message'];
                    if(typeof messageObject == 'string' || messageObject.constructor == String){
                        window.messageBox.show(messageObject);
                    }else{
                        // {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
                        for(var key in messageObject){
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message);
                        }
                    }
                }

            },
            'fail':function(error){
                console.log(error);
            },
        });

    })


};
Auth.prototype.run = function () {
    var self = this;
    self.listenShowHideEvent();
    self.listenSwitchEvent();
    self.listenSigninEvent();
};





//全加载完才执行
$(function () {
    var auth = new Auth();
    auth.run();
});