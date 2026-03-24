$(function () {


    /* ===============================================================
         LIGHTBOX
      =============================================================== */
    lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true
    });


    /* ===============================================================
         PRODUCT SLIDER
      =============================================================== */
    $('.product-slider').owlCarousel({
        items: 1,
        thumbs: true,
        thumbImage: false,
        thumbsPrerendered: true,
        thumbContainerClass: 'owl-thumbs',
        thumbItemClass: 'owl-thumb-item'
    });


    /* ===============================================================
         PRODUCT QUNATITY
      =============================================================== */
      $('.dec-btn').click(function () {
          var siblings = $(this).siblings('input');
          if (parseInt(siblings.val(), 10) >= 1) {
              siblings.val(parseInt(siblings.val(), 10) - 1);
          }
      });

      $('.inc-btn').click(function () {
          var siblings = $(this).siblings('input');
          siblings.val(parseInt(siblings.val(), 10) + 1);
      });


      /* ===============================================================
           BOOTSTRAP SELECT
        =============================================================== */
      $('.selectpicker').on('change', function () {
          $(this).closest('.dropdown').find('.filter-option-inner-inner').addClass('selected');
      });


      /* ===============================================================
           TOGGLE ALTERNATIVE BILLING ADDRESS
        =============================================================== */
      $('#alternateAddressCheckbox').on('change', function () {
         var checkboxId = '#' + $(this).attr('id').replace('Checkbox', '');
         $(checkboxId).toggleClass('d-none');
      });


      /* ===============================================================
           DISABLE UNWORKED ANCHORS
        =============================================================== */
      $('a[href="#"]').on('click', function (e) {
         e.preventDefault();
      });


      /* ===============================================================
           HEADER SEARCH OVERLAY
        =============================================================== */
      var $searchOverlay = $('#headerSearchOverlay');
      var $searchToggle = $('.header-search-toggle');

      function openHeaderSearch() {
          $searchOverlay.addClass('is-open').attr('aria-hidden', 'false');
          $searchToggle.attr('aria-expanded', 'true');
          setTimeout(function () {
              $searchOverlay.find('input[type="search"]').trigger('focus');
          }, 120);
      }

      function closeHeaderSearch() {
          $searchOverlay.removeClass('is-open').attr('aria-hidden', 'true');
          $searchToggle.attr('aria-expanded', 'false');
      }

      $searchToggle.on('click', function () {
          if ($searchOverlay.hasClass('is-open')) {
              closeHeaderSearch();
          } else {
              openHeaderSearch();
          }
      });

      $(document).on('click', '.header-search-close', function () {
          closeHeaderSearch();
      });

      $(document).on('keydown', function (e) {
          if (e.key === 'Escape' && $searchOverlay.hasClass('is-open')) {
              closeHeaderSearch();
          }
      });

});


/* ===============================================================
     COUNTRY SELECT BOX FILLING
  =============================================================== */
$.getJSON('/static/js/countries.json', function (data) {
    $.each(data, function (key, value) {
        var selectOption = "<option value='" + value.name + "' data-dial-code='" + value.dial_code + "'>" + value.name + "</option>";
        $("select.country").append(selectOption);
    });
})
