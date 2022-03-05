(function () {
    
    let hr = new XMLHttpRequest()

    document.querySelector('a#logout').addEventListener('click', e => {
        e.preventDefault()
        hr.open('GET', `${window.location.protocol}//${window.location.host}/c-logout`)
        hr.send()

        hr.onreadystatechange = function() {
            if (hr.readyState === 4) {
                document.querySelector('span#c-status').textContent = 'Déconnecté'
            }
        }
    })
    let form =  document.getElementById('search-form')
    form.addEventListener('submit', e => {
        console.log('Form submit')
        e.preventDefault()
        let data = new FormData(form)
        
        hr.open('GET', `${window.location.protocol}//${window.location.host}/followers?username=${data.get('username')}`, true)
        
        hr.send(data)
        

        hr.onreadystatechange = function () {
            if (hr.readyState === 4) {
                if (hr.status == 200) {
                    var followers = JSON.parse(hr.responseText).data.splice(0, 6)
                    document.querySelector('#datas').textContent = `${followers.length} followers found`
                    followers.forEach(user => {
                        let li = document.createElement('li')
                        li.textContent = user
                        li.classList.add('list-group-item')
                
                        document.querySelector('#list').appendChild(li)
                        document.querySelector('#datas').textContent = `${followers.length} utilisateurs trouvés`
                        
                    })

                    hr.open('GET', `${window.location.protocol}//${window.location.host}/sendmass?users=${JSON.stringify(followers)}`)
                    hr.send()
                    hr.onreadystatechange = function() {
                        if(hr.readyState === 4) {
                            document.querySelector('#datas').textContent = `${JSON.parse(hr.responseText).message}`
                        }
                    }
                }
            }
        }
    })

    let send_link = document.querySelector('a#send-link')
    send_link.addEventListener('click', e => {
        console.log('Click on send')
        e.preventDefault()
        hr.open('GET', `${window.location.protocol}//${window.location.host}/sendmass?users=${JSON.stringify(followers)}`)

        hr.onreadystatechange = function() {
            if(hr.readyState === 4) {
                document.querySelector('#datas').textContent = `${hr.responseText}`
            }
        }
    })
    let send = document.getElementById('send-form')
    send.addEventListener('submit', e => {
            e.preventDefault()
            let data = new FormData(send)
            
            hr.open('POST', `${window.location.protocol}//${window.location.host}/send`, true)
            hr.send(data)

            hr.onreadystatechange = function () {
                if (hr.readyState === 4) {
                    if (hr.status == 200) {
                        document.querySelector('#datas').textContent = JSON.parse(hr.responseText).message
                    }
                }
            }
        }
    )
    }
)()