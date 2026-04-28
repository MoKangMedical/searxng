/**
 * SearXNG 自定义JavaScript - 医疗AI版 v3.0
 * 功能: 暗黑模式切换、搜索历史、即时答案
 */

// ===== 主题管理 =====
const ThemeManager = {
    init() {
        this.theme = localStorage.getItem('theme') || 'auto';
        this.apply();
        this.createToggleButton();
    },
    
    apply() {
        if (this.theme === 'auto') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', this.theme);
        }
    },
    
    toggle() {
        if (this.theme === 'auto') {
            this.theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark';
        } else if (this.theme === 'light') {
            this.theme = 'dark';
        } else {
            this.theme = 'auto';
        }
        localStorage.setItem('theme', this.theme);
        this.apply();
        this.updateToggleIcon();
    },
    
    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'theme-toggle';
        button.innerHTML = this.getIcon();
        button.title = '切换主题';
        button.addEventListener('click', () => this.toggle());
        document.body.appendChild(button);
    },
    
    updateToggleIcon() {
        const button = document.querySelector('.theme-toggle');
        if (button) {
            button.innerHTML = this.getIcon();
        }
    },
    
    getIcon() {
        if (this.theme === 'dark') {
            return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
        } else if (this.theme === 'light') {
            return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
        } else {
            return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>';
        }
    }
};

// ===== 搜索历史管理 =====
const SearchHistory = {
    maxItems: 10,
    
    init() {
        this.history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
        this.bindEvents();
    },
    
    add(query) {
        if (!query || query.trim() === '') return;
        
        // 移除重复项
        this.history = this.history.filter(item => item !== query);
        
        // 添加到开头
        this.history.unshift(query);
        
        // 限制数量
        if (this.history.length > this.maxItems) {
            this.history = this.history.slice(0, this.maxItems);
        }
        
        this.save();
    },
    
    remove(query) {
        this.history = this.history.filter(item => item !== query);
        this.save();
    },
    
    clear() {
        this.history = [];
        this.save();
    },
    
    save() {
        localStorage.setItem('searchHistory', JSON.stringify(this.history));
    },
    
    bindEvents() {
        const searchInput = document.getElementById('q');
        if (!searchInput) return;
        
        // 显示搜索历史
        searchInput.addEventListener('focus', () => {
            if (this.history.length > 0) {
                this.showDropdown();
            }
        });
        
        // 隐藏搜索历史
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#search')) {
                this.hideDropdown();
            }
        });
        
        // 表单提交时保存历史
        const form = searchInput.closest('form');
        if (form) {
            form.addEventListener('submit', () => {
                this.add(searchInput.value);
            });
        }
    },
    
    showDropdown() {
        this.hideDropdown();
        
        const searchInput = document.getElementById('q');
        const dropdown = document.createElement('div');
        dropdown.className = 'search-history';
        
        this.history.forEach(query => {
            const item = document.createElement('div');
            item.className = 'item';
            item.innerHTML = `
                <span class="icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>
                </span>
                <span class="text">${this.escapeHtml(query)}</span>
                <span class="delete" data-query="${this.escapeHtml(query)}">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"/>
                        <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                </span>
            `;
            
            // 点击填充搜索框
            item.querySelector('.text').addEventListener('click', () => {
                searchInput.value = query;
                searchInput.closest('form').submit();
            });
            
            // 删除单个项目
            item.querySelector('.delete').addEventListener('click', (e) => {
                e.stopPropagation();
                this.remove(query);
                this.showDropdown();
            });
            
            dropdown.appendChild(item);
        });
        
        // 清除所有历史
        if (this.history.length > 0) {
            const clearAll = document.createElement('div');
            clearAll.className = 'item';
            clearAll.innerHTML = `
                <span class="icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                </span>
                <span class="text" style="color: var(--text-secondary);">清除所有历史</span>
            `;
            clearAll.addEventListener('click', () => {
                this.clear();
                this.hideDropdown();
            });
            dropdown.appendChild(clearAll);
        }
        
        searchInput.parentNode.appendChild(dropdown);
    },
    
    hideDropdown() {
        const dropdown = document.querySelector('.search-history');
        if (dropdown) {
            dropdown.remove();
        }
    },
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// ===== 即时答案 =====
const InstantAnswers = {
    init() {
        this.checkForInstantAnswer();
    },
    
    checkForInstantAnswer() {
        const query = new URLSearchParams(window.location.search).get('q');
        if (!query) return;
        
        // 检查是否是计算器查询
        if (this.isCalculatorQuery(query)) {
            this.showCalculatorResult(query);
        }
        
        // 检查是否是单位转换查询
        if (this.isUnitConversionQuery(query)) {
            this.showUnitConversionResult(query);
        }
        
        // 检查是否是天气查询
        if (this.isWeatherQuery(query)) {
            this.showWeatherHint(query);
        }
    },
    
    isCalculatorQuery(query) {
        return /^[\d\s\+\-\*\/\(\)\.\%\^]+$/.test(query) && 
               /[\+\-\*\/\%\^]/.test(query);
    },
    
    isUnitConversionQuery(query) {
        const unitPatterns = [
            /\d+\s*(km|mi|miles?|m|ft|inches?|cm|mm)\s*(to|in)\s*(km|mi|miles?|m|ft|inches?|cm|mm)/i,
            /\d+\s*(kg|lbs?|pounds?|g|oz|ounces?)\s*(to|in)\s*(kg|lbs?|pounds?|g|oz|ounces?)/i,
            /\d+\s*(celsius|fahrenheit|kelvin|°C|°F|K)\s*(to|in)\s*(celsius|fahrenheit|kelvin|°C|°F|K)/i
        ];
        return unitPatterns.some(pattern => pattern.test(query));
    },
    
    isWeatherQuery(query) {
        return /weather|天气|temperature|温度/i.test(query);
    },
    
    showCalculatorResult(query) {
        try {
            // 安全的数学表达式计算
            const result = Function('"use strict"; return (' + query + ')')();
            if (typeof result === 'number' && isFinite(result)) {
                this.showInstantAnswer(
                    '计算结果',
                    `${query} = <strong>${result}</strong>`,
                    '计算器'
                );
            }
        } catch (e) {
            // 忽略计算错误
        }
    },
    
    showUnitConversionResult(query) {
        this.showInstantAnswer(
            '单位转换',
            '单位转换功能正在开发中...',
            '单位转换器'
        );
    },
    
    showWeatherHint(query) {
        this.showInstantAnswer(
            '天气查询',
            '请输入具体城市名称，例如："北京天气" 或 "Shanghai weather"',
            '天气服务'
        );
    },
    
    showInstantAnswer(title, content, source) {
        const resultsContainer = document.getElementById('results');
        if (!resultsContainer) return;
        
        const instantAnswer = document.createElement('div');
        instantAnswer.className = 'instant-answer';
        instantAnswer.innerHTML = `
            <div class="title">${title}</div>
            <div class="content">${content}</div>
            <div class="source">来源: ${source}</div>
        `;
        
        resultsContainer.insertBefore(instantAnswer, resultsContainer.firstChild);
    }
};

