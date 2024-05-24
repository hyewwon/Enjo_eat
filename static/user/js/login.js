const btn_login = document.getElementById("btn_login");
const userid = document.getElementById("userid");
const password = document.getElementById("password");
const login_error = document.getElementById("login-error")

btn_login.addEventListener("click", async()=>{
    try{
        const data = new FormData(document.getElementById("login_form"));
        if(validation() == false){
            return false;
        }
        const response = await fetch('',{
            method:"POST",
            headers:{'X-CSRFToken': csrftoken},
            body:data
        })
        const result = await response.json();
        if(response.status == 400){
            login_error.innerHTML = "아이디 혹은 비밀번호가 다릅니다.";
            login_error.style.color = "red";
            userid.classList.add("is-invalid");
            password.classList.add("is-invalid");
        }else{
            const urlSearch = new URLSearchParams(location.search);
            const next_url = urlSearch.get("next")
            location.href = !next_url ? "/" : next_url

        }
        
    }catch(error){
        alert("로그인 실패.. 관리자에게 문의해주세요.");
    }
})

function validation(){
    if(userid.value == ""){
        userid.focus();
        login_error.innerHTML = "아이디를 입력해 주세요";
        login_error.style.color = "red";
        userid.classList.add("is-invalid");
        return false;
    }
    if(password.value == ""){
        password.focus();
        login_error.innerHTML = "비밀번호를 입력해 주세요";
        login_error.style.color = "red";
        password.classList.add("is-invalid");
        return false;
    }
}

userid.oninput = function(){
    login_error.innerHTML = "아이디와 비밀번호를 입력해 주세요.";
    login_error.style.color = "black";
    userid.classList.remove("is-invalid");
    
}
password.oninput = function(){
    login_error.innerHTML = "아이디와 비밀번호를 입력해 주세요.";
    login_error.style.color = "black";
    password.classList.remove("is-invalid");
}

