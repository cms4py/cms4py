const ServerConfig = {
    ACTION_BASE_URL: `/rest/action`,
    ACTIONS: {
        REGISTER_USER_EXISTS: "register.user_exists",
    },

    makeActionURL(actionName) {
        return `${ServerConfig.ACTION_BASE_URL}/${actionName}`;
    },

    do_action(action, args, successCallback, failCallback) {
        $.post(ServerConfig.makeActionURL(action), args).done(function (result) {
            if (typeof result == 'string') {
                try {
                    result = JSON.parse(result);
                } catch (e) {
                }
            }
            console.log(result);
            successCallback(result);
        }).fail(failCallback);
    }
};

export default ServerConfig;