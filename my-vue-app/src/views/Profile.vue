<template>
  <div class="profile-container">
    <!-- 用户信息头部 -->
    <div class="profile-header">
      <div class="avatar-section" @click="showEditForm = true">
        <img 
          :src="userData.avatar" 
          alt="用户头像" 
          class="profile-avatar"
          @error="handleImageError"
        />
      </div>
      
      <div class="profile-info">
        <h2 class="profile-name" @click="showEditForm = true">
          {{ userData.name }}
        </h2>
        <p class="profile-title">{{ userData.title }}</p>
      </div>
      
      <!-- 统计数据 -->
      <div class="profile-stats">
        <div class="stat-item">
          <div class="stat-value">{{ userData.stats.repairCount }}</div>
          <div class="stat-label">修复次数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ userData.stats.favoriteProjects }}</div>
          <div class="stat-label">收藏项目</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ userData.stats.satisfaction }}</div>
          <div class="stat-label">满意度</div>
        </div>
      </div>
    </div>

    <!-- 修改头像和昵称的表单模态框 -->
<div v-if="showEditForm" class="profile-edit-modal">
  <!-- 遮罩层，点击空白关闭 -->
  <div class="modal-overlay" @click.self="showEditForm = false">
    <!-- 模态内容 -->
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>修改个人信息</h3>
        <button class="close-btn" @click="showEditForm = false">×</button>
      </div>

      <div class="form-content">
        <!-- 头像上传 -->
        <div class="form-group">
          <label for="newAvatar">新头像:</label>
          <div class="avatar-upload">
            <img
              :src="previewAvatar || userData.avatar"
              alt="头像预览"
              class="avatar-preview"
            />
            <input
              type="file"
              id="newAvatar"
              accept="image/*"
              @change="handleAvatarChange"
            />
          </div>
        </div>

        <!-- 昵称修改 -->
        <div class="form-group">
          <label for="newName">新昵称:</label>
          <input
            type="text"
            id="newName"
            v-model="newName"
            placeholder="请输入新昵称"
          />
        </div>

        <div class="form-actions">
          <button class="save-btn" @click="saveChanges">保存</button>
          <button class="cancel-btn" @click="showEditForm = false">取消</button>
        </div>
      </div>
    </div>
  </div>
