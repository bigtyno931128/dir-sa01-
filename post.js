// 한줄평 남기기 //
let titleBucket = '';

function readTitle() {
  // title 저장을 위한 변수 선언
  const details = document.querySelectorAll('.modal_detailView');

  details.forEach(function (modal_detailView) {
    details.addEventListener('click', clickDetail);
  });

  function clickDetail(e) {
    let identify = e.currentTarget.getAttribute('data-bs-whatever');
    // titleBucket에 title값을 넣어줍니다
    titleBucket = identify;
  }
}

function com_post() {
    let com = $("#textarea-post").val()
    let today = new Date().toISOString()
    let identify = titleBucket;

    if (com == "") {
        alert("후기를 입력해주세요!")
        return;
    }

    $.ajax({
        type: "POST",
        url: "/item/comment",
        data: {
            com_give: com,
            date_give: today,
            identify_give: identify

        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}

  function post_comment(targetItemId) {
                let comment = $("#userComment").val()
                let post_id = targetItemId
                console.log(post_id)
                $.ajax({
                    type: "POST",
                    url: "/posting",
                    data: {
                        comment_give: comment,
                        targetitemid_give:post_id
                    },
                    success: function (response) {
                        alert(response.result)
                        window.location.reload()
                    }
                })
            }

function get_posts() {
    let identify = titleBucket;
    $("#comment_box").empty()

    $.ajax({
        type: "GET",
        url: `/get_posts`,
        data: { identify_give: identify },
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

