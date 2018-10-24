$(function () {
        //发送验证码
        let $smsCaptchaBtn = $(".form-item .sms-captcha");
        let $telephone = $("input[name=telephone]");
        let reg = /^((1[3-9][0-9])+\d{8})$/;

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

                        let count = 10;
                        let $text = $(this).text();
                        $(this).attr('disabled', true);
                        let timer = setInterval(() => {
                            $(this).text(count);
                            count--;
                            if (count <= 0) {
                                clearInterval(timer);
                                $(this).text("重新发送验证码");
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


        //获取验证
        let $Verify = $(".login-btn");

        let $smsCaptcha = $("input[name=sms_captcha]");

        $Verify.click(function () {
            let telVal = $telephone.val();
            let smsCaptchaVal = $smsCaptcha.val().toLowerCase();
            console.log(`1 ${telVal}  2 ${smsCaptchaVal} `);

            $.post({
                url: "/account/reset_password",
                data: {
                    "telephone": telVal,
                    "sms_captcha": smsCaptchaVal,
                },
                success: res => {
                    console.log(res);
                    if (res["code"] === 200) {

                        window.message.showSuccess("手机验证成功");
                        setTimeout(() => {
                            window.location.href = '/account/login';
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