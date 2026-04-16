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
      <div class="modal-overlay" @click.self="showEditForm = false">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>修改个人信息</h3>
            <button class="close-btn" @click="showEditForm = false">×</button>
          </div>

          <div class="form-content">
            <!-- 头像上传 -->
            <div class="form-group">
              <label>新头像:</label>
              <div class="avatar-upload">
                <img
                  :src="previewAvatar || userData.avatar"
                  alt="头像预览"
                  class="avatar-preview"
                />
                <button class="upload-btn" @click="triggerFileInput">
                  <i class="fas fa-upload"></i> 选择图片
                </button>
                <input
                  type="file"
                  ref="avatarInput"
                  accept="image/*"
                  style="display: none"
                  @change="handleAvatarChange"
                />
              </div>
            </div>

            <!-- 昵称修改 -->
            <div class="form-group">
              <label>新昵称:</label>
              <input
                type="text"
                v-model="newName"
                placeholder="请输入新昵称"
                class="name-input"
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
      <div class="modal-content project-detail-modal">
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
            <p>这是一个重要的数字建筑遗产修复项目，采用了先进的AI技术和传统修复工艺相结合的方法，确保了修复效果的真实性和艺术性。</p>
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
      showEditForm: false,
      selectedProject: null,
      newName: '',
      previewAvatar: null,
      userData: {
        avatar: '/images/logo.png',
        name: '修复大师',
        title: '高级图像修复师 | 数字建筑遗产保护中心',
        stats: {
          repairCount: 256,
          favoriteProjects: 12,
          satisfaction: '98%'
        },
        basicInfo: {
          username: '修复师',
          position: '高级图像修复师',
          organization: '数字建筑遗产保护中心 | 数字修复部门',
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
            title: '侨乡老照片修复',
            date: '2023.08.15',
            tags: ['AI修复', '色彩还原'],
            image: '/images/江门.png'
          },
          {
            title: '横州市云表镇伏波庙修复',
            date: '2023.07.22',
            tags: ['细节增强', '纹理修复'],
            image: '/images/广西1.png'
          },
          {
            title: '百色市西林岑氏家族建筑群修复',
            date: '2023.06.30',
            tags: ['去污处理', '细节增强'],
            image: '/images/广西2.png'
          }
        ]
      }
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.avatarInput.click();
    },
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
    saveChanges() {
      if (this.newName && this.newName.trim() !== "") {
        this.userData.name = this.newName.trim();
      }
      if (this.previewAvatar) {
        this.userData.avatar = this.previewAvatar;
      }
      this.showEditForm = false;
      this.newName = "";
      this.previewAvatar = null;
      alert("保存成功！");
    },
    handleImageError(event) {
      event.target.src = "https://via.placeholder.com/120?text=Avatar";
    },
    handleProjectImageError(event) {
      event.target.src = "https://via.placeholder.com/300x200?text=Project+Image";
    }
  }
};
</script>

<style scoped>
/* 个人中心样式 - 使用标准px单位 */
.profile-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 30px 40px 80px;
    color: #fff;
    min-height: calc(100vh - 100px);
}

/* 用户信息头部 */
.profile-header {
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(0, 216, 255, 0.3);
}

.avatar-section {
    cursor: pointer;
    display: inline-block;
}

.profile-avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 15px;
    border: 3px solid #00d8ff;
    box-shadow: 0 0 20px rgba(0, 216, 255, 0.5);
    transition: transform 0.3s ease;
}

.profile-avatar:hover {
    transform: scale(1.05);
}

.profile-name {
    font-size: 28px;
    color: #00d8ff;
    margin-bottom: 8px;
    cursor: pointer;
    text-shadow: 0 0 10px rgba(0, 216, 255, 0.5);
}

.profile-name:hover {
    text-decoration: underline;
}

.profile-title {
    font-size: 16px;
    color: #a0d7ff;
    margin-bottom: 20px;
}

/* 统计数据 */
.profile-stats {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 20px;
}

.stat-item {
    text-align: center;
    padding: 12px 24px;
    background: rgba(11, 61, 102, 0.5);
    border-radius: 12px;
    min-width: 100px;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(0, 216, 255, 0.3);
}

.stat-value {
    font-size: 24px;
    font-weight: bold;
    color: #00d8ff;
}

.stat-label {
    font-size: 14px;
    color: #a0d7ff;
    margin-top: 5px;
}

/* 卡片样式 */
.profile-card {
    background: rgba(2, 22, 45, 0.6);
    border: 1px solid rgba(0, 216, 255, 0.3);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 30px;
    backdrop-filter: blur(5px);
    transition: all 0.3s ease;
}

.profile-card:hover {
    border-color: rgba(0, 216, 255, 0.6);
    box-shadow: 0 0 20px rgba(0, 216, 255, 0.2);
}

.card-title {
    font-size: 20px;
    color: #00d8ff;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-left: 3px solid #00d8ff;
    padding-left: 15px;
}

.card-title i {
    font-size: 20px;
}

/* 基本信息列表 */
.info-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.info-item {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
}

.info-label {
    width: 100px;
    font-size: 14px;
    color: #59ebe8;
    font-weight: 500;
}

.info-value {
    flex: 1;
    font-size: 15px;
    color: #e0e8ff;
}

/* 技能列表 */
.skills-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.skill-item {
    width: 100%;
}

.skill-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.skill-name {
    color: #e0f7ff;
    font-weight: 500;
    font-size: 14px;
}

.skill-percentage {
    color: #00d8ff;
    font-size: 14px;
}

.skill-bar {
    height: 8px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    overflow: hidden;
}

