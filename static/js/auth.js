$(function () {
    // 获取按钮
    let $loginBtn = $(".login-btn");


    let $graphCaptchaBtn = $(".form-item .captcha-graph-img");
    let $captchaImg = $graphCaptchaBtn.find('img');


    $loginBtn.click(function () {

        let telVal = $("input[name=telephone]").val();
        let pwdVal = $("input[name=password]").val();
        let $remember = $("input[name=remember]");
        let status = $remember.is(":checked");
        // console.log(`${telVal}, ${pwdVal}`)
        // 验证会做两层 前端防止频繁的发送请求
        if (telVal && pwdVal) {     //不为空的时候执行
            data = {
                "telephone": telVal,
                "password": pwdVal,
            };

            if (status) {
                data.remember = status;
            }
            console.log(data);


            $.ajax({
                url: "/account/login",
                method: "post",
                data: data,
                dataType: "json",
                success: res => {
                    // console.log('success');
                    console.log(res);
                    if (res["code"] === 200) {
                        message.showSuccess("登录成功");
                        setTimeout(() => {
                            window.location.href = '/';
                        }, 1500);
                    } else {
                        message.showError(res["msg"])
                    }
                },
                error: err => {
                    // // 当 ajax 出现问题的时候 返回
                    // console.log('error');
                    // console.log(err);
                    logError(err);
                }
            })
        } else {
            message.showError("手机号和密码不能为空");
        }

    });


    // 刷新图形验证码
    $graphCaptchaBtn.click(function () {
        let oldSrc = $captchaImg.attr('src');
        let newSrc = oldSrc.split("?")[0] + "?_=" + Date.now();
        $captchaImg.attr('src', newSrc);
    });


    let $smsCaptchaBtn = $(".form-item .sms-captcha");
    let $telephone = $("input[name=telephone]");
    let reg = /^((1[3-9][0-9])+\d{8})$/;
    // 发送短信验证码
    $smsCaptchaBtn.click(function () {
        let $status = $(this)[0].hasAttribute('disabled');
        if ($status) {
            message.showInfo("验证码已经发送，请注意查收");
            return false
        }
        let telVal = $telephone.val();
        if (telVal && telVal.trim()) {
            if (reg.test(telVal)) {
                $.ajax({
                    url: "/account/sms_captcha",
                    method: "get",
                    data: {
                        "telephone": telVal,
                    },
                    success: res => {
                        // {"Message":"OK","RequestId":"15AAD9E6-5EE4-4A29-B356-850F2D11E013","BizId":"802713039445786543^0","Code":"OK"}
                        console.log(res);   //res  后台返回的是字符串
                        // console.log(typeof res);   //res  后台返回的是字符串
                        //stringify   js对象转成标准的Json格式
                        // let resObj = JSON.parse(res);
                        // // message.showSuccess(resObj["message"]);
                        // if (res['Code'] === 'OK') {
                        //     message.showSuccess(resObj["发送成功"]);
                        // } else {
                        //     message.showSuccess(resObj["发送失败"]);
                        // }

                        let count = 60;
                        let $text = $(this).text();
                        $(this).attr('disabled', true);
                        let timer = setInterval(() => {
                            $(this).text(count);
                            count--;
                            if (count <= 0) {
                                clearInterval(timer);
                                $(this).text($text);
                                $(this).removeAttr('disabled');
                            }
                        }, 1000);
                    },
                    error: err => {
                        logError(err);
                    }
                })
            } else {
                message.showError('手机号格式不正确');
                $telephone.focus();
            }
        } else {
            message.showError('请输入手机号');
            $telephone.focus();
        }
    });



    let $regBtn = $(".register-btn");

    let $smsCaptcha = $("input[name=sms_captcha]");
    let $username = $("input[name=username]");
    let $password = $("input[name=password]");
    let $passwordRepeat = $("input[name=password_repeat]");
    let $graphCaptcha = $("input[name=captcha_graph]");

    $regBtn.click(function () {
        let telVal = $telephone.val();
        let smsCaptchaVal = $smsCaptcha.val().toLowerCase();
        let userVal = $username.val();
        let pwdVal = $password.val();
        let pwdRepeatVal = $passwordRepeat.val();
        let graphCaptchaVal = $graphCaptcha.val().toLowerCase();
        console.log(`1 ${telVal}  2 ${smsCaptchaVal} 3 ${userVal} 4 ${pwdVal} 5 ${pwdRepeatVal} 6 ${graphCaptchaVal}`);

        $.post({
            url: "/account/register",
            data: {
                "telephone": telVal,
                "sms_captcha": smsCaptchaVal,
                "username": userVal,
                "password": pwdVal,
                "password_repeat": pwdRepeatVal,
                "graph_captcha": graphCaptchaVal,
            },
            success: res => {
                if (res["code"] === 200) {
                    console.log("*************");
                    window.message.showSuccess("注册成功js");
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1500)
                } else {
                    window.message.showError(res["msg"])
                }
            },
            error: err => {
                logError(err)
            }
        })

    });

});

