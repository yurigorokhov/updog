

const setHeaderImage = () => {
    const pageElement = document.querySelector('#self-image');
    let imageElement = document.createElement('img');
    imageElement.classList.add('icon-img');
    imageElement.setAttribute('src', "http://lorempixel.com/output/animals-q-c-284-204-8.jpg");
    imageElement.setAttribute('alt', 'Puppy Icon Image for user');
    pageElement.appendChild(imageElement);
}




const wrapMessages = (message, time) => {
    let pageElement = document.querySelector('#main-chat-wrap');
    let div1Element = document.createElement('div');
    let div2Element = document.createElement('div');
    let paragrapeElement = document.createElement('p');
    let timeElement = document.createElement('p')
    div1Element.classList.add('message-wrap');
    div2Element.classList.add('message');
    div2Element.classList.add(message.sent ? 'out' : 'in')
    paragrapeElement.classList.add('mssg');
    timeElement.classList.add('mssg-time')
    pageElement.appendChild(div1Element);
    div1Element.appendChild(div2Element);
    div2Element.appendChild(paragrapeElement)
    div2Element.appendChild(timeElement)
    paragrapeElement.innerHTML = `${message}`
    timeElement.innerHTML = `${time}`

}



const addMessages = (messages) =>{
    let pageElement = document.querySelector('#main-chat-wrap');
    pageElement.innerHTML = ''
    messages.forEach(message => wrapMessages(message.body, message["time-stamp"]))

    }

const retrieveMessages = (req_info) => {
    const url = `/api/chats/${req_info.chat_id}/messages?user_id=${req_info.user_id}`
    fetch(url, {
        method: 'GET'
    }).then(res => res.json())
      .then(data => addMessages(data))
}


const convoClick = (event) => {
    
    // populate form chat_id input
    const clicked = event.currentTarget;
    const dataAttributes = clicked.dataset;
    const chat_id = dataAttributes.chat_id;
    document.querySelector('#sndr-chat_id').value = chat_id;
    
    // retrieve messages for clicked conversation
    retrieveMessages(dataAttributes);
}


const conversationElements = document.getElementsByClassName("convo");

for(let i =0; i < conversationElements.length; i++){
    conversationElements[i].addEventListener('click', convoClick, false);
}



const submitNewMessage = () => {

    // collect data needed for message POST request
    const newMessage = document.querySelector('#new-message').value;
    const chat_id = document.querySelector('#sndr-chat_id').value;
    const user_id = document.querySelector('#sndr-name').value;

    // make POST request to create the message
    const url = `/api/chats/${chat_id}/messages?user_id=${user_id}`;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'body': newMessage
        })
    })
    .then(res => {
        return res.json()
    })
    .then(data => {
        wrapMessages(data.body, data['time-stamp'])
        document.querySelector('#new-message').value = '';
        document.querySelector(`div.convo[data-chat_id="${chat_id}"] p.mssg`).innerHTML = data.body
    })
}


    
setHeaderImage()