/* =========================================================
   CAREERAI THEME ENGINE
   ========================================================= */

(function () {

    const THEME_KEY = "careerai-theme";

    const DEFAULT_THEME = "midnight";

    const VALID_THEMES = [
        "midnight",
        "light",
        "ocean",
        "emerald",
        "sunset",
        "rose"
    ];


    /* -----------------------------------------------------
       Apply Theme
       ----------------------------------------------------- */

    function applyTheme(theme) {

        if (!VALID_THEMES.includes(theme)) {
            theme = DEFAULT_THEME;
        }

        document.documentElement.setAttribute(
            "data-theme",
            theme
        );

        if (document.body) {
            document.body.setAttribute(
                "data-theme",
                theme
            );
        }

        localStorage.setItem(
            THEME_KEY,
            theme
        );

        window.dispatchEvent(
            new CustomEvent("careerai-theme-change", {
                detail: {
                    theme: theme
                }
            })
        );
    }


    /* -----------------------------------------------------
       Get Current Theme
       ----------------------------------------------------- */

    function getTheme() {

        const savedTheme = localStorage.getItem(THEME_KEY);

        if (VALID_THEMES.includes(savedTheme)) {
            return savedTheme;
        }

        return DEFAULT_THEME;
    }


    /* -----------------------------------------------------
       Initialize Theme
       ----------------------------------------------------- */

    function initializeTheme() {

        const theme = getTheme();

        document.documentElement.setAttribute(
            "data-theme",
            theme
        );

        if (document.body) {
            document.body.setAttribute(
                "data-theme",
                theme
            );
        }
    }


    /* -----------------------------------------------------
       Theme Picker
       ----------------------------------------------------- */

    function initializeThemePicker() {

        const toggle = document.querySelector(
            "[data-theme-toggle]"
        );

        const menu = document.querySelector(
            "[data-theme-menu]"
        );

        const options = document.querySelectorAll(
            "[data-theme-option]"
        );


        /* Theme picker does not exist on this page */

        if (!toggle || !menu || !options.length) {
            return;
        }


        /* -------------------------------------------------
           Update Selected Theme
           ------------------------------------------------- */

        function updateSelectedTheme() {

            const currentTheme = getTheme();

            options.forEach(function (option) {

                const isSelected =
                    option.dataset.themeOption === currentTheme;

                option.classList.toggle(
                    "is-selected",
                    isSelected
                );

                option.setAttribute(
                    "aria-checked",
                    String(isSelected)
                );

            });
        }


        /* -------------------------------------------------
           Open Menu
           ------------------------------------------------- */

        function openMenu() {

            menu.hidden = false;

            toggle.classList.add(
                "is-open"
            );

            toggle.setAttribute(
                "aria-expanded",
                "true"
            );

            updateSelectedTheme();
        }


        /* -------------------------------------------------
           Close Menu
           ------------------------------------------------- */

        function closeMenu() {

            menu.hidden = true;

            toggle.classList.remove(
                "is-open"
            );

            toggle.setAttribute(
                "aria-expanded",
                "false"
            );
        }


        /* -------------------------------------------------
           Theme Button
           ------------------------------------------------- */

        toggle.addEventListener(
            "click",
            function (event) {

                event.stopPropagation();

                if (menu.hidden) {

                    openMenu();

                } else {

                    closeMenu();

                }

            }
        );


        /* -------------------------------------------------
           Theme Options
           ------------------------------------------------- */

        options.forEach(function (option) {

            option.addEventListener(
                "click",
                function () {

                    const theme =
                        option.dataset.themeOption;

                    applyTheme(theme);

                    updateSelectedTheme();

                    closeMenu();

                }
            );

        });


        /* -------------------------------------------------
           Close When Clicking Outside
           ------------------------------------------------- */

        document.addEventListener(
            "click",
            function (event) {

                if (
                    !event.target.closest(
                        ".theme-picker"
                    )
                ) {

                    closeMenu();

                }

            }
        );


        /* -------------------------------------------------
           Keep Selection In Sync
           ------------------------------------------------- */

        window.addEventListener(
            "careerai-theme-change",
            updateSelectedTheme
        );


        /* -------------------------------------------------
           Initial Selection
           ------------------------------------------------- */

        updateSelectedTheme();

    }


    /* -----------------------------------------------------
       Public Theme API
       ----------------------------------------------------- */

    window.CareerAITheme = {

        set: applyTheme,

        get: getTheme,

        available: VALID_THEMES.slice()

    };


    /* -----------------------------------------------------
       Start Theme Engine
       ----------------------------------------------------- */

    function initializeCareerAITheme() {

        initializeTheme();

        initializeThemePicker();

    }


    if (document.readyState === "loading") {

        document.addEventListener(
            "DOMContentLoaded",
            initializeCareerAITheme
        );

    } else {

        initializeCareerAITheme();

    }

})();