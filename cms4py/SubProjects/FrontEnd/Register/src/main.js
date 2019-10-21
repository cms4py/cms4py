new Vue({
    el: "#vueapp",

    created() {
        this.language_password_confirm_not_match = $(".languages .password_confirm_not_match").html();
        this.language_password_confirm_matched = $(".languages .password_confirm_matched").html();
        this.language_checking_login_name = $(".languages .checking_login_name").html();
    },

    data() {
        return {
            password: "",
            passwordConfirm: "",
            password_confirm_alert_msg: "",
            allFieldsVerified: false,
            login_name: "",
            login_name_alert_msg: "",
        }
    },

    methods: {
        formSubmitHandler(e) {

        },

        checkToChangeAllFieldsVerifiedValue() {
            //TODO
        },

        verifyPassword() {
            if (this.password != this.passwordConfirm) {
                this.password_confirm_alert_msg = `<div class="text-danger">${this.language_password_confirm_not_match}</div>`;
            } else {
                this.password_confirm_alert_msg = `<div class="text-success">${this.language_password_confirm_matched}</div>`;
                this.checkToChangeAllFieldsVerifiedValue();
            }
        },

        loginNameFocusoutHandler(e) {
            if (this.login_name) {
                this.login_name_alert_msg = `
<div class="text-info">
    <div class="spinner-border spinner-border-sm" role="status">
        <span class="sr-only">Loading...</span>
    </div>
    ${this.language_checking_login_name}
</div>`;
            }
        }
    },

    watch: {
        password(val) {
            this.verifyPassword();
        },

        passwordConfirm(val) {
            this.verifyPassword();
        }
    }
});