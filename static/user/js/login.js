window.onload = function(){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const btn_login = document.getElementById("btn_login");
    const userid = document.getElementById("userid");
    const password = document.getElementById("password");

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
            if(result.success == false){
                alert("로그인 에러")
            }else{
                if(result.check == "fail"){
                    document.getElementById("login_error").innerHTML = "<p style='color:red'>아이디 혹은 비밀번호가 틀립니다.</p>";
                }else{
                    location.href = "/"
                }
            }

        }catch(error){
            alert(error)
        }
    })

    function validation(){

        if(userid.value == ""){
            userid.focus();
            document.getElementById("userid_error").innerHTML = "<p style='color:red'>아이디를 입력해 주세요</p>";
            return false;
        }
        if(password.value == ""){
            password.focus();
            document.getElementById("password_error").innerHTML = "<p style='color:red'>비밀번호를 입력해 주세요</p>";
            return false;
        }
    }

    userid.oninput = function(){
        document.getElementById("userid_error").innerHTML = "";
        document.getElementById("login_error").innerHTML = "";
    }
    password.oninput = function(){
        document.getElementById("password_error").innerHTML = "";
        document.getElementById("login_error").innerHTML = "";
    }

}