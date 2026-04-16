#!/bin/bash
# =====================================
# 一键启动脚本：文化遗产图像修复系统
# 后端 + 前端 自动启动（MacBook 专用）
# =====================================

# 更新为最新的项目路径
BACKEND_DIR="/Users/ouxiaoying/Documents/项目/ican终稿（数字建筑）/backend"
FRONTEND_DIR="/Users/ouxiaoying/Documents/项目/ican终稿（数字建筑）/my-vue-app"

# 检查后端目录
if [ ! -d "$BACKEND_DIR" ]; then
  echo "❌ 后端目录不存在: $BACKEND_DIR"
  exit 1
fi

# 检查前端目录
if [ ! -d "$FRONTEND_DIR" ]; then
  echo "❌ 前端目录不存在: $FRONTEND_DIR"
  exit 1
fi

# 启动后端服务（新终端窗口，已添加 OpenMP 冲突修复环境变量）
echo "🚀 启动后端服务..."
osascript <<EOF
tell application "Terminal"
    do script "cd \"$BACKEND_DIR\" && export KMP_DUPLICATE_LIB_OK=TRUE && source ~/miniconda3/etc/profile.d/conda.sh && conda activate MA-SPA-GAN && python3 app.py"
end tell
EOF

# 等待几秒钟确保后端启动
sleep 5

# 启动前端服务（另一个终端窗口）
echo "🌐 启动前端服务器..."
osascript <<EOF
tell application "Terminal"
    do script "cd \"$FRONTEND_DIR\" && source ~/.bash_profile && npm run dev"
end tell
EOF

# 输出信息
echo "✅ 所有服务已启动！预祝 iCAN 比赛顺利！"
echo "------------------------------------"
echo "后端：http://127.0.0.1:8000"
echo "前端：http://localhost:5173"
echo "------------------------------------"