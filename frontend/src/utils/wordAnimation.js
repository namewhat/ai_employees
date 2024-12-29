export class WordCardAnimation {
    constructor() {
        this.textBox = document.querySelector('.text-box');
        this.progressInner = document.querySelector('.progress-inner');
        this.progressText = document.querySelector('.progress-text');
        this.progressNumber = document.querySelector('.progress-number');
        this.animation = null;
        this.startTime = null;
        this.cards = [];
        this.currentWord = null;
        
        // 动画配置
        this.ANIMATION_DURATION = 15000;
        this.CARD_INTERVAL = 500;
        this.CARD_MIN_WIDTH = 100;
        this.CARD_HEIGHT = 70;
        this.OVERLAP_THRESHOLD = 0.3;
        this.TEXT_ANIMATION_INTERVAL = 1000;
        
        // 音频配置
        this.audio = new Audio();
        this.isPlaying = false;
        this.lastAudioTime = 0;
        this.MIN_INTERVAL = 300;
        this.MAX_INTERVAL = 800;
        this.WAVE_DURATION = 2000;
        
        // 音频播放速率配置
        this.BASE_PLAYBACK_RATE = 0.9;
        this.MAX_PLAYBACK_RATE = 1.8;
        
        // 监听音频加载完成
        this.audio.addEventListener('loadedmetadata', () => {
            this.audio.preservesPitch = true;
            // 获取自然发音时长
            this.naturalDuration = this.audio.duration * 1000; // 转换为毫秒
            // 计算总播放次数（15秒除以自然发音时长，向上取整）
            this.totalPlayCount = Math.ceil(this.ANIMATION_DURATION / this.naturalDuration)+5;
            // 计算实际的播放间隔
            this.playInterval = this.ANIMATION_DURATION / this.totalPlayCount;
            console.log(`Natural duration: ${this.naturalDuration}ms, Total plays: ${this.totalPlayCount}, Interval: ${this.playInterval}ms`);
        });
        this.isLoading = false;
        
        // 卡片配置
        this.MAX_CARDS = 10;
        this.CARD_WIDTH = 150;
        this.CARD_HEIGHT = 70;
        this.GRID_COLS = 3;  // 网格列数
        this.GRID_ROWS =3;  // 网格行数
        this.occupiedSpaces = new Set();  // 记录已占用的网格位置
        
        // 添加中心卡片配置
        this.centerCard = null;
        this.CENTER_CARD_Z_INDEX = 9999; // 确保中心卡片始终在最上层
        
        // 添加音频状态
        this.audioContext = null;
        this.hasInteracted = false;
        
        // 添加用户交互监听
        document.addEventListener('click', () => {
            if (!this.hasInteracted) {
                this.initAudioContext();
            }
        });
        
        document.addEventListener('keydown', () => {
            if (!this.hasInteracted) {
                this.initAudioContext();
            }
        });
    }

    initAudioContext() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.hasInteracted = true;
        }
        
        // 恢复音频上下文
        if (this.audioContext.state === 'suspended') {
            this.audioContext.resume();
        }
    }

    async restart(wordType = null) {
        try {
            // 显示加载状态
            this.isLoading = true;
            this.showLoading();
            
            // 清空现有卡片
            this.textBox.innerHTML = '';
            this.cards = [];
            this.progressInner.style.width = '0%';
            
            // 重置音频状态
            this.audio.pause();
            this.audio.currentTime = 0;
            this.isPlaying = false;
            this.lastAudioTime = 0;
            
            // 如果用户还没有交互，显示提示
            if (!this.hasInteracted) {
                this.showInteractionPrompt();
                return;
            }
            
            // 获取新的随机单词
            const response = await fetch(`/api/word/random${wordType ? `?word_type=${wordType}` : ''}`);
            if (!response.ok) throw new Error('Failed to fetch word');
            this.currentWord = await response.json();
            
            // 隐藏加载状态
            this.isLoading = false;
            this.hideLoading();
            
            // 重置计数器
            this.currentPlayCount = 0;
            
            // 设置音频源
            this.audio.src = this.currentWord.audio_url;
            
            // 等待音频加载完成
            await new Promise(resolve => {
                this.audio.addEventListener('loadedmetadata', resolve, { once: true });
            });
            
            if (this.animation) {
                cancelAnimationFrame(this.animation);
            }
            
            this.startTime = Date.now();
            this.lastAnimationTime = 0;
            this.animate();
            this.startAudioLoop();
            this.animateProgressText();
            
            // 重置中心卡片
            this.centerCard = null;
            
        } catch (error) {
            console.error('Error fetching word:', error);
            this.isLoading = false;
            this.hideLoading();
            this.showError('获取单词失败，请重试');
        }
    }

    showLoading() {
        // 创建加载提示
        const loading = document.createElement('div');
        loading.className = 'word-loading';
        loading.innerHTML = `
            <div class="loading-spinner"></div>
            <div class="loading-text">加载中...</div>
        `;
        this.textBox.appendChild(loading);
    }

    hideLoading() {
        const loading = this.textBox.querySelector('.word-loading');
        if (loading) {
            loading.remove();
        }
    }

    showError(message) {
        // 可以添加错误提示UI
        console.error(message);
    }

    animate() {
        const currentTime = Date.now();
        const elapsed = currentTime - this.startTime;
        const progress = Math.min(elapsed / this.ANIMATION_DURATION * 100, 100);
        
        this.progressInner.style.width = `${progress}%`;
        this.progressNumber.textContent = `${Math.round(progress)}%`;
        
        if (currentTime - this.lastAnimationTime >= this.TEXT_ANIMATION_INTERVAL) {
            this.animateProgressText();
            this.lastAnimationTime = currentTime;
        }
        
        if (elapsed < this.ANIMATION_DURATION) {
            this.animation = requestAnimationFrame(() => this.animate());
        }
    }

    startAudioLoop() {
        const checkAndPlay = async () => {
            const currentTime = Date.now();
            const elapsed = currentTime - this.startTime;
            const progress = elapsed / this.ANIMATION_DURATION;
            
            if (progress >= 1 || this.currentPlayCount >= this.totalPlayCount) {
                return;
            }
            
            // 检查是否应该播放下一次
            const shouldPlayNext = elapsed >= (this.currentPlayCount * this.playInterval);
            
            if (!this.isPlaying && shouldPlayNext) {
                this.currentPlayCount++;
                await this.playAudioAndAddCard();
            }
            
            requestAnimationFrame(checkAndPlay);
        };
        
        requestAnimationFrame(checkAndPlay);
    }

    calculateCurrentInterval(elapsed) {
        // 根据当前播放速率调整间隔
        const currentRate = this.calculatePlaybackRate(elapsed);
        const baseInterval = this.MIN_INTERVAL + 
                           (1 - (currentRate - 1.0) / 0.7) * (this.MAX_INTERVAL - this.MIN_INTERVAL);
        
        // 添加波动效果
        const wavePosition = (elapsed % this.WAVE_DURATION) / this.WAVE_DURATION;
        const wave = Math.pow(Math.sin(wavePosition * Math.PI * 2), 2);
        
        // 间隔随速率动态调整
        return baseInterval * (0.8 + wave * 0.4);
    }

    calculatePlaybackRate(elapsed) {
        const progress = elapsed / this.ANIMATION_DURATION;
        
        // 使用三个正弦波叠加来创建更自然的波动
        const wave1 = Math.sin(progress * Math.PI * 2) * 0.3;
        const wave2 = Math.sin(progress * Math.PI * 4) * 0.1;
        const wave3 = Math.sin(progress * Math.PI * 8) * 0.05;
        
        // 基础曲线：开始慢，中间快，结束慢
        const baseCurve = -4 * Math.pow(progress - 0.5, 2) + 1;
        
        // 合并所有波形
        const combinedWave = wave1 + wave2 + wave3 + baseCurve;
        
        // 映射到目标范围
        const rate = this.BASE_PLAYBACK_RATE + 
                    (combinedWave + 1) * (this.MAX_PLAYBACK_RATE - this.BASE_PLAYBACK_RATE) / 2;
        
        return Math.max(this.BASE_PLAYBACK_RATE, Math.min(this.MAX_PLAYBACK_RATE, rate));
    }

    async playAudioAndAddCard() {
        try {
            if (!this.hasInteracted) {
                console.warn('Waiting for user interaction...');
                return;
            }

            this.isPlaying = true;
            
            // 获取当前时间点的播放速率
            const elapsed = Date.now() - this.startTime;
            const currentRate = this.calculatePlaybackRate(elapsed);
            
            // 设置当前播放速率
            this.audio.playbackRate = currentRate;
            
            // 创建新卡片
            const card = this.createCard();
            this.cards.push(card);
            this.textBox.appendChild(card);
            
            try {
                // 尝试播放音频
                await this.audio.play();
            } catch (error) {
                if (error.name === 'NotAllowedError') {
                    console.warn('Audio playback requires user interaction');
                    this.showInteractionPrompt();
                    return;
                }
                throw error;
            }
            
            // 检查重叠并移除重叠过多的卡片
            this.checkAndRemoveOverlappingCards();
            
            // 限制最大卡片数量
            while (this.cards.length > this.MAX_CARDS) {
                const oldCard = this.cards.shift();
                oldCard.classList.add('fade-out');
                setTimeout(() => oldCard.remove(), 300);
            }
            
            this.lastAudioTime = Date.now();
            this.isPlaying = false;
            
        } catch (error) {
            console.error('Error playing audio:', error);
            this.isPlaying = false;
        }
    }

    createCard() {
        const card = document.createElement('div');
        card.className = 'word-card';
        
        // 设置卡片内容
        card.innerHTML = `
            <div class="word">${this.currentWord.word}</div>
            <div class="phonetic">${this.currentWord.phonetic}</div>
            <div class="meaning">${this.currentWord.meaning}</div>
        `;
        
        // 计算中心点位置
        const boxWidth = this.textBox.offsetWidth;
        const boxHeight = this.textBox.offsetHeight;
        const centerX = (boxWidth - this.CARD_WIDTH) / 2;
        const centerY = (boxHeight - this.CARD_HEIGHT) / 2;
        
        // 先将卡片放在中心点
        card.style.left = `${centerX}px`;
        card.style.top = `${centerY}px`;
        card.style.opacity = '0';
        card.style.transform = 'scale(0.8)';
        
        // 如果还没有中心卡片，将这个卡片设为中心卡片
        if (!this.centerCard) {
            this.centerCard = card;
            card.style.zIndex = this.CENTER_CARD_Z_INDEX;
            
            // 中心卡片保持在中心位置，不旋转
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    card.style.left = `${centerX}px`;
                    card.style.top = `${centerY}px`;
                    card.style.opacity = '1';
                    card.style.transform = 'scale(0.8)'; // 保持80%大小
                });
            });
            
            return card;
        }
        
        // 对于非中心卡片，计算随机位置
        const { x, y, rotation, zIndex } = this.calculateCardPosition();
        
        // 获取当前播放速率
        const elapsed = Date.now() - this.startTime;
        const currentRate = this.calculatePlaybackRate(elapsed);
        
        // 设置过渡效果
        const transitionSpeed = Math.random() < 0.3 ? 0.2 : 0.3;
        card.style.transition = `all ${transitionSpeed / currentRate}s cubic-bezier(0.4, 0, 0.2, 1)`;
        card.style.zIndex = zIndex;
        
        // 移动到随机位置
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                card.style.left = `${x}px`;
                card.style.top = `${y}px`;
                card.style.opacity = '1';
                card.style.transform = `scale(0.8) rotate(${rotation}deg)`; // 所有卡片保持80%大小
            });
        });
        
        return card;
    }

    calculateCardPosition() {
        const boxWidth = this.textBox.offsetWidth;
        const boxHeight = this.textBox.offsetHeight;
        const margin = 10;
        
        // 尝试找到最佳位置的最大次数
        const MAX_ATTEMPTS = 10;
        let bestPosition = null;
        let minOverlap = Infinity;
        
        for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
            // 生成候选位置
            const candidate = this.generateRandomPosition(boxWidth, boxHeight, margin);
            
            // 计算与现有卡片的总重叠面积
            const overlapArea = this.calculateTotalOverlap(candidate);
            
            // 更新最佳位置
            if (overlapArea < minOverlap) {
                minOverlap = overlapArea;
                bestPosition = candidate;
            }
            
            // 如果找到几乎不重叠的位置，直接使用
            if (overlapArea < 0.1) { // 10%以下的重叠是可接受的
                break;
            }
        }
        
        return bestPosition;
    }

    generateRandomPosition(boxWidth, boxHeight, margin) {
        // 将区域分成更小的网格（5x5以获得更均匀的分布
        const GRID_SIZE = 6;
        const gridWidth = (boxWidth - this.CARD_WIDTH) / GRID_SIZE;
        const gridHeight = (boxHeight - this.CARD_HEIGHT) / GRID_SIZE;
        
        // 随机选择一个网格单元
        const gridX = Math.floor(Math.random() * GRID_SIZE);
        const gridY = Math.floor(Math.random() * GRID_SIZE);
        
        // 在选中的网格单元内随机取点
        let x = gridX * gridWidth + Math.random() * gridWidth;
        let y = gridY * gridHeight + Math.random() * gridHeight;
        
        // 添加随机偏移
        const offset = 20;
        x += (Math.random() - 0.5) * offset;
        y += (Math.random() - 0.5) * offset;
        
        // 确保不完全超出边界
        x = Math.max(-this.CARD_WIDTH * 0.3, Math.min(boxWidth - this.CARD_WIDTH * 0.7, x));
        y = Math.max(-this.CARD_HEIGHT * 0.3, Math.min(boxHeight - this.CARD_HEIGHT * 0.7, y));
        
        // 随机旋转
        const rotation = Math.random() * 40 - 20;
        
        // 随机层级
        const zIndex = Math.floor(Math.random() * 10);
        
        return { x, y, rotation, zIndex };
    }

    calculateTotalOverlap(position) {
        let totalOverlap = 0;
        
        // 计算新卡片的边界
        const newCard = {
            left: position.x,
            right: position.x + this.CARD_WIDTH,
            top: position.y,
            bottom: position.y + this.CARD_HEIGHT
        };
        
        // 检查与每个现有卡片的重叠
        for (const card of this.cards) {
            const rect = card.getBoundingClientRect();
            const boxRect = this.textBox.getBoundingClientRect();
            
            // 转换为相对坐标
            const existingCard = {
                left: rect.left - boxRect.left,
                right: rect.right - boxRect.left,
                top: rect.top - boxRect.top,
                bottom: rect.bottom - boxRect.top
            };
            
            // 计算重叠面积
            const overlapX = Math.min(newCard.right, existingCard.right) - 
                            Math.max(newCard.left, existingCard.left);
            const overlapY = Math.min(newCard.bottom, existingCard.bottom) - 
                            Math.max(newCard.top, existingCard.top);
            
            if (overlapX > 0 && overlapY > 0) {
                const overlap = (overlapX * overlapY) / (this.CARD_WIDTH * this.CARD_HEIGHT);
                totalOverlap += overlap;
            }
        }
        
        return totalOverlap;
    }

    checkAndRemoveOverlappingCards() {
        const cardsToRemove = new Set();
        
        // 检查所有卡片对之间的重叠，跳过中心卡片
        for (let i = 0; i < this.cards.length; i++) {
            for (let j = i + 1; j < this.cards.length; j++) {
                // 如果任一卡片是中心卡片，跳过检查
                if (this.cards[i] === this.centerCard || this.cards[j] === this.centerCard) {
                    continue;
                }
                
                const overlap = this.calculatePairOverlap(this.cards[i], this.cards[j]);
                if (overlap > 0.3) {
                    cardsToRemove.add(this.cards[i]);
                }
            }
        }
        
        // 移除重叠的卡片，但不移除中心卡片
        cardsToRemove.forEach(card => {
            if (card !== this.centerCard) {
                const index = this.cards.indexOf(card);
                if (index > -1) {
                    this.cards.splice(index, 1);
                    card.classList.add('fade-out');
                    setTimeout(() => card.remove(), 300);
                }
            }
        });
    }

    calculatePairOverlap(card1, card2) {
        const rect1 = card1.getBoundingClientRect();
        const rect2 = card2.getBoundingClientRect();
        const boxRect = this.textBox.getBoundingClientRect();
        
        // 转换为相对坐标
        const r1 = {
            left: rect1.left - boxRect.left,
            right: rect1.right - boxRect.left,
            top: rect1.top - boxRect.top,
            bottom: rect1.bottom - boxRect.top
        };
        
        const r2 = {
            left: rect2.left - boxRect.left,
            right: rect2.right - boxRect.left,
            top: rect2.top - boxRect.top,
            bottom: rect2.bottom - boxRect.top
        };
        
        const overlapX = Math.min(r1.right, r2.right) - Math.max(r1.left, r2.left);
        const overlapY = Math.min(r1.bottom, r2.bottom) - Math.max(r1.top, r2.top);
        
        if (overlapX > 0 && overlapY > 0) {
            return (overlapX * overlapY) / (this.CARD_WIDTH * this.CARD_HEIGHT);
        }
        
        return 0;
    }

    animateProgressText() {
        // 固定显示文本
        this.progressText.textContent = "正在传输到你的脑子里";
    }

    showInteractionPrompt() {
        // 创建交互提示
        const prompt = document.createElement('div');
        prompt.className = 'interaction-prompt';
        prompt.innerHTML = `
            <div class="prompt-content">
                <div class="prompt-icon">👆</div>
                <div class="prompt-text">点击任意位置开始学习</div>
            </div>
        `;
        
        // 添加点击事件
        prompt.addEventListener('click', () => {
            this.initAudioContext();
            prompt.remove();
            this.restart();
        });
        
        this.textBox.appendChild(prompt);
    }
} 