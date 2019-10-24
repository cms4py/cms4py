/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./cms4py/SubProjects/FrontEnd/Register/src/main.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./cms4py/SubProjects/FrontEnd/Register/src/main.js":
/*!**********************************************************!*\
  !*** ./cms4py/SubProjects/FrontEnd/Register/src/main.js ***!
  \**********************************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _commons_ServerConfig__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../commons/ServerConfig */ \"./cms4py/SubProjects/FrontEnd/commons/ServerConfig.js\");\n/* harmony import */ var _commons_Dialog__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../commons/Dialog */ \"./cms4py/SubProjects/FrontEnd/commons/Dialog.js\");\n\n\n\nnew Vue({\n    el: \"#vueapp\",\n\n    created() {\n    },\n\n    data() {\n        return {\n            language_password_confirm_not_match: $(\".languages .password_confirm_not_match\").html(),\n            language_password_confirm_matched: $(\".languages .password_confirm_matched\").html(),\n            language_checking_login_name: $(\".languages .checking_login_name\").html(),\n            language_login_name_exists: $(\".languages .login_name_exists\").html(),\n            language_checking_email: $(\".languages .checking_email\").html(),\n            language_email_exists: $(\".languages .email_exists\").html(),\n            language_checking_phone: $(\".languages .checking_phone\").html(),\n            language_phone_exists: $(\".languages .phone_exists\").html(),\n\n            password: \"\",\n            passwordConfirm: \"\",\n            password_confirm_alert_msg: \"\",\n            allFieldsVerified: false,\n            login_name: \"\",\n            login_name_ok: false,\n            login_name_alert_msg: \"\",\n            email: \"\",\n            email_ok: false,\n            email_alert_msg: \"\",\n            phone: \"\",\n            phone_ok: false,\n            phone_alert_msg: \"\"\n        }\n    },\n\n    methods: {\n        formSubmitHandler(e) {\n\n        },\n\n        checkToChangeAllFieldsVerifiedValue() {\n            this.allFieldsVerified = this.password == this.passwordConfirm && this.login_name_ok && this.email_ok && this.phone_ok;\n        },\n\n        verifyPassword() {\n            if (this.password != this.passwordConfirm) {\n                this.password_confirm_alert_msg = `<div class=\"text-danger\">${this.language_password_confirm_not_match}</div>`;\n            } else {\n                this.password_confirm_alert_msg = `<div class=\"text-success\">${this.language_password_confirm_matched}</div>`;\n            }\n            this.checkToChangeAllFieldsVerifiedValue();\n        },\n\n        makeErrorMessageHTMLString(msg) {\n            return `<div class=\"text-danger\">\n    <span class=\"fa fa-times\"></span>\n    ${msg}\n</div>`\n        },\n\n        makeOKMessageHTMLString() {\n            return `<div class=\"text-success\">\n    <span class=\"fa fa-check\"></span>\n</div>`\n        },\n\n        makeLoadingMessageHTMLString(msg) {\n            return `\n<div class=\"text-info\">\n    <div class=\"spinner-border spinner-border-sm\" role=\"status\">\n        <span class=\"sr-only\">Loading...</span>\n    </div>\n    ${msg}\n</div>`;\n        },\n\n        asyncCheckFieldExists(field_name, field_value) {\n            if (this[field_name]) {\n                this[field_name + \"_alert_msg\"] = this.makeLoadingMessageHTMLString(this[\"language_checking_\" + field_name]);\n\n                var params = {};\n                params.field_name = field_name;\n                params[field_name] = field_value;\n\n                _commons_ServerConfig__WEBPACK_IMPORTED_MODULE_0__[\"default\"].do_action(_commons_ServerConfig__WEBPACK_IMPORTED_MODULE_0__[\"default\"].ACTIONS.REGISTER_USER_EXISTS, params, function (result) {\n                    if (result && result.code == 0) {\n                        if (result.exists) {\n                            this[field_name + \"_alert_msg\"] = this.makeErrorMessageHTMLString(this[\"language_\" + field_name + \"_exists\"]);\n                            this[field_name + \"_ok\"] = false;\n                        } else {\n                            this[field_name + \"_ok\"] = true;\n                            this[field_name + \"_alert_msg\"] = this.makeOKMessageHTMLString();\n                        }\n\n                        this.checkToChangeAllFieldsVerifiedValue();\n                    } else {\n                        _commons_Dialog__WEBPACK_IMPORTED_MODULE_1__[\"default\"].showMessageDialog(\"数据错误，请稍后重试。\");\n                    }\n                }.bind(this), function () {\n                    _commons_Dialog__WEBPACK_IMPORTED_MODULE_1__[\"default\"].showMessageDialog(\"连接服务器失败，请稍后重试。\");\n                });\n            }\n        },\n\n        loginNameChangeHandler(e) {\n            this.asyncCheckFieldExists(\"login_name\", this.login_name);\n        },\n\n        emailChangeHandler(e) {\n            this.asyncCheckFieldExists(\"email\", this.email);\n        },\n\n\n        phoneChangeHandler(e) {\n            this.asyncCheckFieldExists(\"phone\", this.phone);\n        }\n    },\n\n    watch: {\n        password(val) {\n            this.verifyPassword();\n        },\n\n        passwordConfirm(val) {\n            this.verifyPassword();\n        }\n    }\n});\n\n//# sourceURL=webpack:///./cms4py/SubProjects/FrontEnd/Register/src/main.js?");

