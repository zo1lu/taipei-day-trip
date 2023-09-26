class Footer extends HTMLElement {
    constructor(){
        super();
    }
    connectedCallback() {
        this.innerHTML =`
        <p class="footer__copyright">COPYRIGHT © 2023 台北一日遊</p>`;
    };
};
customElements.define("footer-component",Footer)