</div>

    <!-- 基本信息卡片 -->
    <div class="profile-card">
      <h3 class="card-title">
        <i class="fas fa-user-circle"></i>
        <span class="title-text">基本信息</span>
      </h3>
      
      <div class="info-list">
        <div class="info-item">
          <div class="info-label">用户名</div>
          <div class="info-value">{{ userData.basicInfo.username }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">职位</div>
          <div class="info-value">{{ userData.basicInfo.position }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">机构</div>
          <div class="info-value">{{ userData.basicInfo.organization }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">专业领域</div>
          <div class="info-value">{{ userData.basicInfo.expertise }}</div>
        </div>
        <div class="info-item">
          <div class="info-label">加入时间</div>
          <div class="info-value">{{ userData.basicInfo.joinDate }}</div>
        </div>
      </div>
    </div>

    <!-- 修复技能卡片 -->
    <div class="profile-card">
      <h3 class="card-title">
        <i class="fas fa-tools"></i>
        <span class="title-text">专业技能</span>
      </h3>
      
      <div class="skills-list">
        <div class="skill-item" v-for="skill in userData.skills" :key="skill.name">
          <div class="skill-info">
            <span class="skill-name">{{ skill.name }}</span>
            <span class="skill-percentage">{{ skill.progress }}%</span>
          </div>
          <div class="skill-bar">
            <div 
              class="skill-progress" 
              :style="{ width: skill.progress + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 近期项目卡片 -->
    <div class="recent-projects-container">
      <h3 class="section-title">
        <i class="fas fa-project-diagram"></i>
        <span class="title-text">近期项目</span>
      </h3>
      
      <div class="project-grid">
        <div 
          class="project-card" 
          v-for="project in userData.projects" 
          :key="project.title"
          @click="selectedProject = project"
        >
          <div class="project-image-container">
            <img 
              :src="project.image" 
              :alt="project.title"
              @error="handleProjectImageError"
            />
            <div class="project-overlay">
              <i class="fas fa-search-plus"></i>
            </div>
          </div>
          <div class="project-content">
            <h4 class="project-title">{{ project.title }}</h4>
            <div class="project-meta">
              <span class="project-date">
                <i class="far fa-calendar-alt"></i> {{ project.date }}
              </span>
              <div class="project-tags">
                <span 
                  v-for="tag in project.tags" 
                  :key="tag" 
                  class="project-tag"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 项目详情模态框 -->
    <div v-if="selectedProject" class="project-modal" @click.self="selectedProject = null">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">{{ selectedProject.title }}</h3>
          <button class="close-btn" @click="selectedProject = null">×</button>
        </div>
        
        <div class="modal-body">
          <div class="project-image">
            <img 
              :src="selectedProject.image" 
              :alt="selectedProject.title"
              @error="handleProjectImageError"
            />
          </div>
          
          <div class="project-details">
            <div class="detail-item">
              <i class="far fa-calendar-alt"></i>
              <span class="detail-label">修复完成:</span>
              <span class="detail-value">{{ selectedProject.date }}</span>
            </div>
            
            <div class="detail-item">
              <i class="fas fa-tags"></i>
              <span class="detail-label">技术标签:</span>
              <div class="tags-container">
                <span 
                  v-for="tag in selectedProject.tags" 
                  :key="tag" 
                  class="detail-tag"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="project-description">
            <h4>项目描述</h4>
            <p>这是一个重要的文化遗产修复项目，采用了先进的AI技术和传统修复工艺相结合的方法，确保了修复效果的真实性和艺术性。</p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="action-btn secondary" @click="selectedProject = null">关闭</button>
          <button class="action-btn primary">
            <i class="fas fa-download"></i> 下载修复结果
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileCenter',
  data() {
    return {
      // 控制编辑表单显示
      showEditForm: false,
      // 选中的项目
      selectedProject: null,
      // 表单数据
      formData: {
        name: '',
        avatar: null
      },
      // 头像预览
      previewAvatar: null,
      // 用户数据
      userData: {
        avatar: '/images/logo.png',
        name: '修复大师',
        title: '高级图像修复师 | 文化遗产保护中心',
        stats: {
          repairCount: 256,
          favoriteProjects: 12,
          satisfaction: '98%'
        },
        basicInfo: {
          username: '宝宝',
          position: '高级图像修复师',
          organization: '文化遗产保护中心 | 数字修复部门',
          expertise: '古画修复、老照片修复、文物数字化',
          joinDate: '2020年5月'
        },
        skills: [
          { name: 'AI修复', progress: 95 },
          { name: '传统修复', progress: 88 },
          { name: '色彩校正', progress: 92 },
          { name: '细节增强', progress: 96 }
        ],
        projects: [
          {
            title: '江门侨乡老照片修复',
            date: '2023.08.15',
            tags: ['AI修复', '色彩还原'],
            image: '/images/江门.png'
          },
          {
            title: '清代书画数字化修复',
            date: '2023.07.22',
            tags: ['细节增强', '纹理修复'],
            image: '/images/书画.png'
          },
          {
            title: '民国档案修复工程',
            date: '2023.06.30',
            tags: ['去污处理', '文字增强'],
            image: '/images/文件.png'
          }
        ]
      }
    }
  },
    methods: {
    // 上传头像
    handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewAvatar = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    // 保存更改
    saveChanges() {
      console.log("正在保存...");

      // ✅ 检查昵称是否有输入
      if (this.newName && this.newName.trim() !== "") {
        this.userData.name = this.newName.trim();
      }

      // ✅ 如果上传了头像，则更新
      if (this.previewAvatar) {
        this.userData.avatar = this.previewAvatar;
      }

      // ✅ 关闭弹窗并重置状态
      this.showEditForm = false;
      this.newName = "";
      this.previewAvatar = null;

      alert("保存成功！");
    },

    // 头像加载失败时替换默认图
    handleImageError(event) {
      event.target.src = "https://via.placeholder.com/80?text=No+Image";
    },
  },
};
</script>

<style scoped>
/* 个人中心样式 */
.profile-container {
    max-width: 100%;
    padding: 3rem;
    color: #fff;
    overflow: auto;
     min-height: 110vh; /* 新增：确保容器有足够高度 */
}

.profile-header {
    text-align: center;
    margin-bottom: 4rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid rgba(0, 216, 255, 0.3);
}

.profile-avatar {
    width: 25rem;
    height: 25rem;
    border-radius: 50%;
    object-fit: cover;
    margin: 10rem auto 2rem;
    border: 2px solid #00d8ff;
    box-shadow: 0 0 0.3rem rgba(0, 216, 255, 0.5);
}

.profile-name {
    font-size: 0.3rem;
    color: #00d8ff;
    margin-bottom: 0.1rem;
    text-shadow: 0 0 0.1rem rgba(0, 216, 255, 0.3);
}

.profile-title {
    font-size: 0.18rem;
    color: #a0d7ff;
    margin-bottom: 0.3rem;
}

.profile-stats {
    display: flex;
    justify-content: center;
    gap: 0.4rem;
    margin-top: 0.3rem;
}

.stat-item {
    text-align: center;
    padding: 1rem 3rem;
    background: rgba(11, 61, 102, 0.5);
    border-radius: 0.1rem;
    min-width: 1rem;
}

.stat-value {
    font-size: 0.24rem;
    font-weight: bold;
    color: #00d8ff;
}

.stat-label {
    font-size: 0.14rem;
    color: #a0d7ff;
}

/* 卡片样式 */
.profile-card {
    background: rgba(2, 22, 45, 0.6);
    border: 1px solid #217093;
    border-radius: 0.1rem;
    padding: 3rem;
    margin-bottom: 5rem;
    box-shadow: 0 0 0.3rem rgba(0, 216, 255, 0.2) inset;
    position: relative;
    overflow: hidden;
    box-sizing: border-box;
    overflow: auto;
}

.profile-card:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, rgba(0, 216, 255, 0.1) 0%, transparent 50%);
    z-index: 0;
}

