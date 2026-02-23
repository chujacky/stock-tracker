(() => {
    window.addEventListener("load", (event) => {
        const form = document.querySelector("form");
        const ticker = document.querySelector("input[name='ticker']");
        const category = document.querySelector("select[name='category']");
        const new_category = document.querySelector("input[name='new-category']");

        category.addEventListener("change", (e) => {
            new_category.required = false;

            if (category.value == "Other") {
                new_category.required = true;
            }
        })

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            ticker.value = ticker.value.toUpperCase();
            e.currentTarget.submit()
        })
    });
})()