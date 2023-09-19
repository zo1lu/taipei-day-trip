class Header extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML =`
        <div class="head">
            <a class="head__title" href="/">台北一日遊</a>
            <div class="navbar">
                <a class="navbar__link">預定行程</a>
                <a class="navbar__link" id="login_btn" onclick="switchPopupDisplay(false)">登入/註冊</a>
                <a class="navbar__link link__logout" id="logout_btn" onclick="logout()">&nbsp&nbsp登出&nbsp&nbsp</a>
            </div>
        </div>`;
    };
};
customElements.define("header-component",Header)