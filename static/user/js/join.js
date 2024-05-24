
const btn_join = document.getElementById("btn_join");
const userid = document.getElementById("userid");
const password = document.getElementById("password");
const re_password = document.getElementById("re_password");
const btn_userid = document.getElementById("btn_userid");
const join_error = document.getElementById("join-error")
let chk_userid = false;

// 회원가입
btn_join.addEventListener("click", async()=>{
    try{
        const data = new FormData(document.getElementById("join_form"));
        if(!validation()){
            return false;
        }
        if(!confirm("가입 하시겠습니까?")){
            return false;
        }
        const response = await fetch('',{
            method:"POST",
            headers:{'X-CSRFToken': csrftoken},
            body:data
        })
        const result = await response.json();
        if(response.status == 400){
            alert(result.message);
        }else{
            alert("가입 되었습니다 😄");
            location.href = "/";
        }
        
    }catch(error){
        alert("로그인 실패.. 관리자에게 문의해주세요.");
    }

})

// 아이디 중복검사
btn_userid.addEventListener("click", async()=>{
    if(userid.value == ""){
        userid.focus();
        join_error.innerHTML = "아이디를 입력해 주세요";
        join_error.style.color = "red";
        userid.classList.add("is-invalid");
        return false;
    }if(userid.value.length < 5){
        userid.focus();
        join_error.innerHTML = "아이디는 5글자 이상입니다";
        join_error.style.color = "red";
        userid.classList.add("is-invalid");
        return false;
    }

    try{
        btn_userid.disabled = true;
        const response = await fetch('/duple/',{
            method:"POST",
            headers:{'X-CSRFToken': csrftoken},
            body:JSON.stringify({userid:userid.value,})
        });
        
        const result = await response.json();
        if(result.exist){
            join_error.innerHTML = "중복된 아이디 입니다.";
            join_error.style.color = "red";
            userid.classList.add("is-invalid");
            btn_userid.disabled = false;
            
        }else{
            userid.classList.add("is-valid");
            userid.classList.remove("is-invalid");
            join_error.innerHTML = "사용 가능한 아이디 입니다.";
            join_error.style.color = "green";
            chk_userid = true;
            btn_userid.disabled = false;
        }
        
    }catch(error){
        alert(error);
        btn_userid.disabled = false;
    }

})

// 유효성 검사
function validation(){
    if(userid.value == ""){
        userid.focus();
        join_error.innerHTML = "아이디를 입력해 주세요";
        join_error.style.color = "red";
        userid.classList.add("is-invalid");
        return false;
    }
    if(userid.value.length < 5){
        userid.focus();
        join_error.innerHTML = "아이디는 5글자 이상입니다";
        join_error.style.color = "red";
        userid.classList.add("is-invalid");
        return false;
    }
    if(chk_userid == false){
        userid.focus();
        join_error.innerHTML = "아이디 중복검사를 해주세요.";
        join_error.style.color = "red";
        userid.classList.add("is-invalid");
        return false;
    }
    if(password.value == ""){
        password.focus();
        join_error.innerHTML = "비밀번호를 입력해주세요.";
        join_error.style.color = "red";
        password.classList.add("is-invalid");
        return false;
    }
    if(password.value.length < 5){
        password.focus();
        join_error.innerHTML = "비밀번호는 5글자 이상입니다.";
        join_error.style.color = "red";
        password.classList.add("is-invalid");
        return false;
    }
    if(re_password.value == ""){
        re_password.focus();
        join_error.innerHTML = "비밀번호 확인을 입력해주세요.";
        join_error.style.color = "red";
        re_password.classList.add("is-invalid");
        return false;
    }
    if(password.value != re_password.value){
        re_password.focus();
        join_error.innerHTML = "비밀번호가 다릅니다.";
        join_error.style.color = "red";
        re_password.classList.add("is-invalid");
        return false;
    }

    return true;
}

userid.oninput = function(){
    join_error.innerHTML = "모든 항목을 입력해주세요.";
    join_error.style.color = "black";
    userid.classList.remove("is-invalid");
    userid.classList.remove("is-valid");
    chk_userid = false;
}
password.oninput = function(){
    join_error.innerHTML = "모든 항목을 입력해주세요.";
    join_error.style.color = "black";
    password.classList.remove("is-invalid");
}
re_password.oninput = function(){
    join_error.innerHTML = "모든 항목을 입력해주세요.";
    join_error.style.color = "black";
    re_password.classList.remove("is-invalid");
}
