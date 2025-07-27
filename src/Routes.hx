/*
 * MIT License
 *
 * Copyright (c) 2025 https://yunp.top
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
 * Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
 * AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
 * THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

package;

import com.example.myapp.apis.user.Logout;
import com.example.myapp.apis.user.Profile;
import com.example.myapp.apis.user.SignIn;
import com.example.myapp.apis.user.SignUp;
import com.example.myapp.pages.About;
import com.example.myapp.pages.Articles;
import com.example.myapp.pages.Index;
import com.example.myapp.pages.ResetPassword;
import com.example.myapp.pages.Sign;
import top.yunp.cms4py.framework.web.routing.apis.API;
import top.yunp.cms4py.framework.web.routing.CRoute;

class Routes {
    public static function configRoutes():Array<CRoute> {
        var apis = new API();
        apis.addAction("user.profile.aspx", new Profile());
        apis.addAction("user.logout.aspx", new Logout());
        apis.addAction("user.signup.aspx", new SignUp());
        apis.addAction("user.signin.aspx", new SignIn());

        return [
            new CRoute("/", new Index()),
            new CRoute("/about", new About()),
            new CRoute("/articles", new Articles()),
            new CRoute("/sign", new Sign()),
            new CRoute("/profile", new com.example.myapp.pages.Profile()),
            new CRoute("/reset-password", new ResetPassword()),
            new CRoute("/apis/{action}", apis, ["GET", "POST"])
        ];
    }
}