/***/ }),

/***/ "./cms4py/SubProjects/FrontEnd/commons/Dialog.js":
/*!*******************************************************!*\
  !*** ./cms4py/SubProjects/FrontEnd/commons/Dialog.js ***!
  \*******************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\nconst Dialog = {\n    showLoading(msg) {\n        return $(`<div class=\"modal\" tabindex=\"-1\" role=\"dialog\">\n  <div class=\"modal-dialog\" role=\"document\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <div class=\"spinner-border\" role=\"status\">\n          <span class=\"sr-only\">Loading...</span>\n        </div>\n      </div>\n      <div class=\"modal-body\">\n        <p>${msg}</p>\n      </div>\n    </div>\n  </div>\n</div>`).modal({\n            keyboard: false,\n            backdrop: \"static\",\n        }).appendTo(document.body).on(\"hide.bs.modal\", function (e) {\n            $(this).remove();\n        });\n    },\n\n    showMessageDialog(msg, title = \"\", closeCallback) {\n        return $(`<div class=\"modal fade\" tabindex=\"-1\" role=\"dialog\">\n  <div class=\"modal-dialog\" role=\"document\">\n    <div class=\"modal-content\">\n      <div class=\"modal-header\">\n        <h5 class=\"modal-title\">${title}</h5>\n        <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n          <span aria-hidden=\"true\">&times;</span>\n        </button>\n      </div>\n      <div class=\"modal-body\">\n        ${msg}\n      </div>\n      <div class=\"modal-footer\">\n        <button type=\"button\" class=\"btn btn-danger\" data-dismiss=\"modal\">OK</button>\n      </div>\n    </div>\n  </div>\n</div>`).modal({\n            keyboard: true,\n            backdrop: true,\n        }).appendTo(document.body).on(\"hide.bs.modal\", function (e) {\n            $(this).remove();\n            if (closeCallback) {\n                closeCallback();\n            }\n        });\n    }\n};\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (Dialog);\n\n//# sourceURL=webpack:///./cms4py/SubProjects/FrontEnd/commons/Dialog.js?");

/***/ }),

/***/ "./cms4py/SubProjects/FrontEnd/commons/ServerConfig.js":
/*!*************************************************************!*\
  !*** ./cms4py/SubProjects/FrontEnd/commons/ServerConfig.js ***!
  \*************************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\nconst ServerConfig = {\n    ACTION_BASE_URL: `/rest/action`,\n    ACTIONS: {\n        REGISTER_USER_EXISTS: \"register.user_exists\",\n    },\n\n    makeActionURL(actionName) {\n        return `${ServerConfig.ACTION_BASE_URL}/${actionName}`;\n    },\n\n    do_action(action, args, successCallback, failCallback) {\n        $.post(ServerConfig.makeActionURL(action), args).done(function (result) {\n            if (typeof result == 'string') {\n                try {\n                    result = JSON.parse(result);\n                } catch (e) {\n                }\n            }\n            console.log(result);\n            successCallback(result);\n        }).fail(failCallback);\n    }\n};\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (ServerConfig);\n\n//# sourceURL=webpack:///./cms4py/SubProjects/FrontEnd/commons/ServerConfig.js?");

/***/ })

/******/ });