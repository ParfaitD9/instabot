let hr = new XMLHttpRequest()

hr.open('GET', `${window.location.protocol}//${window.location.host}/existants-messages`, true)
hr.send()
hr.onreadystatechange = function() {
    if (hr.readyState === 4) {
        msgs = JSON.parse(hr.responseText).data
        msgs.forEach(msg => {
            opt = document.createElement('option')
            opt.value = msg[0]
            opt.textContent = msg[1].substring(0, 30) + ' ...'
            document.querySelector('#existants').appendChild(opt)
        })
    }
}

let form1 = document.querySelector('#form-1')
form1.addEventListener('submit', e => {
    e.preventDefault()
    let form1_datas = new FormData(form1)
    hr.open('POST', `${window.location.protocol}//${window.location.host}/default`, true)
    hr.send(form1_datas)

    hr.onreadystatechange = function () {
        if (hr.readyState === 4){
            document.querySelector('#result-1').textContent = JSON.parse(hr.responseText).message
        }
    }
})

let form2 = document.querySelector('#form-2')
form2.addEventListener('submit', e => {
    e.preventDefault()
    let form2_datas = new FormData(form2)
    if (form2_datas.get('message').length > 1){
        hr.open('POST', `${window.location.protocol}//${window.location.host}/new-message`, true)
        hr.send(form2_datas)

        hr.onreadystatechange = function () {
            if (hr.readyState === 4){
                document.querySelector('#result-2').textContent = JSON.parse(hr.responseText).message
            }
        }
    } else {
        document.querySelector('#result-2').textContent = 'Veuillez saisir un message.'
    }
})