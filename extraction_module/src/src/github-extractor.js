// استخراج ابزارهای سایت‌سازی از GitHub
const https = require('https');
const fs = require('fs-extra');
const path = require('path');

class GitHubResourceExtractor {
    constructor() {
        this.extractedRepos = [];
        this.errors = [];
    }

    async extractGitHubResources() {
        console.log('🐙 شروع استخراج منابع GitHub...');
        
        // بهترین repository های سایت‌سازی
        const topRepos = {
            websiteBuilders: [
                'grapesjs/grapesjs',           // Visual Builder
                'unlayer/react-email-editor',  // Email Builder  
                'BuilderIO/builder',           // Visual Builder
                'webstudio-is/webstudio',      // Open Source Builder
                'blocks/blocks',               // WordPress Builder
                'tinacms/tinacms',            // CMS Builder
                'forestryio/forestry.io',     // Static Site CMS
                'netlify/netlify-cms'         // Git-based CMS
            ],
            
            frameworks: [
                'twbs/bootstrap',              // Bootstrap
                'tailwindlabs/tailwindcss',   // Tailwind
                'mui/material-ui',            // Material UI
                'ant-design/ant-design',      // Ant Design
                'chakra-ui/chakra-ui',        // Chakra UI
                'mantinedev/mantine',         // Mantine
                'foundation/foundation-sites', // Foundation
                'jgthms/bulma'                // Bulma
            ],
            
            pageBuilders: [
                'elementor/elementor',         // WordPress Builder
                'beaver-builder/bb-plugin',    // Beaver Builder
                'siteorigin/siteorigin-panels', // SiteOrigin
                'Codeinwp/neve',              // WordPress Theme
                'wpbakery/js_composer',       // WPBakery
                'kingcomposer/kingcomposer'    // King Composer
            ],
            
            staticSiteGenerators: [
                'gatsbyjs/gatsby',            // Gatsby
                'vercel/next.js',             // Next.js
                'nuxt/nuxt.js',              // Nuxt.js
                'vuejs/vuepress',            // VuePress
                'facebook/docusaurus',        // Docusaurus
                'gridsome/gridsome',          // Gridsome
                'gohugoio/hugo',             // Hugo
                'jekyll/jekyll'              // Jekyll
            ],
            
            componentLibraries: [
                'react-bootstrap/react-bootstrap', // React Bootstrap
                'semantic-org/semantic-ui',        // Semantic UI
                'grommet/grommet',                 // Grommet
                'arco-design/arco-design',         // Arco Design
                'semi-design/semi-design',         // Semi Design
                'DouyinFE/semi-design'             // Semi Design
            ],
            
            designSystems: [
                'primer/css',                 // GitHub Primer
                'carbon-design-system/carbon', // IBM Carbon
                'microsoft/fluentui',         // Microsoft Fluent
                'salesforce/design-system',   // Salesforce Lightning
                'atlassian/design-system',    // Atlassian Design
                'shopify/polaris'            // Shopify Polaris
            ],
            
            adminTemplates: [
                'ColorlibHQ/AdminLTE',        // AdminLTE
                'coreui/coreui-free-bootstrap-admin-template', // CoreUI
                'creativetimofficial/material-dashboard', // Material Dashboard
                'wrappixel/materialpro-bootstrap-dashboard', // MaterialPro
                'puikinsh/gentelella',        // Gentelella
                'tabler/tabler'               // Tabler
            ],
            
            landingPageTemplates: [
                'cruip/open-react-template',  // React Templates
                'tailwindtoolbox/tailwindcss-templates', // Tailwind Templates
                'html5up/html5up.github.io',  // HTML5 UP
                'BlackrockDigital/startbootstrap', // Start Bootstrap
                'themefisher/navigation-menu', // Navigation Menus
                'ColorlibHQ/awesome-landing-page' // Landing Pages
            ]
        };

        // شروع استخراج از هر دسته
        for (const [category, repos] of Object.entries(topRepos)) {
            console.log(`\n🔥 دسته: ${category} (${repos.length} مخزن)`);
            
            for (const repo of repos) {
                try {
                    await this.extractRepo(repo, category);
                    await this.delay(1000); // جلوگیری از محدودیت GitHub API
                } catch (error) {
                    console.error(`❌ خطا در ${repo}:`, error.message);
                    this.errors.push({ repo, category, error: error.message });
                }
            }
        }

        await this.generateGitHubReport();
        console.log(`✅ استخراج GitHub کامل شد! ${this.extractedRepos.length} مخزن`);
    }

    async extractRepo(repoPath, category) {
        console.log(`📦 در حال بررسی: ${repoPath}`);
        
        const [owner, repo] = repoPath.split('/');
        
        try {
            // دریافت اطلاعات repository
            const repoInfo = await this.getRepoInfo(owner, repo);
            
            // دریافت فایل‌های مهم
            const importantFiles = await this.getImportantFiles(owner, repo);
            
            // دریافت README
            const readme = await this.getReadme(owner, repo);
            
            // ذخیره اطلاعات
            const extractedData = {
                name: repo,
                owner: owner,
                fullName: repoPath,
                category: category,
                description: repoInfo.description,
                stars: repoInfo.stargazers_count,
                forks: repoInfo.forks_count,
                language: repoInfo.language,
                homepage: repoInfo.homepage,
                topics: repoInfo.topics,
                importantFiles: importantFiles,
                readme: readme,
                extractedAt: new Date().toISOString()
            };

            // ذخیره در فایل
            const outputDir = `./extracted_sites/github_repos/${category}/${repo}`;
            await fs.ensureDir(outputDir);
            
            await fs.writeFile(
                path.join(outputDir, 'repo_info.json'),
                JSON.stringify(extractedData, null, 2)
            );

            if (readme) {
                await fs.writeFile(path.join(outputDir, 'README.md'), readme);
            }

            this.extractedRepos.push(extractedData);
            
            console.log(`✅ ${repoPath} - ⭐${repoInfo.stargazers_count} - ${repoInfo.language}`);
            
        } catch (error) {
            throw new Error(`خطا در استخراج ${repoPath}: ${error.message}`);
        }
    }

