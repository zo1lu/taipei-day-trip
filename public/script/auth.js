function clearPopupMessage(){
    const loginResultMessage = document.getElementById("login_result_message");
    const signupResultMessage = document.getElementById("signup_result_message");
    loginResultMessage.style.display = "none";
    signupResultMessage.style.display = "none";
}
function clearInput(){
    document.getElementById("login_email").value = "";
    document.getElementById("login_password").value = "";
    document.getElementById("signup_name").value = "";
    document.getElementById("signup_email").value = "";
    document.getElementById("signup_password").value = "";
}
function switchPopupDisplay(show){
    const popup = document.getElementById("popup")
    popup.style.display = show?"none":"block"
    clearPopupMessage();
    clearInput();
    setPopupBoxesToDefaultDisplay();
}
function setPopupBoxesToDefaultDisplay(){
    const loginBox = document.getElementById("login_box");
    const signupBox = document.getElementById("signup_box");
    signupBox.style.display = "none";
    loginBox.style.display = "block";
}
function switchPopupBox(haveAccount){
    const loginBox = document.getElementById("login_box");
    const signupBox = document.getElementById("signup_box");
    loginBox.style.display = haveAccount?"block":"none";
    signupBox.style.display = haveAccount?"none":"block";
    clearPopupMessage();
    clearInput();
}

function requestAuthenticate(token){
    return new Promise((resolve,reject)=>{
        let url = "/api/user/auth"
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

async function authenticateLogin(){
    let token = localStorage.getItem("token")
    if (token){
        let data = await requestAuthenticate(token);
        let result = data["data"];
        //let authenticated = result!==null?true:false;
        return result;
    }else{
        return false;
    }
}


export { authenticateLogin, switchPopupDisplay, switchPopupBox};