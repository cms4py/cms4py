import ServerConfig from "../../commons/ServerConfig";
import Dialog from "../../commons/Dialog";

new Vue({
    el: "#vueapp",

    created() {
    },

    data() {
        return {
            language_password_confirm_not_match: $(".languages .password_confirm_not_match").html(),
            language_password_confirm_matched: $(".languages .password_confirm_matched").html(),
            language_checking_login_name: $(".languages .checking_login_name").html(),
            language_login_name_exists: $(".languages .login_name_exists").html(),
            language_checking_email: $(".languages .checking_email").html(),
            language_email_exists: $(".languages .email_exists").html(),
            language_checking_phone: $(".languages .checking_phone").html(),
            language_phone_exists: $(".languages .phone_exists").html(),

            password: "",
            passwordConfirm: "",
            password_confirm_alert_msg: "",
            allFieldsVerified: false,
            login_name: "",
            login_name_ok: false,
            login_name_alert_msg: "",
            email: "",
            email_ok: false,
            email_alert_msg: "",
            phone: "",
            phone_ok: false,
            phone_alert_msg: ""
        }
    },

    methods: {
        formSubmitHandler(e) {

        },

        checkToChangeAllFieldsVerifiedValue() {
            this.allFieldsVerified = this.password == this.passwordConfirm && this.login_name_ok && this.email_ok && this.phone_ok;
        },

        verifyPassword() {
            if (this.password != this.passwordConfirm) {
                this.password_confirm_alert_msg = `<div class="text-danger">${this.language_password_confirm_not_match}</div>`;
            } else {
                this.password_confirm_alert_msg = `<div class="text-success">${this.language_password_confirm_matched}</div>`;
            }
            this.checkToChangeAllFieldsVerifiedValue();
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

        makeLoadingMessageHTMLString(msg) {
            return `
<div class="text-info">
    <div class="spinner-border spinner-border-sm" role="status">
        <span class="sr-only">Loading...</span>
    </div>
    ${msg}
</div>`;
        },

        asyncCheckFieldExists(field_name, field_value) {
            if (this[field_name]) {
                this[field_name + "_alert_msg"] = this.makeLoadingMessageHTMLString(this["language_checking_" + field_name]);

                var params = {};
                params.field_name = field_name;
                params[field_name] = field_value;

                ServerConfig.do_action(ServerConfig.ACTIONS.REGISTER_USER_EXISTS, params, function (result) {
                    if (result && result.code == 0) {
                        if (result.exists) {
                            this[field_name + "_alert_msg"] = this.makeErrorMessageHTMLString(this["language_" + field_name + "_exists"]);
                            this[field_name + "_ok"] = false;
                        } else {
                            this[field_name + "_ok"] = true;
                            this[field_name + "_alert_msg"] = this.makeOKMessageHTMLString();
                        }

                        this.checkToChangeAllFieldsVerifiedValue();
                    } else {
                        Dialog.showMessageDialog("数据错误，请稍后重试。");
                    }
                }.bind(this), function () {
                    Dialog.showMessageDialog("连接服务器失败，请稍后重试。");
                });
            }
        },

        loginNameChangeHandler(e) {
            this.asyncCheckFieldExists("login_name", this.login_name);
        },

        emailChangeHandler(e) {
            this.asyncCheckFieldExists("email", this.email);
        },


        phoneChangeHandler(e) {
            this.asyncCheckFieldExists("phone", this.phone);
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