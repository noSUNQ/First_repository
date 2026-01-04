window.addEventListener("DOMContentLoaded", () => {
    const tg = window.Telegram.WebApp;

    document.getElementById('btn_login').addEventListener("click", () => {
        const init_data = tg.init_data;

        fetch ("/home" , {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(init_data)
        })
    });
}); 