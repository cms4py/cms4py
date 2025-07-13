package com.example.myapp.apis.exceptions;
import top.yunp.cms4py.framework.web.exceptions.APIException;
import top.yunp.cms4py.framework.web.routing.apis.actions.Action;
class ParametersError extends APIException {
    public function new() {
        super(Action.createResult(ResultCode.CODE_PARAMETERS_ERROR, "Parameters error"));
    }
}