.card-title {
    font-size: 0.22rem;
    color: #00d8ff;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    position: relative;
    z-index: 1;
}

.card-title i {
    margin-right: 8rem;
    font-size: 0.2rem;
}

.info-item {
    display: flex;
    margin-bottom: 1.5rem;
    position: relative;
    flex-direction: row; /* 确保横向排列 */
    align-items: center; /* 垂直居中 */
    z-index: 1;
}

.info-label {
    width: 1.2rem;
    font-size: 0.16rem;
    color: #59ebe8;
    text-align: left; /* 左对齐 */
    white-space: nowrap; /* 防止文字换行 */
    margin-right: 25rem; /* 添加右边距 */
}

.info-value {
    flex: 1;
    font-size: 1.6rem;
    color: #d0e8ff;
}

/* 技能条样式 */
.skill-bar {
    height: 2rem;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 0.04rem;
    margin-top: 0.5rem;
    width: 100%; 
}

/* 技能名称样式 */
.skill-item {
    display: flex;
    align-items: center;
    width: 100%; /* 确保技能项宽度为100% */
    margin-bottom: rem;
}

.skill-name {
    color: #e0f7ff;  
    font-weight: 500;
    margin-right: 0.5rem; /* 添加右边距 */
}

.skill-progress {
    height: 2rem; /* 增加高度使进度条更粗 */
    background: linear-gradient(to right, #01cfff, #0066ff);
    border-radius: 4rem;
    position: relative;
    transition: width 0.3s ease;
}

.skill-progress:after {
    content: attr(style);
    position: absolute;
    right: 5rem;
    top: -6rem;
    font-size: 0.12rem;
    color: #00d8ff;
}

/* 近期项目整体容器 */
.recent-projects-container {
    margin-top: 0.5rem;
    padding: 0.3rem;
    background: rgba(234, 228, 228, 0.05);
    border-radius: 0.3rem;
    overflow: auto;
}

.recent-projects-container h3 {
    color: #00c2ff;
    font-size: 5rem;
    margin-bottom: 0.2rem;
    padding-bottom: 0.1rem;
    border-bottom: 1px solid rgba(0, 194, 255, 0.3);
}

/* --- 近期项目标题颜色修复 --- */
.section-title {
  color: #40a7e6 !important;  /* 亮蓝色 */
  display: flex;
  align-items: center;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

/* --- 图标颜色修复 --- */
.section-title i {
  color: #40a7e6 !important;  /* 同样的亮蓝色 */
  margin-right: 0.5rem;
  font-size: 2.2rem;
  text-shadow: 0 0 8px rgba(0, 170, 255, 0.6);
  padding-left: 3rem;
}

/* --- 近期项目标题文字颜色 --- */
.section-title .title-text {
  color: #40a7e6 !important;
  text-shadow: 0 0 5px rgba(0, 207, 255, 0.6);
  padding-left: 8rem;
}


/* 项目网格布局 */
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 0.3rem;
}

/* 单个项目卡片 */
.project-card {
    background: rgba(0, 102, 255, 0.1);
    border: 1px solid rgba(0, 194, 255, 0.2);
    border-radius: 0.2rem;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
}

.project-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 194, 255, 0.2);
    border-color: #00c2ff;
}

/* 项目图片区域 */
.project-image-container {
    height: 160px;
    overflow: hidden;
}

.project-image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.project-card:hover .project-image-container img {
    transform: scale(1.05);
}

/* 项目内容区域 */
.project-content {
    padding: 0.15rem;
}

.project-content h4 {
    color: #fff;
    font-size: 0.18rem;
    margin: 0 0 0.1rem 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.project-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.14rem;
}

.project-date {
    color: #8eb6f5;
}

