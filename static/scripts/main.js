const settingsBtn = document.querySelector('#settings-btn')
const settingsDiv = document.querySelector('#settings')
const outerDiv = document.querySelector('#outer-settings')


settingsBtn.addEventListener('click', () => {
  if (settingsDiv.style.display == 'none') {
    outerDiv.style.display = 'block'
    outerDiv.style.zIndex = '9999'
    settingsDiv.style.display = 'block'
    settingsDiv.style.zIndex = '10000'
  }
  else {
    outerDiv.style.display = 'none'
    settingsDiv.style.display = 'none'
  }
})

outerDiv.addEventListener('click', () => {
  outerDiv.style.display = 'none'
  settingsDiv.style.display = 'none'
})


