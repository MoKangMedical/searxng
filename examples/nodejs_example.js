/**
 * SearXNG Node.js 集成示例
 * 演示如何在Node.js项目中使用SearXNG
 */

// 引入API客户端
const SearXNGClient = require('../api/searxng');

async function exampleBasicSearch() {
    console.log('=== 基础搜索示例 ===');
    
    const client = new SearXNGClient();
    
    // 检查服务状态
    const isHealthy = await client.healthCheck();
    if (!isHealthy) {
        console.log('SearXNG服务不可用，请先启动服务');
        return;
    }
    
    console.log('SearXNG服务正常');
    
    // 百度搜索
    const baiduResults = await client.searchBaidu('医疗AI');
    console.log(`百度搜索结果数: ${baiduResults.results.length}`);
    
    // 搜狗搜索
    const sogouResults = await client.searchSogou('医疗AI');
    console.log(`搜狗搜索结果数: ${sogouResults.results.length}`);
    
    // 360搜索
    const so360Results = await client.search360('医疗AI');
    console.log(`360搜索结果数: ${so360Results.results.length}`);
}

async function exampleAcademicSearch() {
    console.log('\n=== 学术搜索示例 ===');
    
    const client = new SearXNGClient();
    
    // 学术搜索
    const results = await client.searchAcademic('artificial intelligence healthcare');
    console.log(`学术搜索结果数: ${results.results.length}`);
    
    // 显示前3个结果
    results.results.slice(0, 3).forEach((result, i) => {
        console.log(`\n${i + 1}. ${result.title}`);
        console.log(`   链接: ${result.url}`);
        console.log(`   来源: ${result.engine || 'unknown'}`);
    });
}

async function exampleWechatSearch() {
    console.log('\n=== 微信搜索示例 ===');
    
    const client = new SearXNGClient();
    
    // 微信搜索
    const results = await client.searchWechat('医疗AI');
    console.log(`微信搜索结果数: ${results.results.length}`);
    
    // 显示前3个结果
    results.results.slice(0, 3).forEach((result, i) => {
        console.log(`\n${i + 1}. ${result.title}`);
        console.log(`   链接: ${result.url}`);
        console.log(`   来源: ${result.engine || 'unknown'}`);
    });
}

async function exampleDevSearch() {
    console.log('\n=== 开发者搜索示例 ===');
    
    const client = new SearXNGClient();
    
    // 开发者搜索
    const results = await client.searchDev('machine learning');
    console.log(`开发者搜索结果数: ${results.results.length}`);
    
    // 显示前3个结果
    results.results.slice(0, 3).forEach((result, i) => {
        console.log(`\n${i + 1}. ${result.title}`);
        console.log(`   链接: ${result.url}`);
        console.log(`   来源: ${result.engine || 'unknown'}`);
    });
}

async function exampleCustomSearch() {
    console.log('\n=== 自定义搜索示例 ===');
    
    const client = new SearXNGClient();
    
    // 使用多个引擎搜索
    const results = await client.search('医疗AI', {
        engines: ['baidu', 'sogou', 'google_scholar'],
        language: 'zh-CN',
        page: 1
    });
    
    console.log(`自定义搜索结果数: ${results.results.length}`);
    
    // 按引擎分组显示
    const engines = {};
    results.results.forEach(result => {
        const engine = result.engine || 'unknown';
        if (!engines[engine]) {
            engines[engine] = [];
        }
        engines[engine].push(result);
    });
    
    Object.entries(engines).forEach(([engine, engineResults]) => {
        console.log(`\n${engine}: ${engineResults.length} 个结果`);
        engineResults.slice(0, 2).forEach(result => {
            console.log(`  - ${result.title}`);
        });
    });
}

async function main() {
    console.log('SearXNG Node.js 集成示例');
    console.log('='.repeat(50));
    
    try {
        await exampleBasicSearch();
        await exampleAcademicSearch();
        await exampleWechatSearch();
        await exampleDevSearch();
        await exampleCustomSearch();
        
        console.log('\n' + '='.repeat(50));
        console.log('所有示例执行完成！');
        
    } catch (error) {
        console.error(`错误: ${error.message}`);
        console.error(error.stack);
    }
}

// 运行示例
if (require.main === module) {
    main();
}

module.exports = {
    exampleBasicSearch,
    exampleAcademicSearch,
    exampleWechatSearch,
    exampleDevSearch,
    exampleCustomSearch
};
