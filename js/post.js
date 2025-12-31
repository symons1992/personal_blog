// 获取URL中的文章ID
function getPostIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// 从API获取文章详情
async function fetchPostDetail(postId) {
    try {
        const response = await fetch(`http://localhost:5001/api/posts/${postId}`);
        const data = await response.json();
        
        if (data.success) {
            return data.data;
        } else {
            console.error('获取文章详情失败:', data.message);
            return null;
        }
    } catch (error) {
        console.error('网络错误:', error);
        return null;
    }
}

// 渲染文章详情
async function renderPostDetail() {
    const postId = getPostIdFromUrl();
    const postContent = document.getElementById('post-content');
    
    if (!postId) {
        postContent.innerHTML = '<div style="text-align: center; padding: 4rem 0; font-size: 1.2rem; color: #666;">文章ID不存在</div>';
        return;
    }
    
    const post = await fetchPostDetail(postId);
    
    if (post) {
        postContent.innerHTML = `
            <article class="post">
                <h1 class="post-title">${post.title}</h1>
                <div class="post-meta">
                    <span>发布日期: ${post.date}</span>
                    <span>分类: ${post.category}</span>
                    <span>作者: ${post.author}</span>
                </div>
                <img src="${post.image}" alt="${post.title}" class="post-image">
                <div class="post-body">
                    <p>${post.excerpt}</p>
                    <p>${post.content || '本文暂无详细内容。'}</p>
                </div>
            </article>
            <div class="post-actions">
                <a href="index.html" class="btn">返回首页</a>
            </div>
        `;
    } else {
        postContent.innerHTML = '<div style="text-align: center; padding: 4rem 0; font-size: 1.2rem; color: #666;">文章不存在</div>';
    }
}

// 移动端汉堡菜单交互
function initHamburgerMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
}

// 平滑滚动效果
function initSmoothScroll() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', async () => {
    await renderPostDetail();
    initHamburgerMenu();
    initSmoothScroll();
});