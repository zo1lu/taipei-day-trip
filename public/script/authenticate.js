import { switchPopupDisplay, authenticateLogin, switchPopupBox } from "./auth.js"
function setAccountBtn(authenticated){
    const loginBtn = document.getElementById("login_btn")
    const logoutBtn = document.getElementById("logout_btn")
    loginBtn.style.display = authenticated?"none":"block"
    logoutBtn.style.display = authenticated?"block":"none"
}
function showResultMessage(member, message, alert=true){
    if(member){
        const loginResultMessage = document.getElementById("login_result_message");
        loginResultMessage.innerText = message;
        loginResultMessage.style.display = "block";
    }else{
        const signupResultMessage = document.getElementById("signup_result_message");
        signupResultMessage.innerText = message;
        signupResultMessage.style.color = alert?"rgb(241, 67, 67)":"rgb(35, 159, 35)";
        signupResultMessage.style.display = "block";
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

async function setLoginBtn(){
    let authenticated = await authenticateLogin();
    setAccountBtn(authenticated);
}

async function checkLoginForBooking(){
    let authenticated = await authenticateLogin();
    if (authenticated){
        window.location.href = "/booking"
    }else{
        switchPopupDisplay(false);
    }
}

function logout(){
    localStorage.removeItem("token");
    location.reload();
}

window.signup = signup
window.logout = logout
window.login = login
window.checkLoginForBooking = checkLoginForBooking
window.switchPopupDisplay = switchPopupDisplay
window.switchPopupBox = switchPopupBox
setLoginBtn()
