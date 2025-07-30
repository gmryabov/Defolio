document.addEventListener('DOMContentLoaded', function () {
  const dropdown = document.getElementById('post_dropdown');
  const toggleBtn = dropdown.querySelector('.dropdown-toggle');
  const hiddenInput = document.getElementById('post_category');

  dropdown.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', function (e) {
      e.preventDefault();

      // 1. Обновляем содержимое кнопки
      toggleBtn.innerHTML = this.innerHTML;

      // 2. Устанавливаем значение hidden input
      const selectedId = this.getAttribute('data-id');
      hiddenInput.value = selectedId;

      // 3. Обновляем active класс
      dropdown.querySelectorAll('.dropdown-item').forEach(i => i.classList.remove('active'));
      this.classList.add('active');
    });
  });
});
