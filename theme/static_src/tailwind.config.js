/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                'main': '#013561',
                'main-graded': {
                    '50': '#eef8ff',
                    '100': '#ddf1ff',
                    '200': '#b3e4ff',
                    '300': '#6fd0ff',
                    '400': '#23b8ff',
                    '500': '#009fff',
                    '600': '#007edd',
                    '700': '#0064b2',
                    '800': '#005493',
                    '900': '#014679',
                    '950': '#013561',
                },
                'main-dark': '#011E38',
                'main-dark-graded': {
                    '50': '#eef8ff',
                    '100': '#ddf1ff',
                    '200': '#b3e2ff',
                    '300': '#70ceff',
                    '400': '#25b4ff',
                    '500': '#009aff',
                    '600': '#007adb',
                    '700': '#0061b1',
                    '800': '#005292',
                    '900': '#024478',
                    '950': '#011e38',
                },
                'off': '#95c11f',
                'off-graded': {
                    '50': '#fafde8',
                    '100': '#f1facd',
                    '200': '#e2f4a2',
                    '300': '#cceb6b',
                    '400': '#b5dd3e',
                    '500': '#95c11f',
                    '600': '#759b15',
                    '700': '#587615',
                    '800': '#475e16',
                    '900': '#3d5017',
                    '950': '#1f2c07',
                },
                'off-dark': '#526B16',
                'off-dark-graded': {
                    '50': '#f9fce9',
                    '100': '#f1f8cf',
                    '200': '#e2f2a4',
                    '300': '#cbe76f',
                    '400': '#b4d843',
                    '500': '#96bd25',
                    '600': '#749719',
                    '700': '#526b16',
                    '800': '#475c18',
                    '900': '#3d4e19',
                    '950': '#1f2b08',
                },
                'action': '#DB6C00',
                'action-graded': {
                    '50': '#fffaea',
                    '100': '#fff2c5',
                    '200': '#ffe387',
                    '300': '#ffce48',
                    '400': '#ffb81e',
                    '500': '#fc9504',
                    '600': '#db6c00',
                    '700': '#b94a04',
                    '800': '#96390a',
                    '900': '#7b2f0c',
                    '950': '#471601',
                },
                'error': '#C10D00',
                'error-graded': {
                    '50': '#fff0ef',
                    '100': '#ffdedc',
                    '200': '#ffc3bf',
                    '300': '#ff9992',
                    '400': '#ff6054',
                    '500': '#ff2e1f',
                    '600': '#ff1100',
                    '700': '#db0f00',
                    '800': '#c10d00',
                    '900': '#941108',
                    '950': '#520600',
                },
                'off-white': '#f2f6fc',
                'off-white-graded': {
                    '50': '#f2f6fc',
                    '100': '#e2eaf7',
                    '200': '#cbdbf2',
                    '300': '#a7c4e9',
                    '400': '#7da4dd',
                    '500': '#5e86d3',
                    '600': '#4a6cc6',
                    '700': '#405bb5',
                    '800': '#394b94',
                    '900': '#324176',
                    '950': '#222a49',
                },
                'sb-gray': '#B9B9B9',
                'sb-gray-graded': {
                    '50': '#f8f8f8',
                    '100': '#f0f0f0',
                    '200': '#e4e4e4',
                    '300': '#d1d1d1',
                    '400': '#b9b9b9',
                    '500': '#9a9a9a',
                    '600': '#818181',
                    '700': '#6a6a6a',
                    '800': '#5a5a5a',
                    '900': '#4e4e4e',
                    '950': '#282828',
                },
                'h2-gray': '#6F6F6F',
                'h2-gray-graded': {
                    '50': '#f7f7f7',
                    '100': '#e3e3e3',
                    '200': '#c8c8c8',
                    '300': '#a4a4a4',
                    '400': '#818181',
                    '500': '#6f6f6f',
                    '600': '#515151',
                    '700': '#434343',
                    '800': '#383838',
                    '900': '#313131',
                    '950': '#1a1a1a',
                },
                'p-gray': '#858585',
                'p-gray-graded': {
                    '50': '#f8f8f8',
                    '100': '#f0f0f0',
                    '200': '#e4e4e4',
                    '300': '#d1d1d1',
                    '400': '#b4b4b4',
                    '500': '#9a9a9a',
                    '600': '#858585',
                    '700': '#6a6a6a',
                    '800': '#5a5a5a',
                    '900': '#4e4e4e',
                    '950': '#282828',
                },
            }
        },
    },
    screens: {
        'smartphone': { max: '639px' },
        'smartphone-xs': { max: '430px' },
        'navbar-smart': { max: '550px' },
    },
    fontFamily: {
        'Helvetica': 'Helvetica, sans',
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
