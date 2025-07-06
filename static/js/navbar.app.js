(function () {

    Vue.createApp({
        setup() {
            let userProfile = Vue.ref({});

            async function loadUserProfile() {
                let resp = await fetch("/apis/user.profile.aspx");
                let data = await resp.json();
                if (data.code) {
                    console.error("Failed to load user profile", data);
                    return;
                }

                console.log(data);
                Object.assign(userProfile.value, data.result);
                console.log(userProfile.value.userid, data.result);
            }

            Vue.onMounted(async () => {
                await loadUserProfile();
            });
            return { userProfile };
        }
    }).mount("#navbar");

})();