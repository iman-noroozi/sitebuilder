    async enhanceTemplate(templatePath) {
        console.log(`\n🎨 شروع بهبود قالب: ${templatePath}`);
        
        try {
            const template = await fs.readFile(templatePath, 'utf-8');
            const enhancedTemplate = this.applyEnhancements(template);
            await fs.writeFile(templatePath, enhancedTemplate);
            console.log(`✅ بهبود قالب ${templatePath} با موفقیت انجام شد`);
        } catch (error) {
            console.error(`❌ خطا در بهبود قالب ${templatePath}:`, error.message);
        }
    }

    applyEnhancements(template) {
        // اینجا می‌توانید بهبودهای مورد نظر خود را اعمال کنید
        return template.replace(/<\/body>/, `
            <script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>
            <script>
                // کدهای جاوااسکریپت بهبود یافته
            </script>
        </body>`);
    }               
