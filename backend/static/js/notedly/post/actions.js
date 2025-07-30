document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.dataset.postId;
            fetch("ajax/toggle-like/", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `post_id=${postId}`
            })
            .then(res => res.json())
            .then(data => {
                this.querySelector('.like-count').textContent = data.likes_count;
                // this.textContent = data.liked ? `❤️ ${data.likes_count}` : `🤍 ${data.likes_count}`;
            });
        });
    });

    document.querySelectorAll('.bookmark-btn').forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.dataset.postId;
            fetch("/ajax/toggle-bookmark/", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `post_id=${postId}`
            })
            .then(res => res.json())
            .then(data => {
                this.querySelector('.bookmark-count').textContent = data.bookmarks_count;
                // this.textContent = data.bookmarked ? `🔖 ${data.bookmarks_count}` : `📄 ${data.bookmarks_count}`;
            });
        });
    });
});
