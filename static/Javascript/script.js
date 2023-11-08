const body = document.querySelector('body'),  
      sidebar = body.querySelector('.sidebar'),
      toggleSwitch = body.querySelector('.toggle'), 
      // searchBox = body.querySelector('.search-box'),
      modeSwitch = body.querySelector('.toggle-switch'),
      modeText = body.querySelector('.mode-text');

      // searchBox.addEventListener('click', () => {
      //   sidebar.classList.remove('close')
      // });

      modeSwitch.addEventListener('click', () => {
        body.classList.toggle('dark')

        if(body.classList.contains('dark')) 
        {
            modeText.innerText = 'light Mode'
        } else {
            modeText.innerText = 'Dark Mode'
        }
      });

      toggleSwitch.addEventListener('click', () => {
        sidebar.classList.toggle('close')
      });


      const sub_pages = document.querySelector('.sub_pages ul');
      const sales_icon = document.querySelector('.icon-text a');
      