function refreshPopupMessage(){
    const loginMessage = document.getElementById("login_message");
    const loginResultMessage = document.getElementById("login_result_message");
    const signupMessage = document.getElementById("signup_message");
    const signupResultMessage = document.getElementById("signup_result_message");
    loginMessage.style.display="block";
    loginResultMessage.style.display = "none";
    signupMessage.style.display="block";
    signupResultMessage.style.display = "none";

    document.getElementById("login_email").value = "";
    document.getElementById("login_password").value = "";
    document.getElementById("signup_name").value = "";
    document.getElementById("signup_email").value = "";
    document.getElementById("signup_password").value = "";
}
function switchPopupDisplay(show){
    const popup = document.getElementById("popup")
    popup.style.display = show?"none":"block"
    refreshPopupMessage()
}
function switchPopupBox(haveAccount){
    const loginBox = document.getElementById("login_box");
    const signupBox = document.getElementById("signup_box");
    loginBox.style.display = haveAccount?"block":"none";
    signupBox.style.display = haveAccount?"none":"Block";
}
function setAccountBtn(authenticated){
    const loginBtn = document.getElementById("login_btn")
    const logoutBtn = document.getElementById("logout_btn")
    loginBtn.style.display = authenticated?"none":"block"
    logoutBtn.style.display = authenticated?"block":"none"
}
function showResultMessage(member, message, alert=true){
    if (member){
        const loginMessage = document.getElementById("login_message");
        const loginResultMessage = document.getElementById("login_result_message");
        loginMessage.style.display="none";
        loginResultMessage.innerText = message;
        loginResultMessage.style.display = "block";
    }else{
        const signupMessage = document.getElementById("signup_message");
        const signupResultMessage = document.getElementById("signup_result_message");
        signupMessage.style.display="none";
        signupResultMessage.innerText = message;
        signupResultMessage.style.display = "block";
        signupResultMessage.style.color = alert?"rgb(241, 67, 67)":"rgb(35, 159, 35)";
    }
}
function checkInputNotEmpty(haveAccount){
    let message
    if(haveAccount){
        const loginEmail = document.getElementById("login_email").value;
        const loginPassword = document.getElementById("login_password").value;
        if (loginEmail == "" || loginPassword == ""){
            message = "請輸入信箱地址和密碼"
            showResultMessage(haveAccount,message)
            return false
        }
    }else{
        const signupName = document.getElementById("signup_name").value;
        const signupEmail = document.getElementById("signup_email").value;
        const signupPassword = document.getElementById("signup_password").value;
        if (signupName == "" || signupEmail == "" || signupPassword == ""){
            message = "請輸入使用者名稱、信箱地址和密碼"
            showResultMessage(haveAccount,message)
            return false
        }
    }
    return true
}
function requestCreateMember(){
    return new Promise((resolve,reject)=>{
        const url = "/api/user";
        const name = document.getElementById("signup_name").value;
        const email = document.getElementById("signup_email").value;
        const password = document.getElementById("signup_password").value;
        const body = {
            "name":name,
            "email":email,
            "password":password
        }
        const head = {
            "Content-Type":"application/json"
        }
        fetch(url, {method:"POST", body : JSON.stringify(body), headers: head})
        .then(data=>data.json())
        .then((data)=>{
            return resolve(data)
        })
        .catch(e=>{
            console.log(e)
            return reject(e)
        })
    })
}
function requestLogin(){
    return new Promise((resolve,reject)=>{
        const url = "/api/user/auth";
        const email = document.getElementById("login_email").value;
        const password = document.getElementById("login_password").value;
        const body = {
            "email":email,
            "password":password
        };
        const head = {
            "Content-Type":"application/json"
        };
        fetch(url,{method: "PUT", body: JSON.stringify(body), headers: head})
        .then(data=>data.json())
        .then(data=>{
            return resolve(data)
        })
        .catch(e=>{
            return reject(e)
        })
    })
}
function requestAuthenticate(token){
    return new Promise((resolve,reject)=>{
        url = "/api/user/auth"
        let head = {
            "Authorization":`Bearer ${token}`,
        }
        fetch(url,{ headers : head })
        .then((data)=>data.json())
        .then((data)=>{
            return resolve(data);
        })
        .catch(e=>{
            console.error(e);
            return reject(e);
        })
    })
}
async function signup(){
    if (checkInputNotEmpty(false)){
        let data = await requestCreateMember(); 
        const message = data["ok"]?"註冊成功":"註冊失敗";
        const alert = data["ok"]?false:true;
        showResultMessage(false,message,alert);
    }
}
async function login(){
    if (checkInputNotEmpty(true)){
        try{
            let data = await requestLogin();
            if(data["error"]){
                showResultMessage(true, "登入失敗");
            }else if(data["token"]){
                localStorage.setItem("token", data["token"])
                switchPopupDisplay(true)
                location.reload() 
            };
        }catch(e){
            console.log(e)
            showResultMessage(true, "登入失敗")
        }
    }
}
async function authenticateLogin(){
    let token = localStorage.getItem("token")
    if (token){
        let data = await requestAuthenticate(token);
        let result = data["data"];
        let authenticated = result!==null?true:false;
        setAccountBtn(authenticated);
    }else{
        setAccountBtn(false)
    }
}
function logout(){
    localStorage.removeItem("token");
    location.reload();
}

authenticateLogin()