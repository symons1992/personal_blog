// 从API获取博客文章数据
async function fetchBlogPosts() {
    try {
        const response = await fetch('http://localhost:5001/api/posts');
        const data = await response.json();
        
        if (data.success) {
            return data.data;
        } else {
            console.error('获取文章失败:', data.message);
            return [];
        }
    } catch (error) {
        console.error('网络错误:', error);
        return [];
    }
}

// 动态生成博客文章卡片
async function renderBlogPosts() {
    const blogGrid = document.querySelector('.blog-grid');
    
    // 显示加载状态
    blogGrid.innerHTML = '<div style="text-align: center; padding: 2rem; font-size: 1.2rem; color: #666;">加载中...</div>';
    
    const blogPosts = await fetchBlogPosts();
    
    // 清空加载状态
    blogGrid.innerHTML = '';
    
    if (blogPosts.length === 0) {
        blogGrid.innerHTML = '<div style="text-align: center; padding: 2rem; font-size: 1.2rem; color: #666;">暂无文章</div>';
        return;
    }
    
    blogPosts.forEach(post => {
        const blogCard = document.createElement('div');
        blogCard.className = 'blog-card';
        
        blogCard.innerHTML = `
            <img src="${post.image}" alt="${post.title}">
            <div class="blog-card-content">
                <div class="blog-card-meta">
                    <span>${post.date}</span>
                    <span>${post.category}</span>
                    <span>${post.author}</span>
                </div>
                <h3>${post.title}</h3>
                <p>${post.excerpt}</p>
                <a href="#post-${post.id}" class="btn read-more" data-post-id="${post.id}">阅读全文</a>
            </div>
        `;
        
        // 添加点击事件监听器，跳转到文章详情页
        const readMoreBtn = blogCard.querySelector('.read-more');
        readMoreBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.getAttribute('data-post-id');
            window.location.href = `post.html?id=${postId}`;
        });
        
        blogGrid.appendChild(blogCard);
    });
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

// 平滑滚动效果 - 只针对导航链接
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
    await renderBlogPosts();
    initHamburgerMenu();
    initSmoothScroll();
});