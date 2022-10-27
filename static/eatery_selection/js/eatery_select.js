const card = document.querySelectorAll(".card");
const result_eatery = document.getElementById("result-eatery");
const modal_detail_btn = document.getElementById("modal-detail-btn");


function selectCard(card){
    let selectedCard = card.parentNode;
    selectedCard.classList.toggle("flip");

    setTimeout(function(){
        $("#result_modal").modal("show");

        modal_detail_btn.href = card.parentNode.getAttribute("data-url");

        result_eatery.innerHTML = `<img src="${card.parentNode.getAttribute("data-eatery-image")}" style="width:200px;height:200px;">
        <p class="mt-3">오늘은 <strong>${card.parentNode.getAttribute("data-eatery-name")}</strong> 어떠세요?</p>
        <p>이 식당이 궁금하시다면 <span style="color:rgb(232,122,68)">자세히 보러가기</span>를 클릭해 주세요!</p>`;

    },1300)
}