// ===== 搜索增强 =====
const SearchEnhancer = {
    init() {
        this.addKeyboardShortcuts();
        this.addSearchTips();
    },
    
    addKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K 聚焦搜索框
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.getElementById('q');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }
            
            // Escape 清空搜索框
            if (e.key === 'Escape') {
                const searchInput = document.getElementById('q');
                if (searchInput && document.activeElement === searchInput) {
                    searchInput.value = '';
                    searchInput.blur();
                }
            }
        });
    },
    
    addSearchTips() {
        const searchForm = document.getElementById('search');
        if (!searchForm) return;
        
        const tips = document.createElement('div');
        tips.className = 'search-tips';
        tips.innerHTML = `
            <div class="title">搜索技巧</div>
            <div class="tip">使用 <code>!bd</code> 进行百度搜索</div>
            <div class="tip">使用 <code>!gs</code> 进行学术搜索</div>
            <div class="tip">使用 <code>!sgw</code> 进行微信搜索</div>
            <div class="tip">按 <code>Ctrl+K</code> 快速聚焦搜索框</div>
        `;
        
        searchForm.appendChild(tips);
    }
};

// ===== 初始化 =====
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    SearchHistory.init();
    InstantAnswers.init();
    SearchEnhancer.init();
});

// ===== 搜索建议 =====
const SearchSuggestions = {
    // 医疗AI常用搜索词
    medicalTerms: [
        "医疗AI", "人工智能医疗", "AI诊断", "医疗大数据",
        "药物研发", "临床试验", "基因组学", "精准医疗",
        "医学影像", "病理分析", "健康管理", "远程医疗",
        "医疗机器人", "智能问诊", "电子病历", "医疗知识图谱",
        "罕见病", "肿瘤诊断", "心血管疾病", "糖尿病",
        "阿尔茨海默症", "帕金森病", "免疫治疗", "基因治疗"
    ],
    
    // 搜索引擎快捷键
    engineShortcuts: {
        "!bd": "百度搜索",
        "!sg": "搜狗搜索",
        "!360": "360搜索",
        "!go": "Google搜索",
        "!ddg": "DuckDuckGo搜索",
        "!bi": "Bing搜索",
        "!br": "Brave搜索",
        "!gs": "Google Scholar学术搜索",
        "!arx": "arXiv学术搜索",
        "!sgw": "搜狗微信搜索",
        "!gh": "GitHub代码搜索",
        "!st": "StackOverflow技术问答",
        "!hf": "HuggingFace AI模型搜索",
        "!bdi": "百度图片搜索",
        "!sgi": "搜狗图片搜索",
        "!gis": "Google图片搜索",
        "!360v": "360视频搜索",
        "!sgv": "搜狗视频搜索",
        "!yt": "YouTube视频搜索"
    },
    
    init() {
        this.bindEvents();
    },
    
    bindEvents() {
        const searchInput = document.getElementById('q');
        if (!searchInput) return;
        
        // 输入时显示建议
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                this.showSuggestions(query);
            } else {
                this.hideSuggestions();
            }
        });
        
        // 失焦时隐藏建议
        searchInput.addEventListener('blur', () => {
            setTimeout(() => this.hideSuggestions(), 200);
        });
        
        // 键盘导航
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                e.preventDefault();
                this.navigateSuggestions(e.key === 'ArrowDown' ? 1 : -1);
            } else if (e.key === 'Enter') {
                const selected = document.querySelector('.suggestion-item.selected');
                if (selected) {
                    e.preventDefault();
                    searchInput.value = selected.dataset.value;
                    this.hideSuggestions();
                    searchInput.closest('form').submit();
                }
            } else if (e.key === 'Escape') {
                this.hideSuggestions();
            }
        });
    },
    
    showSuggestions(query) {
        this.hideSuggestions();
        
        const suggestions = this.getSuggestions(query);
        if (suggestions.length === 0) return;
        
        const dropdown = document.createElement('div');
        dropdown.className = 'search-suggestions';
        dropdown.innerHTML = suggestions.map((s, i) => `
            <div class="suggestion-item ${i === 0 ? 'selected' : ''}" data-value="${s.value}">
                <span class="suggestion-icon">${s.icon}</span>
                <span class="suggestion-text">${this.highlightMatch(s.text, query)}</span>
                <span class="suggestion-type">${s.type}</span>
            </div>
        `).join('');
        
        const searchInput = document.getElementById('q');
        searchInput.parentNode.appendChild(dropdown);
        
        // 点击建议项
        dropdown.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                searchInput.value = item.dataset.value;
                this.hideSuggestions();
                searchInput.closest('form').submit();
            });
        });
    },
    
    hideSuggestions() {
        const dropdown = document.querySelector('.search-suggestions');
        if (dropdown) {
            dropdown.remove();
        }
    },
    
    getSuggestions(query) {
        const suggestions = [];
        const lowerQuery = query.toLowerCase();
        
        // 匹配医疗AI术语
        this.medicalTerms.forEach(term => {
            if (term.toLowerCase().includes(lowerQuery)) {
                suggestions.push({
                    text: term,
                    value: term,
                    icon: '🏥',
                    type: '医疗AI'
                });
            }
        });
        
        // 匹配搜索引擎快捷键
        Object.entries(this.engineShortcuts).forEach(([shortcut, desc]) => {
            if (shortcut.includes(lowerQuery) || desc.toLowerCase().includes(lowerQuery)) {
                suggestions.push({
                    text: `${shortcut} - ${desc}`,
                    value: shortcut,
                    icon: '🔍',
                    type: '搜索引擎'
                });
            }
        });
        
        // 匹配高级搜索语法
        const advancedSyntax = [
            { syntax: 'site:', desc: '搜索特定网站', example: 'site:github.com' },
            { syntax: 'filetype:', desc: '搜索特定文件类型', example: 'filetype:pdf' },
            { syntax: 'intitle:', desc: '搜索标题关键词', example: 'intitle:医疗' },
            { syntax: 'inurl:', desc: '搜索URL关键词', example: 'inurl:medical' },
            { syntax: 'after:', desc: '搜索指定年份之后', example: 'after:2020' },
            { syntax: 'before:', desc: '搜索指定年份之前', example: 'before:2024' }
        ];
        
        advancedSyntax.forEach(item => {
            if (item.syntax.includes(lowerQuery) || item.desc.includes(lowerQuery)) {
                suggestions.push({
                    text: `${item.syntax} - ${item.desc}`,
                    value: item.example,
                    icon: '⚙️',
                    type: '高级语法'
                });
            }
        });
        
        return suggestions.slice(0, 8); // 最多返回8个建议
    },
    
    navigateSuggestions(direction) {
        const items = document.querySelectorAll('.suggestion-item');
        if (items.length === 0) return;
        
        const current = document.querySelector('.suggestion-item.selected');
        let index = 0;
        
        if (current) {
            index = Array.from(items).indexOf(current);
            index += direction;
            
            if (index < 0) index = items.length - 1;
            if (index >= items.length) index = 0;
            
            current.classList.remove('selected');
        }
        
        items[index].classList.add('selected');
        items[index].scrollIntoView({ block: 'nearest' });
    },
    
    highlightMatch(text, query) {
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<strong>$1</strong>');
    }
};

