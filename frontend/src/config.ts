export const settings = {
  // API配置
  API_URL: '/api',
  
  // AI服务配置
  KIMI_URL: 'https://kimi.moonshot.cn',
  KELING_URL: 'https://www.kelingai.com',
  
  // 分页配置
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZES: [10, 20, 50, 100],
  
  // 上传配置
  UPLOAD: {
    QUOTE_ACCEPT: '.txt',
    IMAGE_ACCEPT: '.jpg,.jpeg,.png',
    MAX_SIZE: 5 * 1024 * 1024  // 5MB
  },
  
  // 生成配置
  GENERATE: {
    MAX_QUOTES: 20,
    MAX_IMAGES: 4
  },
  
  // 提示词建议
  PROMPT_SUGGESTIONS: {
    QUOTES: [
      '成功',
      '励志',
      '人生',
      '爱情',
      '友情',
      '工作',
      '学习',
      '梦想'
    ],
    IMAGES: [
      '风景',
      '美食',
      '动物',
      '建筑',
      '人物',
      '艺术',
      '科技',
      '自然'
    ]
  }
} 