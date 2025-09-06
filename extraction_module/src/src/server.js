// Express Server for Website Template Extractor

const express = require('express');
const path = require('path');
const fs = require('fs-extra');
const { v4: uuidv4 } = require('uuid');
const DeepWebsiteCloner = require('./deep-cloner');

class ExtractorServer {
    constructor() {
        this.app = express();
        this.port = process.env.PORT || 3000;
        this.jobs = new Map(); // Store active jobs
        
        this.setupMiddleware();
        this.setupRoutes();
    }

    setupMiddleware() {
        // Body parsing
        this.app.use(express.json());
        this.app.use(express.urlencoded({ extended: true }));
        
        // Serve static files
        this.app.use(express.static(path.join(__dirname, '../public')));

        // CORS for development
        this.app.use((req, res, next) => {
            res.header('Access-Control-Allow-Origin', '*');
            res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
            res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
            next();
        });

        // Logging
        this.app.use((req, res, next) => {
            console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
            next();
        });
    }

    setupRoutes() {
        // Serve main page
        this.app.get('/', (req, res) => {
            res.sendFile(path.join(__dirname, '../public/index.html'));
        });

        // Start extraction
        this.app.post('/api/extract', async (req, res) => {
            try {
                const { url, ...options } = req.body;
                
                if (!url) {
                    return res.status(400).json({ error: 'URL is required' });
                }

                // Validate URL
                try {
                    new URL(url);
                } catch {
                    return res.status(400).json({ error: 'Invalid URL format' });
                }

                const jobId = uuidv4();
                const job = {
                    id: jobId,
                    url: url,
                    options: options,
                    status: 'starting',
                    progress: 0,
                    currentTask: 'آماده‌سازی...',
                    startTime: new Date(),
                    logs: [],
                    stats: {},
                    outputPath: null
                };

                this.jobs.set(jobId, job);
                
                // Start extraction in background
                this.startExtraction(jobId, url, options);

                res.json({ 
                    jobId: jobId,
                    message: 'استخراج شروع شد'
                });

            } catch (error) {
                console.error('خطا در شروع استخراج:', error);
                res.status(500).json({ error: 'خطا در شروع استخراج' });
            }
        });

        // Get job status
        this.app.get('/api/status/:jobId', (req, res) => {
            const jobId = req.params.jobId;
            const job = this.jobs.get(jobId);

            if (!job) {
                return res.status(404).json({ error: 'Job پیدا نشد' });
            }

            res.json({
                status: job.status,
                progress: job.progress,
                currentTask: job.currentTask,
                logs: job.logs.slice(-10), // آخرین 10 لاگ
                stats: job.stats,
                startTime: job.startTime
            });
        });

        // Download result
        this.app.get('/api/download/:jobId', async (req, res) => {
            const jobId = req.params.jobId;
            const job = this.jobs.get(jobId);

            if (!job) {
                return res.status(404).json({ error: 'Job پیدا نشد' });
            }

            if (job.status !== 'completed') {
                return res.status(400).json({ error: 'استخراج هنوز تمام نشده' });
            }

            const zipPath = `${job.outputPath}.zip`;
            
            if (!await fs.pathExists(zipPath)) {
                return res.status(404).json({ error: 'فایل ZIP پیدا نشد' });
            }

            const stats = await fs.stat(zipPath);
            const filename = `extracted-${new URL(job.url).hostname}-${jobId}.zip`;

            res.setHeader('Content-Type', 'application/zip');
            res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
            res.setHeader('Content-Length', stats.size);

            const stream = fs.createReadStream(zipPath);
            stream.pipe(res);
        });

        // List all jobs
        this.app.get('/api/jobs', (req, res) => {
            const jobs = Array.from(this.jobs.values()).map(job => ({
                id: job.id,
                url: job.url,
                status: job.status,
                progress: job.progress,
                startTime: job.startTime,
                stats: job.stats
            }));

            res.json(jobs);
        });

        // Delete job
        this.app.delete('/api/jobs/:jobId', async (req, res) => {
            const jobId = req.params.jobId;
            const job = this.jobs.get(jobId);

            if (!job) {
                return res.status(404).json({ error: 'Job پیدا نشد' });
            }

            // Clean up files
            if (job.outputPath) {
                try {
                    await fs.remove(job.outputPath);
                    await fs.remove(`${job.outputPath}.zip`);
                } catch (error) {
                    console.error('خطا در حذف فایل‌ها:', error);
                }
            }

            this.jobs.delete(jobId);
            res.json({ message: 'Job حذف شد' });
        });

        // Health check
        this.app.get('/health', (req, res) => {
            res.json({ 
                status: 'OK',
                uptime: process.uptime(),
                activeJobs: this.jobs.size,
                memory: process.memoryUsage()
            });
        });
    }