// ===== 高级搜索面板 =====
const AdvancedSearch = {
    init() {
        this.createToggleButton();
    },
    
    createToggleButton() {
        const searchInput = document.getElementById('q');
        if (!searchInput) return;
        
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'advanced-search-toggle';
        toggleBtn.innerHTML = '⚙️';
        toggleBtn.title = '高级搜索';
        toggleBtn.addEventListener('click', () => this.togglePanel());
        
        searchInput.parentNode.appendChild(toggleBtn);
    },
    
    togglePanel() {
        let panel = document.querySelector('.advanced-search-panel');
        
        if (panel) {
            panel.remove();
            return;
        }
        
        panel = document.createElement('div');
        panel.className = 'advanced-search-panel';
        panel.innerHTML = `
            <div class="advanced-search-header">
                <h3>高级搜索</h3>
                <button class="close-btn" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="advanced-search-body">
                <div class="field">
                    <label>包含以下全部关键词</label>
                    <input type="text" id="adv-all-words" placeholder="例: 医疗 人工智能">
                </div>
                <div class="field">
                    <label>包含以下完整关键词</label>
                    <input type="text" id="adv-exact-phrase" placeholder="例: 医疗AI">
                </div>
                <div class="field">
                    <label>排除以下关键词</label>
                    <input type="text" id="adv-exclude-words" placeholder="例: 游戏 娱乐">
                </div>
                <div class="field">
                    <label>搜索特定网站</label>
                    <input type="text" id="adv-site" placeholder="例: github.com">
                </div>
                <div class="field">
                    <label>文件类型</label>
                    <select id="adv-filetype">
                        <option value="">所有类型</option>
                        <option value="pdf">PDF</option>
                        <option value="doc">Word</option>
                        <option value="ppt">PowerPoint</option>
                        <option value="xls">Excel</option>
                        <option value="txt">文本</option>
                    </select>
                </div>
                <div class="field">
                    <label>时间范围</label>
                    <select id="adv-time-range">
                        <option value="">任何时间</option>
                        <option value="day">过去24小时</option>
                        <option value="week">过去一周</option>
                        <option value="month">过去一月</option>
                        <option value="year">过去一年</option>
                    </select>
                </div>
                <div class="field">
                    <label>语言</label>
                    <select id="adv-language">
                        <option value="auto">自动检测</option>
                        <option value="zh-CN">中文</option>
                        <option value="en">英文</option>
                        <option value="ja">日文</option>
                        <option value="ko">韩文</option>
                    </select>
                </div>
                <div class="advanced-search-actions">
                    <button class="search-btn" onclick="AdvancedSearch.applyFilters()">搜索</button>
                    <button class="reset-btn" onclick="AdvancedSearch.resetFilters()">重置</button>
                </div>
            </div>
        `;
        
        const searchForm = document.getElementById('search');
        searchForm.appendChild(panel);
    },
    
    applyFilters() {
        const searchInput = document.getElementById('q');
        let query = searchInput.value;
        
        // 添加高级搜索语法
        const allWords = document.getElementById('adv-all-words')?.value;
        const exactPhrase = document.getElementById('adv-exact-phrase')?.value;
        const excludeWords = document.getElementById('adv-exclude-words')?.value;
        const site = document.getElementById('adv-site')?.value;
        const filetype = document.getElementById('adv-filetype')?.value;
        
        if (allWords) query += ` ${allWords}`;
        if (exactPhrase) query += ` "${exactPhrase}"`;
        if (excludeWords) query += ` ${excludeWords.split(' ').map(w => `-${w}`).join(' ')}`;
        if (site) query += ` site:${site}`;
        if (filetype) query += ` filetype:${filetype}`;
        
        searchInput.value = query.trim();
        
        // 关闭面板
        document.querySelector('.advanced-search-panel')?.remove();
        
        // 提交搜索
        searchInput.closest('form').submit();
    },
    
    resetFilters() {
        document.getElementById('adv-all-words').value = '';
        document.getElementById('adv-exact-phrase').value = '';
        document.getElementById('adv-exclude-words').value = '';
        document.getElementById('adv-site').value = '';
        document.getElementById('adv-filetype').value = '';
        document.getElementById('adv-time-range').value = '';
        document.getElementById('adv-language').value = 'auto';
    }
};

// 更新初始化
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    SearchHistory.init();
    InstantAnswers.init();
    SearchEnhancer.init();
    SearchSuggestions.init();
    AdvancedSearch.init();
});
