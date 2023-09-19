class Popup extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML =`
            <div class="login__box" id="login_box">
                <div class="popup__deco"></div>
                <button class="popup__close" onclick="switchPopupDisplay(true)"><img src="/icon/icon-close.png"/></button>
                <p class="popup__title">登入會員帳號</p>
                <div class="popup__wrapper">    
                    <input type="email" name="email" class="popup__input" placeholder="輸入電子郵件" id="login_email" required/>
                    <input type="password" name="password" class="popup__input" placeholder="輸入密碼" id="login_password" required/>  
                    <button class="popup__submit" onclick="login()">登入帳號</button>
                    <p class="popup__message" id="login_message">還沒有帳戶?<span class="popup__link" onclick="switchPopupBox(false)"> 點此前往</span></p>
                    <p class="popup__result-message" id="login_result_message"></p>
                </div>    
            </div>
            <div class="signup__box" id="signup_box">
                <div class="popup__deco"></div>
                <button class="popup__close" onclick="switchPopupDisplay(true)"><img src="/icon/icon-close.png"/></button>
                <p class="popup__title">註冊會員帳號</p> 
                <div class="popup__wrapper">  
                    <input type="text" name="username" class="popup__input" placeholder="輸入姓名" id="signup_name" required/>
                    <input type="email" name="email" class="popup__input" placeholder="輸入電子郵件" id="signup_email" required/>
                    <input type="password" name="password" class="popup__input" placeholder="輸入密碼" id="signup_password" required/>  
                    <button class="popup__submit" onclick="signup()">註冊新帳號</button>
                    <p class="popup__message" id="signup_message">已經有帳戶了?<span class="popup__link" onclick="switchPopupBox(true)"> 點此登入</span></p>
                    <p class="popup__result-message" id="signup_result_message"></p> 
                </div>     
            </div>`;
    };
};
customElements.define("popup-component",Popup)