

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
    const clicked = event.currentTarget
    retrieveMessages(clicked.dataset)
}


const conversationElements = document.getElementsByClassName("convo");

for(let i =0; i < conversationElements.length; i++){
    conversationElements[i].addEventListener('click', convoClick, false);
}


    
setHeaderImage()