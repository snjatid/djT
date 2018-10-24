// 富文本编辑器
$(function () {
    var E = window.wangEditor;
    var editor2 = new E('#news-content');
    editor2.create();


// ====================  传文件 ============================
  // 获取缩略图输入框元素
  let $thumbnailUrl = $("#news-thumbnail-url");

  // ================== 上传至七牛（云存储平台） ================
  let $progressBar = $(".progress-bar");
  fQINIU.upload({
    // 七牛空间域名
    "domain": "http://pgtt3m7zc.bkt.clouddn.com/",
    // 后台返回 token的地址
    "uptoken_url": "/admin_cms/up_token/",
    // 按钮
    "browse_btn": "upload-btn",
    // 成功
    "success": (up, file, info) => {
      let domain = up.getOption('domain');
      let res = JSON.parse(info);
      let filePath = domain + res.key;
      // console.log("----------",up,file,info);
      $thumbnailUrl.val('');
      $thumbnailUrl.val(filePath);
    },
    // 失败
    "error": (up, err, errTip) => {
      console.log('error');
      console.log(up);
      console.log(err);
      console.log(errTip);
      console.log('error');
    },
    // 上传文件的过程中 七牛对于 4M 秒传
    "progress": (up, file) => {
      let percent = file.percent;
      $progressBar.parent().css("display", 'block');
      $progressBar.css("width", percent + '%');
      $progressBar.text(parseInt(percent) + '%');
    },
    // 完成后 去掉进度条
    "complete": () => {
      $progressBar.parent().css("display", 'none');
      $progressBar.css("width", '0%');
      $progressBar.text('0%');
    }
  });



// ================== 上传至服务器 ================
  let $uploadThumbnail = $("#upload-news-thumbnail");
  $uploadThumbnail.change(function () {
    // 获取文件
    let file = this.files[0];
    // 创建一个 FormData
    let formData = new FormData();
    // 把文件添加进去
    formData.append("upload_file", file);
    // 发送请求
    $.ajax({
      url: "/admin_cms/upload_file/",
      method: "post",
      data: formData,
      // 定义文件的传输
      processData: false,
      contentType: false,
      success: res => {
        console.log(res);
        if (res["code"] === 200) {
          // 获取后台返回的 URL 地址
          let thumbnailUrl = res["data"]["file_url"];
          console.log(thumbnailUrl);

          $thumbnailUrl.val('');
          $thumbnailUrl.val(thumbnailUrl);
        }
      },
      error: err => {
        logError(err);
      }
    });
  });


   // ========= 发表新闻 ==========
  let $newsBtn = $("#btn-pub-news");
  $newsBtn.click(function () {
    let titleVal = $("#news-title").val();
    let descVal = $("#news-desc").val();
    let tagId = $("#news-category").val();
    let thumbnailVal = $thumbnailUrl.val();
    let contentHtml = editor2.txt.html();
    let contentText = editor2.txt.text();
    if (tagId === '0') {
      ALERT.alertInfoToast('请选择新闻标签')
    }
    console.log(`
      新闻标题: ${titleVal},
      新闻描述: ${descVal},
      新闻分类id: ${tagId},
      新闻缩略图地址: ${thumbnailVal}
      新闻内容html版: ${contentHtml},
      新闻内容纯文字版：${contentText}
    `);

    $.ajax({
      url: "/admin_cms/news_pub/",
      method: "post",
      data: {
        "title": titleVal,
        "desc": descVal,
        "tag_id": tagId,
        "thumbnail_url": thumbnailVal,
        "content": contentHtml,
      },
      dataType: "json",
      success: res => {
         console.log(res);
        if (res["code"] === 200) {
          ALERT.alertNewsSuccessCallback("新闻发表成功", '跳到首页', () => {
            window.location.href = '/';
          });
        } else {
          ALERT.alertErrorToast(res["msg"]);
        }
      },
      error: err => {
        logError(err)
      }
    })
  });


  });