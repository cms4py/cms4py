const ServerConfig = {
    ACTION_BASE_URL: `/rest/action`,
    ACTIONS: {
        REGISTER_USER_EXISTS: "register.user_exists",
    },

    makeActionURL(actionName) {
        return `${ServerConfig.ACTION_BASE_URL}/${actionName}`;
    }
};

export default ServerConfig;