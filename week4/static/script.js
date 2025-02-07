document.addEventListener("DOMContentLoaded",function(){
    const form = document.getElementById("signin-form");

    form.addEventListener("submit",function(event){
        const checkbox = document.getElementById("agree");

        if(!checkbox.checked){
            alert("Please check the checkbox first");
            event.preventDefault();
        }
    });

    document.getElementById("calculate-btn").addEventListener("click", function() {
        calculateSquare();
    });
});

//計算平方
function calculateSquare() {
    const inputElement = document.getElementById("number-input");
    const input = inputElement.value.trim(); // 取得輸入值並去掉前後空格

    // 檢查輸入是否為正整數
    const number = Number(input);
    if (!input || isNaN(number) || number <= 0 || !Number.isInteger(number)) {
        alert("請輸入正整數");
        return;
    }

    // 轉跳到平方計算結果頁面
    window.location.href = `/square/${number}`;
}