/**
 * SearXNG API 客户端 (JavaScript)
 * 提供Node.js和浏览器端调用SearXNG搜索功能
 * 支持JSON API
 */

class SearXNGClient {
    /**
     * @param {string} baseUrl - SearXNG服务地址
     */
    constructor(baseUrl = 'http://localhost:8888') {
        this.baseUrl = baseUrl.replace(/\/$/, '');
    }

    /**
     * 执行搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @param {string[]} options.engines - 搜索引擎列表
     * @param {string} options.language - 搜索语言
     * @param {number} options.page - 页码
     * @param {string} options.timeRange - 时间范围
     * @param {number} options.safeSearch - 安全搜索级别
     * @returns {Promise<Object>} 搜索结果
     */
    async search(query, options = {}) {
        const params = new URLSearchParams({
            q: query,
            format: 'json',
            language: options.language || 'auto',
            pageno: options.page || 1,
            time_range: options.timeRange || '',
            safe_search: options.safeSearch || 0
        });

        if (options.engines) {
            params.append('engines', options.engines.join(','));
        }

        const response = await fetch(`${this.baseUrl}/search?${params}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    /**
     * 百度搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchBaidu(query, options = {}) {
        return this.search(query, { ...options, engines: ['baidu'] });
    }

    /**
     * 搜狗搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchSogou(query, options = {}) {
        return this.search(query, { ...options, engines: ['sogou'] });
    }

    /**
     * 360搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async search360(query, options = {}) {
        return this.search(query, { ...options, engines: ['360search'] });
    }

    /**
     * Google搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchGoogle(query, options = {}) {
        return this.search(query, { ...options, engines: ['google'] });
    }

    /**
     * 学术搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchAcademic(query, options = {}) {
        return this.search(query, { 
            ...options, 
            engines: ['google_scholar', 'arxiv'] 
        });
    }

    /**
     * 微信搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchWechat(query, options = {}) {
        return this.search(query, { ...options, engines: ['sogou_wechat'] });
    }

    /**
     * 开发者搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchDev(query, options = {}) {
        return this.search(query, { 
            ...options, 
            engines: ['github', 'stackoverflow', 'huggingface'] 
        });
    }

    /**
     * 图片搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchImages(query, options = {}) {
        return this.search(query, { 
            ...options, 
            engines: ['baidu_images', 'sogou_images', 'google_images'] 
        });
    }

    /**
     * 视频搜索
     * @param {string} query - 搜索关键词
     * @param {Object} options - 搜索选项
     * @returns {Promise<Object>} 搜索结果
     */
    async searchVideos(query, options = {}) {
        return this.search(query, { 
            ...options, 
            engines: ['360search_videos', 'sogou_videos', 'youtube_noapi'] 
        });
    }

    /**
     * 健康检查
     * @returns {Promise<boolean>} 服务是否正常
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/`, { 
                method: 'HEAD',
                timeout: 5000 
            });
            return response.ok;
        } catch {
            return false;
        }
    }

    /**
     * 获取搜索引擎列表
     * @returns {Promise<Object>} 配置信息
     */
    async getConfig() {
        const response = await fetch(`${this.baseUrl}/config`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SearXNGClient;
}
if (typeof window !== 'undefined') {
    window.SearXNGClient = SearXNGClient;
}

// 使用示例
if (typeof require !== 'undefined' && require.main === module) {
    const client = new SearXNGClient();
    
    (async () => {
        // 健康检查
        const isHealthy = await client.healthCheck();
        console.log(`SearXNG服务状态: ${isHealthy ? '正常' : '异常'}`);
        
        if (!isHealthy) return;
        
        // 百度搜索示例
        console.log('\n=== 百度搜索 ===');
        const results = await client.searchBaidu('医疗AI');
        results.results.slice(0, 3).forEach(result => {
            console.log(`标题: ${result.title}`);
            console.log(`链接: ${result.url}`);
            console.log();
        });
        
        // 学术搜索示例
        console.log('\n=== 学术搜索 ===');
        const academicResults = await client.searchAcademic('artificial intelligence healthcare');
        academicResults.results.slice(0, 3).forEach(result => {
            console.log(`标题: ${result.title}`);
            console.log(`链接: ${result.url}`);
            console.log();
        });
    })();
}