    async startExtraction(jobId, url, options) {
        const job = this.jobs.get(jobId);
        if (!job) return;

        let cloner = null;

        try {
            this.updateJob(jobId, {
                status: 'running',
                progress: 10,
                currentTask: 'راه‌اندازی مرورگر...'
            });

            cloner = new DeepWebsiteCloner({
                outputDir: './extracted_sites',
                ...options
            });

            await cloner.init();

            this.updateJob(jobId, {
                progress: 20,
                currentTask: 'شروع استخراج...'
            });

            // Custom progress tracking
            const originalExtractPage = cloner.extractPage.bind(cloner);
            let processedPages = 0;
            
            cloner.extractPage = async function(url, baseDir, depth) {
                processedPages++;
                const progress = Math.min(90, 20 + (processedPages * 5));
                
                this.updateJob(jobId, {
                    progress: progress,
                    currentTask: `استخراج صفحه ${processedPages}: ${url.substring(0, 50)}...`
                });

                return await originalExtractPage(url, baseDir, depth);
            }.bind(this);

            const outputPath = await cloner.cloneWebsite(url);

            this.updateJob(jobId, {
                status: 'completed',
                progress: 100,
                currentTask: 'تمام شد!',
                outputPath: outputPath,
                stats: {
                    totalPages: cloner.visitedUrls.size,
                    totalAssets: cloner.downloadedAssets.size,
                    totalSize: await this.getDirectorySize(outputPath)
                }
            });

            this.addJobLog(jobId, '🎉 استخراج با موفقیت تمام شد!', 'success');

        } catch (error) {
            console.error(`خطا در job ${jobId}:`, error);
            
            this.updateJob(jobId, {
                status: 'failed',
                error: error.message
            });

            this.addJobLog(jobId, `❌ خطا: ${error.message}`, 'error');
        } finally {
            if (cloner) {
                await cloner.close();
            }
        }
    }

    updateJob(jobId, updates) {
        const job = this.jobs.get(jobId);
        if (job) {
            Object.assign(job, updates);
            this.jobs.set(jobId, job);
        }
    }

    addJobLog(jobId, message, type = 'info') {
        const job = this.jobs.get(jobId);
        if (job) {
            job.logs.push({
                timestamp: new Date().toISOString(),
                message: message,
                type: type
            });
            
            // Keep only last 100 logs
            if (job.logs.length > 100) {
                job.logs = job.logs.slice(-100);
            }
            
            this.jobs.set(jobId, job);
        }
    }

    async getDirectorySize(dirPath) {
        try {
            let totalSize = 0;
            const files = await fs.readdir(dirPath, { recursive: true, withFileTypes: true });
            
            for (const file of files) {
                if (file.isFile()) {
                    const filePath = path.join(dirPath, file.name);
                    const stats = await fs.stat(filePath);
                    totalSize += stats.size;
                }
            }
            
            return totalSize;
        } catch (error) {
            return 0;
        }
    }

    start() {
        this.app.listen(this.port, () => {
            console.log(`🚀 استخراج کننده قالب‌های وب سایت`);
            console.log(`🌐 سرور در حال اجرا: http://localhost:${this.port}`);
            console.log(`📁 مسیر ذخیره: ./extracted_sites`);
            console.log(`⏰ زمان شروع: ${new Date().toLocaleString('fa-IR')}`);
        });
    }
}

// Start server if called directly
if (require.main === module) {
    const server = new ExtractorServer();
    server.start();
}

module.exports = ExtractorServer;
