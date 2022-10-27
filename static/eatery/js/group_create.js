const group_name = document.getElementById("name");
const group_location = document.getElementById("location");
const group_comment = document.getElementById("comment");
const btn_submit = document.getElementById("btn_submit");

btn_submit.addEventListener("click",()=>{
    if(group_name.value == ""){
        group_name.focus();
        document.getElementById("name_error").innerHTML = "<p style='color:red;'>테마 이름을 작성해 주세요</p>";
        return false;
    }
    if(group_location.value == ""){
        group_location.focus();
        document.getElementById("location_error").innerHTML = "<p style='color:red;'>주요 지역을 작성해 주세요</p>";
        return false;
    }
    if(group_comment.value == ""){
        group_comment.focus();
        document.getElementById("comment_error").innerHTML = "<p style='color:red;'>테마 소개를 작성해 주세요</p>";
        return false;
    }

    document.getElementById("group_form").submit();
 
})


group_name.oninput = function(){
    document.getElementById("name_error").innerHTML = "";
}
group_comment.oninput = function(){
    document.getElementById("comment_error").innerHTML = "";
}
group_location.oninput = function(){
    document.getElementById("location_error").innerHTML = "";
}

