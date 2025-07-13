package com.example.myapp.pages.exceptions;
import top.yunp.cms4py.framework.web.exceptions.PageException;
import externals.starlette.responses.RedirectResponse;
class RequireLogin extends PageException {
    public function new() {
        super(new RedirectResponse("/sign"));
    }
}
