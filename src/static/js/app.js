//import usernames from "./datas"

let usernames = [
    'Lorem',
    'ipsum',
    'dolor',
    'sit',
    'amet',
    'consectetur',
    'adipisicing',
    'elit',
    'Quo',
    'nisi',
    'velit',
    'dolore',
    'excepturi',
    'quidem',
    'delectus',
    'consequatur',
    'eaque'
]


/*
<ul class="list-group">
  <li class="list-group-item">Cras justo odio</li>
  <li class="list-group-item">Dapibus ac facilisis in</li>
  <li class="list-group-item">Morbi leo risus</li>
  <li class="list-group-item">Porta ac consectetur ac</li>
  <li class="list-group-item">Vestibulum at eros</li>
</ul>
*/

let form =  document.getElementById('search-form')
form.addEventListener('submit', e => {
    e.preventDefault()
    let hr = new XMLHttpRequest()
    
    let data = new FormData(form)
    
    hr.open('GET', `${window.location.protocol}//${window.location.host}/followers?username=${data.get('username')}`, true)
    
    hr.send(data)
    console.log(data)
    console.log(hr.responseURL)

    hr.onreadystatechange = function () {
        if (hr.readyState === 4) {
            if (hr.status == 200) {
                let data = JSON.parse(hr.responseText).data
                document.querySelector('#datas').textContent = `${data.length} followers found`
                data.forEach(user => {
                    let li = document.createElement('li')
                    li.textContent = user
                    li.classList.add('list-group-item')
            
                    document.querySelector('#list').appendChild(li)
            
                })
            }
        }
    }

    
    document.querySelector('#datas').textContent = `${usernames.length} utilisateurs trouvés`
    document.querySelector('#send').style.display = 'block'
})

let send = document.getElementById('send-form')
send.addEventListener('submit', e => {
        e.preventDefault()
        let hr = new XMLHttpRequest()
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