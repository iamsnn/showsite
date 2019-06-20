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
                    window.location.reload();
            },
        });

    })

};
Auth.prototype.listenSignUpEvent = function(){
  var self = this;
  var signUpGroup = $('.signup-group');
  var submitBtn = signUpGroup.find(('.submit-btn'));
  submitBtn.click(function (event) {
        event.preventDefault();

        var telephoneInput = signUpGroup.find("input[name='telephone']");
        var usernameInput = signUpGroup.find("input[name='username']");
        var passwordInput1 = signUpGroup.find("input[name='password1']");
        var passwordInput2 = signUpGroup.find("input[name='password2']");
        var imgInput = signUpGroup.find("input[name='img_captcha']");

        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var password1 = passwordInput1.val();
        var password2 = passwordInput2.val();
        var img = imgInput.val();

        xfzajax.post({
            'url':'/account/register/',
            'data':{
                'telephone':telephone,
                'username':username,
                'img_captcha':img,
                'password1':password1,
                'password2':password2
            },
            'success':function (result) {
                window.location.reload();
            },
            'fail':function (error) {
                window.messageBox.showError('服务器内部错误！');
            }
      });


  });


};
Auth.prototype.listenImgCaptchaEvent = function(){
    var self = this;
    var img = $('.img-captcha');
    img.click(function () {
       img.attr("src","/account/img_captcha/"+"?random="+Math.random());
    });

};

Auth.prototype.run = function () {
    var self = this;
    self.listenShowHideEvent();
    self.listenSwitchEvent();
    self.listenSigninEvent();
    self.listenSignUpEvent();
    self.listenImgCaptchaEvent();
};


//全加载完才执行


function FrontBase() {

}
FrontBase.prototype.listenAuthBoxHover = function () {
    var self = this;
    var authbox = $('.auth-box');
    var userMoreBox = $('.user-more-box');
    authbox.hover(function () {
        userMoreBox.show();
    },function () {
        userMoreBox.hide();
    });
};

FrontBase.prototype.run = function () {
    var self = this;
    self.listenAuthBoxHover();
};
$(function () {
   if(window.template){
       template.defaults.imports.time_since = function (dateValue) {
        var date = new Date(dateValue);
        var datestamp = date.getTime();
        var nowstamp = (new Date()).getTime();
        var timestamp = (nowstamp-datestamp)/1000;
    if(timestamp < 60)
        return "刚刚";
    else if(timestamp >= 60&& timestamp < 60*60){
        minutes = parseInt(timestamp/60);
        return minutes+'分钟前';
    }
    else if(timestamp >= 60*60 && timestamp < 60*60*24){
        hours = parseInt(timestamp/60/60);
        return hours+'小时前';
    }
    else if(timestamp >= 60*60*24 && timestamp < 60*60*24*30){
        days = parseInt(timestamp/60/60/24);
        return days+'天前';
    }
    else {
            var year = date.getFullYear();
            var month = date.getMonth();
            var day = date.getDay();
            var hour = date.getHours();
            var minute = date.getMinutes();
            return year+'/'+month+'/'+day+" "+hour+":"+minute;
        }


    };
   }
});
$(function () {
    var auth = new Auth();
    auth.run();
});

$(function () {
    var frontbase = new FrontBase();
    frontbase.run();
});