.skill-progress {
    height: 100%;
    background: linear-gradient(to right, #00d8ff, #0066ff);
    border-radius: 4px;
    transition: width 0.3s ease;
}

/* 近期项目区域 */
.recent-projects-container {
    margin-top: 10px;
}

.section-title {
    color: #00d8ff;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 24px;
    border-left: 3px solid #00d8ff;
    padding-left: 15px;
}

.section-title i {
    font-size: 22px;
    color: #00d8ff;
}

/* 项目网格布局 */
.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 24px;
}

/* 单个项目卡片 */
.project-card {
    background: rgba(0, 102, 255, 0.1);
    border: 1px solid rgba(0, 194, 255, 0.2);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    backdrop-filter: blur(5px);
}

.project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 194, 255, 0.2);
    border-color: #00c2ff;
}

/* 项目图片区域 */
.project-image-container {
    height: 180px;
    overflow: hidden;
    position: relative;
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

.project-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.project-card:hover .project-overlay {
    opacity: 1;
}

.project-overlay i {
    font-size: 32px;
    color: #00c2ff;
}

/* 项目内容区域 */
.project-content {
    padding: 16px;
}

.project-title {
    color: #fff;
    font-size: 16px;
    margin: 0 0 10px 0;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.project-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    flex-wrap: wrap;
    gap: 8px;
}

.project-date {
    color: #8eb6f5;
    display: flex;
    align-items: center;
    gap: 4px;
}

.project-tags {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.project-tag {
    background: rgba(0, 194, 255, 0.2);
    color: #00c2ff;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
}

/* 模态框样式 */
.project-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(5px);
    z-index: 2000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.project-detail-modal {
    background: linear-gradient(135deg, #1a2a4a 0%, #0f1a2e 100%);
    border: 2px solid #00c2ff;
    border-radius: 16px;
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 0 40px rgba(0, 194, 255, 0.4);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 24px;
    border-bottom: 1px solid rgba(0, 194, 255, 0.3);
}

.modal-title {
    color: #00c2ff;
    margin: 0;
    font-size: 20px;
}

.close-btn {
    background: #ff4757;
    color: white;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.close-btn:hover {
    background: #ff3742;
    transform: scale(1.1);
}

.modal-body {
    padding: 24px;
}

.project-image {
    margin-bottom: 20px;
    border-radius: 12px;
    overflow: hidden;
}

.project-image img {
    width: 100%;
    max-height: 300px;
    object-fit: cover;
}

.project-details {
    margin-bottom: 20px;
}

.detail-item {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    color: #e0f7fa;
    flex-wrap: wrap;
}

.detail-item i {
    color: #00c2ff;
    font-size: 16px;
}

.detail-label {
    font-weight: bold;
    color: #4fc3f7;
}

.detail-value {
    flex: 1;
}

.tags-container {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.detail-tag {
    background: linear-gradient(45deg, #00c2ff, #0066ff);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
}

.project-description h4 {
    color: #00c2ff;
    margin-bottom: 10px;
    font-size: 16px;
}

.project-description p {
    color: #e0f7fa;
    line-height: 1.6;
    font-size: 14px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 24px;
    border-top: 1px solid rgba(0, 194, 255, 0.3);
}

.action-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
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
    z-index: 1500;
}

.modal-overlay {
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: center;
    align-items: center;
}

.profile-edit-modal .modal-content {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    border: 2px solid #00c2ff;
    border-radius: 16px;
    width: 90%;
    max-width: 450px;
    padding: 0;
    box-shadow: 0 0 40px rgba(0, 194, 255, 0.4);
}

.profile-edit-modal .modal-header {
    padding: 20px 24px;
    border-bottom: 1px solid rgba(0, 194, 255, 0.3);
}

.profile-edit-modal .modal-header h3 {
    color: #00c2ff;
    margin: 0;
    font-size: 20px;
}

.form-content {
    padding: 24px;
    color: white;
}

.form-group {
    margin-bottom: 24px;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    color: #00c2ff;
    font-weight: bold;
}

.avatar-upload {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.avatar-preview {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 2px solid #00c2ff;
    object-fit: cover;
}

.upload-btn {
    background: linear-gradient(to right, #01cfff, #0066ff);
    border: none;
    border-radius: 8px;
    color: white;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.upload-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(1, 207, 255, 0.4);
}

.name-input {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #00c2ff;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    font-size: 14px;
    box-sizing: border-box;
}

.name-input:focus {
    outline: none;
    border-color: #4fc3f7;
    box-shadow: 0 0 10px rgba(79, 195, 247, 0.3);
}

.name-input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}

.form-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
    margin-top: 24px;
}

.cancel-btn, .save-btn {
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
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

/* 响应式设计 */
@media (max-width: 768px) {
    .profile-container {
        padding: 20px;
    }
    
    .profile-stats {
        flex-direction: column;
        gap: 12px;
        align-items: center;
    }
    
    .stat-item {
        width: 100%;
        max-width: 200px;
    }
    
    .profile-avatar {
        width: 100px;
        height: 100px;
    }
    
    .profile-name {
        font-size: 24px;
    }
    
    .profile-title {
        font-size: 14px;
    }
    
    .info-item {
        flex-direction: column;
        gap: 4px;
    }
    
    .info-label {
        width: auto;
    }
    
    .project-grid {
        grid-template-columns: 1fr;
    }
    
    .modal-footer {
        flex-direction: column;
    }
    
    .action-btn {
        width: 100%;
        justify-content: center;
    }
    
    .avatar-upload {
        flex-direction: column;
        align-items: center;
    }
    
    .form-actions {
        flex-direction: column;
    }
    
    .cancel-btn, .save-btn {
        width: 100%;
    }
}
</style>