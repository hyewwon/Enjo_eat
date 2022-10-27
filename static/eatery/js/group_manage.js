const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

async function deleteGroup(pk){
    if(!confirm('테마를 삭제할까요?')){
        return false;
    }
    try{
        const response = await fetch('',{
            method:"DELETE",
            headers:{'X-CSRFToken': csrftoken},
            body:JSON.stringify({group_pk:pk})
        })
        const result = await response.json();
        if(result.success == false){
            alert("삭제 에러");
        }else{
            location.reload();
        }
    }catch(error){
        alert(error);
    }
}