.project-tags {
    display: flex;
    gap: 0.1rem;
}

.project-tags span {
    background: rgba(0, 194, 255, 0.2);
    color: #00c2ff;
    padding: 0.02rem 0.08rem;
    border-radius: 0.1rem;
    font-size: 0.12rem;
}

/* 模态框样式 */
.project-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    animation: fadeIn 0.3s ease;
}

.modal-content {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    border: 3px solid #00c2ff;
    border-radius: 15px;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 0 40px rgba(0, 194, 255, 0.5);
    animation: slideUp 0.3s ease;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5rem;
    border-bottom: 1px solid rgba(0, 194, 255, 0.3);
    background: rgba(0, 0, 0, 0.2);
}

.modal-title {
    color: #00c2ff;
    margin: 0;
    font-size: 5rem;
    text-shadow: 0 0 10px rgba(0, 194, 255, 0.5);
}

.close-btn {
    background: #ff4757;
    color: white;
    border: none;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    font-size: 1.3rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.close-btn:hover {
    background: #ff3742;
    transform: scale(1.1);
}

.modal-body {
    padding: 1.5rem;
}

.project-image {
    margin-bottom: 1rem;
}

.project-image img {
    width: 100%;
    max-height: 300px;
    object-fit: cover;
    border-radius: 8px;
    border: 2px solid #00c2ff;
}

.project-details {
    margin-bottom: 1.5rem;
}

.detail-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.8rem;
    color: #e0f7fa;
}

.detail-item i {
    color: #00c2ff;
    margin-right: 0.5rem;
    font-size: 1.1rem;
}

.detail-label {
    font-weight: bold;
    margin-right: 0.5rem;
    color: #4fc3f7;
}

.detail-value {
    flex: 1;
}

.tags-container {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.detail-tag {
    background: linear-gradient(45deg, #00c2ff, #0066ff);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: bold;
    box-shadow: 0 2px 8px rgba(0, 194, 255, 0.3);
}

.project-description h4 {
    color: #00c2ff;
    margin-bottom: 0.8rem;
    font-size: 1.2rem;
}

.project-description p {
    color: #e0f7fa;
    line-height: 1.6;
    font-size: 0.9rem;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    padding: 1.5rem;
    border-top: 1px solid rgba(0, 194, 255, 0.3);
    background: rgba(0, 0, 0, 0.2);
}

.action-btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.action-btn.secondary {
    background: #6c757d;
    color: white;
}

.action-btn.secondary:hover {
    background: #5a6268;
}

.action-btn.primary {
    background: linear-gradient(to right, #00b09b, #96c93d);
    color: white;
}

.action-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 176, 155, 0.4);
}

/* 编辑表单模态框 */
.profile-edit-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.5); /* 调整透明度 */
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 80%;
    padding: 50rem;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    z-index: 1;
    display: flex;
    justify-content: center;
    align-items: cente
}

.form-content {
    color: white;
}

.form-group {
    margin-bottom: 8rem;
}

.form-group label {
    display: block;
    margin-bottom: 5rem;
    color: #00c2ff;
    font-weight: bold;
}

.avatar-upload {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.avatar-preview {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 2px solid #00c2ff;
    object-fit: cover;
}

.avatar-upload input[type="file"] {
    display: none;
}

.upload-btn {
    background: linear-gradient(to right, #01cfff, #0066ff);
    border: none;
    border-radius: 5px;
    color: white;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.upload-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(1, 207, 255, 0.4);
}

.form-group input[type="text"] {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #00c2ff;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 1rem;
}

.form-group input[type="text"]:focus {
    outline: none;
    border-color: #4fc3f7;
    box-shadow: 0 0 10px rgba(79, 195, 247, 0.3);
}

.form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 2rem;
}

.cancel-btn, .save-btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.cancel-btn {
    background: #6c757d;
    color: white;
}

.cancel-btn:hover {
    background: #5a6268;
}

.save-btn {
    background: linear-gradient(to right, #00b09b, #96c93d);
    color: white;
}

.save-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 176, 155, 0.4);
}

/* 动画 */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .profile-stats {
        flex-direction: column;
        gap: 0.2rem;
    }

    .profile-card {
        width: 100%; /* 在大屏幕上宽度为100% */
    }
    
    .project-grid {
        grid-template-columns: 1fr;
    }
    
    .modal-content {
        margin: 1rem;
        padding: 1rem;
        z-index: 2;
    }
    
    .avatar-upload {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .form-actions {
        flex-direction: column;
    }
    
    .modal-footer {
        flex-direction: column;
    }
    
    .action-btn {
        width: 100%;
        justify-content: center;
    }
}
</style>