    async getRepoInfo(owner, repo) {
        return new Promise((resolve, reject) => {
            const options = {
                hostname: 'api.github.com',
                path: `/repos/${owner}/${repo}`,
                headers: {
                    'User-Agent': 'Website-Builder-Extractor',
                    'Accept': 'application/vnd.github.v3+json'
                }
            };

            const req = https.get(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const jsonData = JSON.parse(data);
                        resolve(jsonData);
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.setTimeout(10000, () => reject(new Error('Timeout')));
        });
    }

    async getImportantFiles(owner, repo) {
        // فایل‌های مهم که باید بررسی شوند
        const importantFileNames = [
            'package.json',
            'composer.json', 
            'bower.json',
            'webpack.config.js',
            'gulpfile.js',
            'rollup.config.js',
            'tsconfig.json',
            'tailwind.config.js',
            'next.config.js',
            'nuxt.config.js',
            'gatsby-config.js'
        ];

        const foundFiles = [];
        
        for (const fileName of importantFileNames) {
            try {
                const fileContent = await this.getFileContent(owner, repo, fileName);
                if (fileContent) {
                    foundFiles.push({ name: fileName, content: fileContent });
                }
            } catch (error) {
                // فایل وجود ندارد، ادامه می‌دهیم
            }
        }

        return foundFiles;
    }

    async getReadme(owner, repo) {
        try {
            return await this.getFileContent(owner, repo, 'README.md');
        } catch (error) {
            try {
                return await this.getFileContent(owner, repo, 'readme.md');
            } catch (error2) {
                return null;
            }
        }
    }

    async getFileContent(owner, repo, fileName) {
        return new Promise((resolve, reject) => {
            const options = {
                hostname: 'api.github.com',
                path: `/repos/${owner}/${repo}/contents/${fileName}`,
                headers: {
                    'User-Agent': 'Website-Builder-Extractor',
                    'Accept': 'application/vnd.github.v3+json'
                }
            };

            const req = https.get(options, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const jsonData = JSON.parse(data);
                        if (jsonData.content) {
                            const content = Buffer.from(jsonData.content, 'base64').toString('utf8');
                            resolve(content);
                        } else {
                            reject(new Error('No content'));
                        }
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.setTimeout(5000, () => reject(new Error('Timeout')));
        });
    }

    async generateGitHubReport() {
        const report = {
            githubExtraction: {
                title: "استخراج منابع GitHub برای سایت‌سازی",
                completedAt: new Date().toISOString(),
                totalRepos: this.extractedRepos.length,
                errors: this.errors.length,
                categories: {}
            },
            topRepositories: this.extractedRepos
                .sort((a, b) => b.stars - a.stars)
                .slice(0, 20)
                .map(repo => ({
                    name: repo.fullName,
                    stars: repo.stars,
                    language: repo.language,
                    description: repo.description
                })),
            byLanguage: this.groupByLanguage(),
            byCategory: this.groupByCategory(),
            recommendations: [
                "🎯 GrapesJS برای Visual Builder",
                "🚀 Next.js برای React SSG",
                "🎨 Material-UI برای کامپوننت‌های زیبا",
                "⚡ TailwindCSS برای طراحی سریع",
                "🏗️ Builder.io برای CMS بصری",
                "📱 AdminLTE برای Dashboard حرفه‌ای"
            ]
        };

        await fs.writeFile('./extracted_sites/GITHUB_RESOURCES_REPORT.json', JSON.stringify(report, null, 2));
        
        console.log('\n📊 گزارش GitHub:');
        console.log(`   📦 مخازن: ${this.extractedRepos.length}`);
        console.log(`   ❌ خطاها: ${this.errors.length}`);
        console.log('   📄 گزارش در GITHUB_RESOURCES_REPORT.json');
    }

    groupByLanguage() {
        const byLanguage = {};
        this.extractedRepos.forEach(repo => {
            const lang = repo.language || 'Unknown';
            if (!byLanguage[lang]) byLanguage[lang] = [];
            byLanguage[lang].push(repo.fullName);
        });
        return byLanguage;
    }

    groupByCategory() {
        const byCategory = {};
        this.extractedRepos.forEach(repo => {
            if (!byCategory[repo.category]) byCategory[repo.category] = [];
            byCategory[repo.category].push({
                name: repo.fullName,
                stars: repo.stars,
                description: repo.description
            });
        });
        return byCategory;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

if (require.main === module) {
    const extractor = new GitHubResourceExtractor();
    extractor.extractGitHubResources().catch(console.error);
}

module.exports = GitHubResourceExtractor;
