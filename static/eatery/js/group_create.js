const group_name = document.getElementById("name");
const group_location = document.getElementById("location");
const group_comment = document.getElementById("comment");
const create_error = document.getElementById("create-error");
const btn_submit = document.getElementById("btn_submit");
const open = document.getElementById("open");

btn_submit.addEventListener("click", async()=>{

    if(group_name.value == ""){
        group_name.focus();
        create_error.innerText = "테마 이름을 작성해 주세요";
        create_error.style.color = "red";
        group_name.classList.add("is-invalid")
        return false;
    }
    if(group_location.value == ""){
        group_location.focus();
        create_error.innerText = "주요 지역을 작성해 주세요";
        create_error.style.color = "red";
        group_location.classList.add("is-invalid")
        return false;
    }
    if(group_comment.value == ""){
        group_comment.focus();
        create_error.innerText = "테마 소개를 작성해 주세요";
        create_error.style.color = "red";
        group_comment.classList.add("is-invalid")
        return false;
    }

    try{
        const data = new FormData(document.getElementById("group_form"));
        const response = await fetch('',{
            method:"POST",
            headers:{'X-CSRFToken': csrftoken},
            body:JSON.stringify({
                "group_name" : group_name.value,
                "group_location" : group_location.value,
                "group_comment" : group_comment.value,
                "open_flag" : open.checked ? 1 : 0
            })
        })
        const result = await response.json();
        if(response.status == 400){
            alert(response.message)
        }else{
            location.href = result.url
        }
        
    }catch(error){
        alert("로그인 실패.. 관리자에게 문의해주세요.");
    }
 
})


group_name.oninput = function(){
    create_error.innerText = "사용자들이 알기 쉽게 테마를 소개해주세요.";
    create_error.style.color = "gray";
    group_name.classList.remove("is-invalid")
}
group_comment.oninput = function(){
    create_error.innerText = "사용자들이 알기 쉽게 테마를 소개해주세요.";
    create_error.style.color = "gray";
    group_name.classList.remove("is-invalid")
    
}
group_location.oninput = function(){
    create_error.innerText = "사용자들이 알기 쉽게 테마를 소개해주세요.";
    create_error.style.color = "gray";
    group_name.classList.remove("is-invalid")

}

