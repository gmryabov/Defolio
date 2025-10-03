(function($) {

  // Получение product_type селекта
  const productTypeSelect = $('#id_product_type');
  function initRow($row) {
  const propertySelect = $row.find('select[id$="-property"]');
  const valueSelect = $row.find('select[id$="-value"]');
  const currentValue = valueSelect.data('current-value'); // получить data-current-value

  if (!propertySelect.length || !valueSelect.length) return;

  propertySelect.off('change').on('change', function () {
    const propertyId = $(this).val();
    const productTypeId = $('#id_product_type').val();

    // При смене свойства сбрасываем valueSelect и подгружаем новые опции без выбранного значения
    loadValueOptions(propertyId, valueSelect, null, productTypeId);
  });

  // Если есть выбранное свойство — загрузить опции значений, передав currentValue из data-current-value
  const selectedProperty = propertySelect.val();
  if (selectedProperty) {
    const productTypeId = $('#id_product_type').val();
    loadValueOptions(selectedProperty, valueSelect, currentValue, productTypeId);
  }
}


  // Загрузка опций значений по выбранному свойству
  // function loadValueOptions(propertyId, valueSelect, currentValue, productTypeId) {
  //   const rememberedValue = currentValue || valueSelect.val(); // сохраняем до .empty()
  //   valueSelect.empty().append($('<option>').val('').text('---------'));
  //
  //   if (!propertyId) return;
  //
  //   $.ajax({
  //     url: `/admin/store/product/get_property_values/`,
  //     method: 'GET',
  //     data: {
  //       property_id: propertyId,
  //       product_type_id: productTypeId
  //     },
  //     success: function (data) {
  //       data.values.forEach(function (item) {
  //         const option = $('<option>')
  //             .val(item.id)
  //             .text(item.value);
  //         if (String(item.id) === String(rememberedValue)) {
  //           option.prop('selected', true);
  //         }
  //         valueSelect.append(option);
  //       });
  //     },
  //     error: function (err) {
  //       console.error('Ошибка загрузки значений:', err);
  //     }
  //   });
  // }

  function loadValueOptions(propertyId, valueSelect, currentValue, productTypeId) {
  // если currentValue не определено, берем текущее значение valueSelect до очистки
  const rememberedValue = currentValue !== null && currentValue !== undefined
      ? currentValue
      : valueSelect.val();

  valueSelect.empty().append($('<option>').val('').text('---------'));

  if (!propertyId) return;

  $.ajax({
    url: `/admin/shop/product/get_property_values/`,
    method: 'GET',
    data: { property_id: propertyId, product_type_id: productTypeId },
    success: function (data) {
      data.values.forEach(function (item) {
        const option = $('<option>').val(item.id).text(item.value);
        if (String(item.id) === String(rememberedValue)) {
          option.prop('selected', true);
        }
        valueSelect.append(option);
      });

      // если после добавления опций ничего не выбрано — сбросим выбор
      if (!valueSelect.val()) {
        valueSelect.val('');
      }
    },
    error: function (err) {
      console.error('Ошибка загрузки значений:', err);
    }
  });
}



  // Загрузка свойств (props) по product_type и обновление селекта свойств
  function loadValueOptions(propertyId, valueSelect, currentValue, productTypeId) {
  const rememberedValue = (currentValue !== null && currentValue !== undefined)
      ? currentValue
      : valueSelect.val();

  valueSelect.empty().append($('<option>').val('').text('---------'));

  if (!propertyId) return;

  $.ajax({
    url: `/admin/shop/product/get_property_values/`,
    method: 'GET',
    data: { property_id: propertyId, product_type_id: productTypeId },
    success: function (data) {
      data.values.forEach(function (item) {
        const option = $('<option>').val(item.id).text(item.value);
        if (String(item.id) === String(rememberedValue)) {
          option.prop('selected', true);
        }
        valueSelect.append(option);
      });
      // Если после заполнения нет выбранного значения, выбрать пустой option
      if (!valueSelect.val()) {
        valueSelect.val('');
      }
    },
    error: function (err) {
      console.error('Ошибка загрузки значений:', err);
    }
  });
}


  $(document).ready(function () {
    const productTypeSelect = $('#id_product_type');
    // Инициализация уже существующих инлайнов
    $('tr.form-row').each(function () {
      initRow($(this));
    });

    // При изменении product_type — обновляем свойства во всех инлайнах
    productTypeSelect.on('change', function() {
      const ptId = $(this).val();
      loadProperties(ptId);
    });

    // Наблюдаем за добавлением новых инлайнов и инициализируем их
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.addedNodes.forEach(function (node) {
          const $node = $(node);
          if ($node.is('tr.form-row') || $node.find('select[id$="-property"]').length) {
            initRow($node);
          }
        });
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });

    // При загрузке страницы, сразу загрузим свойства для текущего product_type
    const initialProductTypeId = productTypeSelect.val();
    if (initialProductTypeId) {
      loadProperties(initialProductTypeId);
    }
  });
})(django.jQuery);
