package com.example.myapp.pages.validators;
import top.yunp.cms4py.framework.web.http.Context;
import com.example.myapp.pages.exceptions.RequireLogin;
class UserValidators {
    public function new() {
    }

    public static function checkLoginStatus(context:Context) {
        if (context.session.userid == null || context.session.userid == "") {
            throw new RequireLogin();
        }
    }
}
