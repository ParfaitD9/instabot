(
    function () {
        let hr = new XMLHttpRequest()

        document.querySelector('a#logout').addEventListener('click', e => {
            e.preventDefault()
            hr.open('GET', `${window.location.protocol}//${window.location.host}/logout`, true)
            hr.open()
            
            hr.onreadystatechange = function () {
                if (hr.readyState === 4) {
                    document.querySelector('span#c-status').textContent = 'Deconnecté'
                }
            }
        })
    }
)()