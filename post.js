
function com_post() {
    let com = $("#textarea-post").val()
    let today = new Date().toISOString()

    if (com == "") {
        alert("후기를 입력해주세요!")
        return;
    }

    $.ajax({
        type: "POST",
        url: "/item/comment",
        data: {
            com_give: com,
            date_give: today

        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

function get_posts() {

    $("#comment_box").empty()

    $.ajax({
        type: "GET",
        url: `/get_posts`,
        data: { },
        success: function (response) {
            let posts = response["posts"]
            for (let i = 0; i < posts.length; i++) {
                let post = posts[i]
                let time_post = new Date(post["date"])
                let time_before = time2str(time_post)

                let html_temp = `<div class="box $radius-large">                                        
                                      <div class="review">
                                        <strong>${post['username']}</strong> <small>&nbsp;</small> <small>${time_before}</small> <!--{ 작성자 닉네임 | 아이디 | 작성시간 넣기 }} -->
                                        &nbsp;
                                        ${post['comment']}
                                        <br>
                                      </div> <!--{ comment 넣기 }} -->                                                                               
                                  </div>`
                $("#comment_box").append(html_temp)
            }

        }
    })
}

function time2str(date) {
    let today = new Date()
    let time = (today - date) / 1000 / 60  // 분

    if (time < 60) {
        return parseInt(time) + "분 전"
    }
    time = time / 60  // 시간
    if (time < 24) {
        return parseInt(time) + "시간 전"
    }
    time = time / 24
    if (time < 7) {
        return parseInt(time) + "일 전"
    }
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

