document.querySelectorAll('.card').forEach(card => {
          const price = parseFloat(card.dataset.price || '0');
          const qtyInput = card.querySelector('.qty-input');
          card.querySelector('.qty-decrease').addEventListener('click', () => {
            qtyInput.value = Math.max(0, parseInt(qtyInput.value || '1') - 1);
          });
          card.querySelector('.qty-increase').addEventListener('click', () => {
            qtyInput.value = Math.max(0, parseInt(qtyInput.value || '1') + 1);
          });
        });