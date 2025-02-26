document.addEventListener("DOMContentLoaded", () =>{
    document.getElementById("query-btn").addEventListener("click", async()=>{
        const username = document.getElementById("query-username").value;
        const response = await fetch(`/api/member?username=${username}`)
        const resultDiv = document.getElementById("query-result");
        
        if (!username) {
            resultDiv.innerHTML = "請輸入帳號";
            resultDiv.style.color = "red";
            return;
        }
        
        const data = await response.json();

        if (data.data){
            resultDiv.innerHTML=`姓名: ${data.data.name}, 帳號: ${data.data.username}`;
        }else{
            resultDiv.innerHTML="No Data";
        }
    });
    document.getElementById("update-btn").addEventListener("click", async () => {
        const newName = document.getElementById("new-name").value;
        const updateResult = document.getElementById("update-result");

        if (!newName) {
            updateResult.innerHTML = "姓名不能為空";
            updateResult.style.color = "red";
            return;
        }

        const response = await fetch("/api/member", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newName })
        });

        const data = await response.json();
        
        if (data.ok) {
            updateResult.innerHTML = "Updated";
            updateResult.style.color ="green";
            document.getElementById("welcome-name").innerText = newName; // 更新頁面上的會員名稱
        } else {
            updateResult.innerHTML = "Failed to update";
            updateResult.style.color ="red";
        }
    });
});