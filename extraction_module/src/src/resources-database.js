// منابع بهترین ابزارهای سایت‌سازی دنیا
const resources = {
    // منابع اصلی ابزارهای سایت‌سازی
    builders: {
        "webflow": {
            url: "https://webflow.com/",
            type: "Visual Builder",
            description: "بهترین ابزار طراحی بصری",
            features: ["Visual Design", "CMS", "E-commerce", "Interactions"]
        },
        "framer": {
            url: "https://framer.com/",
            type: "Design Tool",
            description: "ابزار پیشرفته طراحی و پروتوتایپ",
            features: ["Prototyping", "Components", "Animations"]
        },
        "wix": {
            url: "https://www.wix.com/",
            type: "Website Builder",
            description: "سایت‌ساز محبوب و آسان",
            features: ["Drag & Drop", "Templates", "App Market"]
        },
        "squarespace": {
            url: "https://www.squarespace.com/",
            type: "Website Builder", 
            description: "طراحی زیبا و حرفه‌ای",
            features: ["Beautiful Templates", "E-commerce", "Blogging"]
        },
        "elementor": {
            url: "https://elementor.com/",
            type: "WordPress Builder",
            description: "بهترین page builder وردپرس",
            features: ["WordPress Integration", "Widgets", "Theme Builder"]
        }
    },

    // منابع کدهای آماده
    codeResources: {
        "codepen": {
            url: "https://codepen.io/",
            type: "Code Playground",
            description: "نمونه کدهای HTML/CSS/JS",
            searchUrls: [
                "https://codepen.io/search/pens?q=website+builder",
                "https://codepen.io/search/pens?q=dashboard",
                "https://codepen.io/search/pens?q=admin+panel"
            ]
        },
        "github": {
            url: "https://github.com/",
            type: "Code Repository",
            description: "کدهای متن‌باز ابزارهای سایت‌سازی",
            searchUrls: [
                "https://github.com/search?q=website+builder",
                "https://github.com/search?q=page+builder",
                "https://github.com/search?q=site+generator"
            ]
        },
        "themeforest": {
            url: "https://themeforest.net/",
            type: "Premium Themes",
            description: "قالب‌های حرفه‌ای و ابزارهای طراحی",
            categories: ["Admin Templates", "Site Templates", "Landing Pages"]
        }
    },

    // ابزارهای توسعه
    devTools: {
        "bootstrap": {
            url: "https://getbootstrap.com/",
            type: "CSS Framework",
            description: "فریمورک محبوب CSS",
            downloadUrl: "https://github.com/twbs/bootstrap/releases"
        },
        "tailwindcss": {
            url: "https://tailwindcss.com/",
            type: "CSS Framework", 
            description: "فریمورک utility-first CSS"
        },
        "materialui": {
            url: "https://mui.com/",
            type: "React Components",
            description: "کامپوننت‌های Material Design"
        },
        "antd": {
            url: "https://ant.design/",
            type: "React UI Library",
            description: "کتابخانه UI حرفه‌ای"
        }
    },

    // منابع الهام و ایده
    inspiration: {
        "dribbble": {
            url: "https://dribbble.com/",
            type: "Design Inspiration",
            description: "طراحی‌های الهام‌بخش",
            searchUrls: [
                "https://dribbble.com/search/website-builder",
                "https://dribbble.com/search/dashboard",
                "https://dribbble.com/search/admin-panel"
            ]
        },
        "behance": {
            url: "https://www.behance.net/",
            type: "Creative Showcase",
            description: "نمایشگاه آثار خلاقانه"
        },
        "awwwards": {
            url: "https://www.awwwards.com/",
            type: "Web Design Awards",
            description: "بهترین طراحی‌های وب"
        }
    },

    // ابزارهای آنلاین رایگان
    freeTools: {
        "figma": {
            url: "https://www.figma.com/",
            type: "Design Tool",
            description: "ابزار طراحی آنلاین رایگان"
        },
        "canva": {
            url: "https://www.canva.com/",
            type: "Graphic Design",
            description: "ابزار طراحی گرافیکی آسان"
        },
        "unsplash": {
            url: "https://unsplash.com/",
            type: "Free Photos",
            description: "تصاویر رایگان با کیفیت بالا"
        },
        "fontawesome": {
            url: "https://fontawesome.com/",
            type: "Icons",
            description: "آیکون‌های وکتور رایگان"
        }
    }
};

// لیست اولویت‌دار سایت‌ها برای استخراج
const extractionPriority = [
    // اولویت 1: ابزارهای اصلی سایت‌سازی
    { name: "Webflow", url: "https://webflow.com/", priority: 1 },
    { name: "Framer", url: "https://framer.com/", priority: 1 },
    { name: "Wix", url: "https://www.wix.com/", priority: 1 },
    { name: "Squarespace", url: "https://www.squarespace.com/", priority: 1 },
    
    // اولویت 2: فریمورک‌ها و کتابخانه‌ها
    { name: "Bootstrap", url: "https://getbootstrap.com/", priority: 2 },
    { name: "TailwindCSS", url: "https://tailwindcss.com/", priority: 2 },
    { name: "MaterialUI", url: "https://mui.com/", priority: 2 },
    { name: "AntDesign", url: "https://ant.design/", priority: 2 },
    
    // اولویت 3: ابزارهای طراحی
    { name: "Figma", url: "https://www.figma.com/", priority: 3 },
    { name: "Dribbble", url: "https://dribbble.com/", priority: 3 },
    { name: "Awwwards", url: "https://www.awwwards.com/", priority: 3 }
];

// منابع دانلود مستقیم
const directDownloads = {
    templates: [
        "https://html5up.net/", // قالب‌های HTML5 رایگان
        "https://templatemo.com/", // قالب‌های رایگان
        "https://www.free-css.com/", // قالب‌های CSS رایگان
        "https://startbootstrap.com/" // قالب‌های Bootstrap رایگان
    ],
    
    frameworks: [
        "https://github.com/twbs/bootstrap/releases", // Bootstrap
        "https://github.com/tailwindlabs/tailwindcss/releases", // Tailwind
        "https://github.com/mui/material-ui/releases", // Material-UI
        "https://github.com/ant-design/ant-design/releases" // Ant Design
    ],
    
    icons: [
        "https://fontawesome.com/download", // Font Awesome
        "https://feathericons.com/", // Feather Icons
        "https://heroicons.com/", // Hero Icons
        "https://lucide.dev/" // Lucide Icons
    ]
};

module.exports = {
    resources,
    extractionPriority,
    directDownloads
};
