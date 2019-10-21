import ServerConfig from "../../commons/ServerConfig";
import Dialog from "../../commons/Dialog";

new Vue({
    el: "#vueapp",

    created() {
        this.language_password_confirm_not_match = $(".languages .password_confirm_not_match").html();
        this.language_password_confirm_matched = $(".languages .password_confirm_matched").html();
        this.language_checking_login_name = $(".languages .checking_login_name").html();
        this.language_login_name_exists = $(".languages .login_name_exists").html();
    },

    data() {
        return {
            password: "",
            passwordConfirm: "",
            password_confirm_alert_msg: "",
            allFieldsVerified: false,
            login_name: "",
            login_name_ok: false,
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

        makeErrorMessageHTMLString(msg) {
            return `<div class="text-danger">
    <span class="fa fa-times"></span>
    ${msg}
</div>`
        },

        makeOKMessageHTMLString() {
            return `<div class="text-success">
    <span class="fa fa-check"></span>
</div>`
        },

        loginNameChangeHandler(e) {
            if (this.login_name) {
                this.login_name_alert_msg = `
<div class="text-info">
    <div class="spinner-border spinner-border-sm" role="status">
        <span class="sr-only">Loading...</span>
    </div>
    ${this.language_checking_login_name}
</div>`;

                ServerConfig.do_action(ServerConfig.ACTIONS.REGISTER_USER_EXISTS, {
                    field_name: "login_name",
                    login_name: this.login_name
                }, function (result) {
                    if (result && result.code == 0) {
                        if (result.exists) {
                            this.login_name_alert_msg = this.makeErrorMessageHTMLString(this.language_login_name_exists);
                            this.login_name_ok = false;
                        } else {
                            this.login_name_ok = true;
                            this.login_name_alert_msg = this.makeOKMessageHTMLString();
                        }
                    } else {
                        Dialog.showMessageDialog("数据错误，请稍后重试。");
                    }
                }.bind(this), function () {
                    Dialog.showMessageDialog("连接服务器失败，请稍后重试。");
                });
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